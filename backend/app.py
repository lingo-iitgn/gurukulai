import os
# Set environment variable to control which GPUs are visible and their mapping
os.environ["CUDA_VISIBLE_DEVICES"] = "0,2"  # Makes physical GPU 1 appear as cuda:0
DEVICE = "cuda:0"  # Use first available GPU after environment variable setting

import torch
import json
import faiss
import pickle
from unsloth import FastLanguageModel
from transformers import AutoTokenizer, AutoModel
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback
import markdown
import time
import pandas as pd
from infer_llama import generate_answer, search_faiss, get_full_chapter_context
from pdf_mappings import get_pdf_link
import re

# Initialize Flask app with static folder for serving static files
app = Flask(__name__, static_folder="static", static_url_path="/gurukulai/static")
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend compatibility

# Configure logging to save logs to a file with timestamp, level, and message
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
app.logger.setLevel(logging.DEBUG)  # Set Flask app logger to DEBUG level

# Create directory for storing user responses if it doesn't exist
os.makedirs("user_responses", exist_ok=True)

# Dictionary to store conversation histories for each session
conversation_histories = {}

# Load fine-tuned LLaMA model and tokenizer for answering queries
cache_dir = "./model_cache"
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="ishanarang/lora_model_it_updated",  # Pretrained model identifier
    load_in_4bit=True,  # Load model in 4-bit precision to save memory
    device_map=DEVICE,  # Map model to specified GPU
    cache_dir=cache_dir  # Cache model files locally
)
model = model.to(DEVICE).eval()  # Move model to GPU and set to evaluation mode

# Dictionary mapping subject abbreviations to full names
SUBJECT_MAPPING = {
    "ss": "socialscience",
    "english": "english",
    "mathematics": "mathematics",
    "science": "science",
    "physics": "physics",
    "chemistry": "chemistry",
    "biology": "biology",
    "history": "history",
    "geography": "geography"
}

# Predefined template questions for science subject to guide users
TEMPLATE_QUESTIONS = {
    'science': [
        {'id': 1, 'question': 'Can you explain the concept of photosynthesis?', 'icon': 'leaf', 'category': 'Biology'},
        {'id': 2, 'question': "What are Newton's three laws of motion?", 'icon': 'move', 'category': 'Physics'},
        {'id': 3, 'question': "How do chemical reactions work?", 'icon': 'flask-conical', 'category': 'Chemistry'},
        {'id': 4, 'question': "Can you help me solve quadratic equations?", 'icon': 'square-equal', 'category': 'Mathematics'}
    ]
}

def get_csv_path(class_name, subject_name):
    """Generate path to CSV file containing chapter data for a class and subject."""
    subject_name = SUBJECT_MAPPING.get(subject_name.lower(), subject_name.lower())
    return f"static/theory_data/{class_name}/chapter_{subject_name}.csv"

def truncate_answer(answer):
    """Truncate answer at the last full stop to ensure complete sentences."""
    last_full_stop = answer.rfind(".")
    return answer[:last_full_stop + 1] if last_full_stop != -1 else answer

def format_markdown_to_html(text):
    """Convert markdown text to HTML for better frontend rendering."""
    return markdown.markdown(text, extensions=["fenced_code", "tables"])

def handle_greetings(user_query):
    """Handle common greeting queries with predefined responses."""
    greetings = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! What would you like to know?",
        "who are you": "I'm a helpful AI assistant here to answer your questions.",
        "how are you": "I'm just a program, but thanks for asking! How can I help you?"
    }
    return greetings.get(user_query.lower(), None)

@app.route("/upload_query", methods=["POST"])
def upload_query():
    """Handle user queries, generate answers using LLaMA model, and maintain conversation history."""
    app.logger.info("upload_query endpoint called.")
    try:
        data = request.get_json()
        app.logger.debug(f"Request data: {data}")

        # Validate request data
        if not data or not all(k in data for k in ("query", "class", "subject")):
            app.logger.warning("Invalid request: Missing required fields")
            return jsonify({"error": "Invalid request data"}), 400

        user_query = data["query"].strip()
        if not user_query:
            app.logger.warning("Empty query received")
            return jsonify({"error": "Query cannot be empty"}), 400

        class_name = data["class"]
        subject = data["subject"]
        session_id = data.get("session_id", "default_session")  # Use default session if not provided

        # Initialize conversation history for new session
        if session_id not in conversation_histories:
            conversation_histories[session_id] = []

        is_template = data.get('isTemplate', False)
        is_ocr = data.get('isOcr', False)
        if is_template:
            app.logger.info(f"Processing template question: {user_query}")
        if is_ocr:
            app.logger.info(f"Processing query with OCR text: {user_query}")

        # Handle greeting queries
        greeting_response = handle_greetings(user_query)
        if greeting_response:
            conversation_histories[session_id].append({
                "question": user_query,
                "answer": greeting_response
            })
            # Keep only last 5 exchanges to manage memory
            if len(conversation_histories[session_id]) > 5:
                conversation_histories[session_id].pop(0)
            return jsonify({"query": user_query, "answer": greeting_response, "session_id": session_id}), 200

        # Define paths for FAISS index and embeddings
        base_path = "/home/isha.narang/gurukul-ai/checking_embedding_models"
        index_filename = f"{class_name}_{subject}_faiss_index.bin"
        embedding_filename = f"{class_name}_{subject}_embeddings.pkl"
        global FAISS_INDEX_PATH, EMBEDDINGS_PATH, CSV_PATH
        FAISS_INDEX_PATH = os.path.join(base_path, index_filename)
        EMBEDDINGS_PATH = os.path.join(base_path, embedding_filename)
        CSV_PATH = f"/home/isha.narang/gurukul-ai/chapter_data/{class_name}/chapter_{subject}.csv"

        start_time = time.time()

        # Build conversation history context
        history_context = ""
        if conversation_histories[session_id]:
            history_context = "Previous conversation:\n"
            for i, qa_pair in enumerate(conversation_histories[session_id]):
                history_context += f"Q{i+1}: {qa_pair['question']}\n"
                history_context += f"A{i+1}: {qa_pair['answer']}\n\n"

        # Handle English subject queries differently
        if subject == "english":
            best_chapter_name, chapter_context = get_full_chapter_context(
                user_query,
                CSV_PATH=CSV_PATH,
                faiss_index_path=FAISS_INDEX_PATH,
                embeddings_path=EMBEDDINGS_PATH,
                top_k=5
            )
            prompt = f"""You are a helpful AI Assistant to help students with their questions. Given question by the student, context chunks, and previous conversation history, generate a well structured and in-detail answer to that question. Answer the question as if you are explaining the concept to the student. Keep the answer detailed.
            If the question refers to previous conversation, use that information in your answer. If the context is not relevant answer with your own knowledge. For forming a well structured answer add different paragraphs, bullet points, numbered list, etc whatever required.
            {history_context}
            Question: {user_query}
            Context:
            {chapter_context}
            Provide only the answer. Do not repeat the question or context."""

            # Tokenize input and generate answer
            inputs = tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}],
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(DEVICE)
            attention_mask = (inputs != tokenizer.pad_token_id).long()

            with torch.no_grad():
                output_ids = model.generate(
                    input_ids=inputs,
                    attention_mask=attention_mask,
                    max_new_tokens=1000,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    do_sample=False,
                    pad_token_id=tokenizer.pad_token_id
                )
            answer = tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True).strip()
            chapter_used = best_chapter_name
        else:
            # Generate answer for non-English subjects with history
            answer, chapter_used = generate_answer_with_history(user_query, FAISS_INDEX_PATH, EMBEDDINGS_PATH, conversation_histories[session_id])

        end_time = time.time()
        pdf_link = get_pdf_link(class_name, chapter_used) if chapter_used else None

        # Update conversation history
        conversation_histories[session_id].append({
            "question": user_query,
            "answer": answer
        })
        if len(conversation_histories[session_id]) > 5:
            conversation_histories[session_id].pop(0)

        time_taken = end_time - start_time
        app.logger.info(f"Time taken to generate answer: {time_taken:.2f} seconds")

        beautified_answer = format_markdown_to_html(answer)
        app.logger.debug(f"Generated response: {beautified_answer}")

        return jsonify({
            "query": user_query,
            "answer": beautified_answer,
            "session_id": session_id,
            "pdf_link": pdf_link,
        }), 200

    except Exception as e:
        app.logger.error(f"Error processing query: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500

def generate_answer_with_history(query, faiss_index_path, embeddings_path, conversation_history):
    """Generate answer using FAISS search and conversation history."""
    retrieved_chunks = search_faiss(query, faiss_index_path, embeddings_path, top_k=2)
    if not retrieved_chunks:
        return "No relevant context found.", None
    top_chapter_id = retrieved_chunks[0]["chapter_id"]
    context_str = "\n\n".join([f"{i+1}. {chunk[:500]}" for i, (_, chunk) in enumerate(retrieved_chunks)])

    # Format conversation history for prompt
    history_context = ""
    if conversation_history:
        history_context = "Previous conversation:\n"
        for i, qa_pair in enumerate(conversation_history):
            history_context += f"Q{i+1}: {qa_pair['question']}\n"
            history_context += f"A{i+1}: {qa_pair['answer']}\n\n"

    prompt = f"""You are a kind and engaging AI tutor. Your goal is to help students understand academic concepts clearly and with context.
            Given the user's question, past conversation, and context chunks from the textbook, do the following:
            - Provide a structured, in-detail and friendly explanation
            - Break it into paragraphs
            - Use bullet points, examples, or analogies if helpful
            - Emphasize clarity over verbosity
            - Generate answer as if you are explaining the concept to the student in detail
        Question: {query}
        Relevant Chapter Contexts:
        {context_str}
        Provide only the answer. Do not repeat the question or context.
        Here are the past conversation between user and model:\n{history_context}
        If the current question is related to the history, use that information in your answer. If not, answer with your own knowledge and ignore the previous conversation."""

    inputs = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(DEVICE)

    try:
        with torch.no_grad():
            output_ids = model.generate(
                input_ids=inputs,
                max_new_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
        answer = tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True).strip()

        # Check for repetitive output and retry if necessary
        for _ in range(2):
            words = answer.split()
            if len(set(words)) >= 10:
                break
            print("⚠️ Detected repetitive output. Retrying...")
        else:
            return "Answer generation failed due to repetition.", None

        if "assistant" in answer.lower():
            answer = answer.split("assistant", 1)[-1].strip()

        return answer, top_chapter_id
    except RuntimeError as e:
        print(f"Error: {e}")
        return "Error during answer generation.", None

@app.route("/conversation_history", methods=["GET", "POST", "DELETE"])
def manage_conversation_history():
    """Manage conversation history for a session (get, create/reset, or delete)."""
    try:
        session_id = request.args.get("session_id", "default_session")
        
        if request.method == "GET":
            return jsonify({"history": conversation_histories.get(session_id, [])}), 200
        elif request.method == "POST":
            conversation_histories[session_id] = []
            return jsonify({"message": "Session created/reset successfully", "session_id": session_id}), 200
        elif request.method == "DELETE":
            if session_id in conversation_histories:
                del conversation_histories[session_id]
            return jsonify({"message": "Session deleted successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error managing conversation history: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/generate_suggestions", methods=["POST"])
def generate_suggestions():
    """Generate follow-up questions based on a question and answer to deepen understanding."""
    app.logger.info("generate_suggestions endpoint called.")
    try:
        data = request.get_json()
        app.logger.debug(f"Request data: {data}")

        if not data or not all(k in data for k in ("question", "answer", "class", "subject")):
            app.logger.warning("Invalid request: Missing required fields")
            return jsonify({"error": "Invalid request data"}), 400

        question = data["question"].strip()
        answer = data["answer"].strip()
        class_name = data["class"]
        subject = data["subject"]

        # Create prompt for generating follow-up questions
        prompt = f"""Based on the following question and answer, generate THREE concise, specific follow-up questions that would help the student deepen their understanding of the topic. 
        Each question should be short (max 15 words), directly related to the original question, and encourage exploration of related concepts.
        Original Question: {question}
        Answer: {answer}
        Return ONLY the three questions as a list, with no numbering, explanations, or extra text."""

        inputs = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(DEVICE)
        attention_mask = (inputs != tokenizer.pad_token_id).long()

        with torch.no_grad():
            output_ids = model.generate(
                input_ids=inputs,
                attention_mask=attention_mask,
                max_new_tokens=200,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id
            )

        generated_text = tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True).strip()

        # Extract questions from generated text
        questions = []
        for line in generated_text.split('\n'):
            line = line.strip()
            if line and not line.startswith(('1.', '2.', '3.')):
                if line[0].isdigit() and line[1:3] in ['. ', ') ']:
                    line = line[3:].strip()
                questions.append(line)

        # Ensure exactly 3 questions
        if len(questions) < 3:
            generic_questions = [
                f"Can you explain more about {subject.lower()} concepts related to this?",
                f"What are practical applications of this in {subject.lower()}?",
                f"How does this relate to other topics in {class_name}?"
            ]
            questions.extend(generic_questions[:3-len(questions)])
        questions = questions[:3]

        return jsonify({"suggestions": questions}), 200
    except Exception as e:
        app.logger.error(f"Error generating suggestions: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Internal server error"}), 500

def load_user_history(user_name):
    """Load user response history from a JSON file, filtering valid entries."""
    file_path = os.path.join("user_responses", f"{user_name}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                history = json.load(f)
            # Filter valid entries for MCQ or theory responses
            valid_history = [
                entry for entry in history
                if isinstance(entry, dict) and 'question' in entry and 'type' in entry and (
                    (entry['type'] == 'mcq' and 'selected' in entry and 'is_correct' in entry) or
                    (entry['type'] == 'theory' and 'user_answer' in entry)
                )
            ]
            if len(valid_history) < len(history):
                app.logger.warning(f"Filtered out {len(history) - len(valid_history)} invalid history entries for {user_name}")
            return valid_history
        except Exception as e:
            app.logger.error(f"Error loading user history for {user_name}: {str(e)}")
            return []
    return []

def extract_json_from_text(text):
    """Extract JSON array from text, handling common formatting issues."""
    json_match = re.search(r'\[\s*{.*}\s*\]', text, re.DOTALL)
    if json_match:
        json_text = json_match.group(0)
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            pass

    code_blocks = re.findall(r'```(?:json)?(.*?)```', text, re.DOTALL)
    for block in code_blocks:
        try:
            return json.loads(block.strip())
        except json.JSONDecodeError:
            continue

    try:
        cleaned = re.sub(r"'", '"', text)
        cleaned = re.sub(r"(\w+):", r'"\1":', cleaned)
        potential_json = re.search(r'\[\s*{.*}\s*\]', cleaned, re.DOTALL)
        if potential_json:
            return json.loads(potential_json.group(0))
    except:
        pass
    return None

def generate_mcqs_from_chapter(class_name, subject_name, chapter_id, user_history, model, tokenizer, device="cuda:0"):
    """Generate 5 personalized MCQs based on chapter content and user history."""
    class_map = {
        "1": "class-9",
        "2": "class-10",
        "3": "class-11",
        "4": "class-12"
    }
    class_name = class_map.get(str(class_name), str(class_name))

    csv_path = f"/home/isha.narang/gurukul-ai/chapter_data/{class_name}/chapter_{subject_name}.csv"
    df = pd.read_csv(csv_path)

    row = df[df['chapter_name'] == chapter_id]
    if row.empty:
        return {"error": "Chapter not found in CSV."}

    chapter_context = row.iloc[0]['content']
    
    history_context = ""
    for i, entry in enumerate(user_history[-5:]):
        history_context += f"Q{i+1}: {entry['question']}\nA{i+1}: {entry['answer']}\n\n"

    prompt = f"""
You are a kind and creative AI tutor. Generate 5 personalized MCQs from the following chapter content and user history.
Each MCQ must be:
- A question related to the chapter
- 4 answer options
- One correct index (0–3)
VERY IMPORTANT:
- Your ENTIRE output must ONLY be a valid JSON array
- Do NOT add any extra text, explanations, markdown, or commentary
Example Output Format:
[
  {{
    "question": "....",
    "options": ["A", "B", "C", "D"],
    "correct": 2
  }},
  ...
]
Chapter Content:
{chapter_context[:1500]}
User History:
{history_context}
"""

    inputs = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=inputs,
            max_new_tokens=800,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    answer = tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True).strip()

    try:
        mcqs = json.loads(answer)
        return mcqs
    except json.JSONDecodeError:
        mcqs = extract_json_from_text(answer)
        if mcqs:
            return mcqs
        else:
            return {"raw_output": answer, "error": "Could not parse MCQs — check formatting"}

def generate_mcqs_with_history(class_name, subject_name, chapter_id, user_name, model, tokenizer, device="cuda:0"):
    """Generate MCQs with user history, retrying on failure with adjusted parameters."""
    if class_name.startswith("class") and not class_name.startswith("class-"):
        class_name = class_name.replace("class", "class-")

    csv_path = f"/home/isha.narang/gurukul-ai/chapter_data/{class_name}/chapter_{subject_name}.csv"
    if not os.path.exists(csv_path):
        return {"error": f"CSV not found for {class_name} - {subject_name}"}

    df = pd.read_csv(csv_path)
    row = df[df['chapter_name'].str.strip() == chapter_id.strip()]
    if row.empty:
        return {"error": f"Chapter '{chapter_id}' not found in CSV."}

    chapter_context = row.iloc[0]['content']
    user_history = load_user_history(user_name)

    history_context = ""
    for i, entry in enumerate(user_history[-5:]):
        if 'type' in entry and entry['type'] == 'mcq' and 'selected' in entry:
            history_context += f"Q{i+1}: {entry.get('question', '')}\nA{i+1}: {entry['selected']}\n\n"
        elif 'type' in entry and entry['type'] == 'theory' and 'user_answer' in entry:
            history_context += f"Q{i+1}: {entry.get('question', '')}\nA{i+1}: {entry.get('user_answer', '')}\n\n"
        else:
            print(f"Skipping history entry with missing or invalid fields: {entry}")
            continue

    prompt = f"""
You are a kind and creative AI tutor. Generate 5 personalized MCQs from the following chapter content and user history.
Each MCQ must be:
- A question related to the chapter
- 4 answer options
- One correct index (0–3)
VERY IMPORTANT:
- Your ENTIRE output must ONLY be a valid JSON array
- Do NOT add any extra text, explanations, markdown, or commentary
Example Output Format:
[
  {{
    "question": "....",
    "options": ["A", "B", "C", "D"],
    "correct": 2
  }},
  ...
]
Chapter Content:
{chapter_context[:1500]}
User History:
{history_context}
"""

    inputs = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=inputs,
            max_new_tokens=800,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )
    answer = tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True).strip()

    try:
        mcqs = json.loads(answer)
        return mcqs
    except json.JSONDecodeError:
        mcqs = extract_json_from_text(answer)
        if mcqs:
            return mcqs
        else:
            print("⚠️ Bad MCQ output. Retrying generation with different settings...")
            with torch.no_grad():
                output_ids = model.generate(
                    input_ids=inputs,
                    max_new_tokens=800,
                    temperature=0.3,
                    top_p=0.8,
                    repetition_penalty=1.1,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id
                )
            retry_answer = tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True).strip()
            try:
                retry_mcqs = json.loads(retry_answer)
                return retry_mcqs
            except json.JSONDecodeError:
                retry_mcqs = extract_json_from_text(retry_answer)
                if retry_mcqs:
                    return retry_mcqs
                else:
                    return {"raw_output": answer, "error": "Could not parse MCQs after retry"}

@app.route("/practice/get_questions/<chapter_id>", methods=["GET"])
def get_questions_with_history(chapter_id):
    """Fetch MCQs for a chapter, personalized with user history."""
    user = request.args.get("user")
    class_name = request.args.get("class")
    subject_name = request.args.get("subject")

    if not all([user, class_name, subject_name, chapter_id]):
        return jsonify({"error": "Missing one or more query parameters"}), 400

    mcqs = generate_mcqs_with_history(
        class_name=class_name,
        subject_name=subject_name,
        chapter_id=chapter_id,
        user_name=user,
        model=model,
        tokenizer=tokenizer,
        device="cuda:0"
    )

    if isinstance(mcqs, list):
        for i, q in enumerate(mcqs):
            q["id"] = f"{chapter_id}_{i}"
            q["text"] = q.get("question", "")
            q.pop("question", None)
        app.logger.info(f"Generated {len(mcqs)} MCQs for chapter {chapter_id}")
        try:
            safe_mcqs = json.loads(json.dumps(mcqs))
            return jsonify(safe_mcqs)
        except Exception as e:
            print("❌ JSON serialization failed:", e)
            return jsonify({"error": "Serialization error", "details": str(e)}), 500
    else:
        app.logger.error(f"MCQ generation failed: {mcqs}")
        return jsonify({"error": "Failed to generate MCQs", "details": str(mcqs.get("error", "Unknown error"))}), 500

@app.route("/evaluate_theory", methods=["POST"])
def evaluate_theory():
    """Evaluate a student's theory answer and provide feedback."""
    data = request.get_json()
    question = data.get("question")
    answer = data.get("answer")
    expected = data.get("expected")

    if not all([question, answer, expected]):
        return jsonify({"error": "Missing required fields"}), 400

    prompt = f"""
You are an experienced teacher. The student has written an answer to the following question.
**Question:** {question}
**Student's Answer:** {answer}
**Expected Answer:** {expected}
Now, as a teacher:
- Evaluate the student's answer.
- Highlight strengths and weaknesses.
- Point out any missing points.
- Suggest improvements if needed.
Be constructive, detailed, and supportive. Provide a complete paragraph as feedback.
"""

    inputs = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(DEVICE)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=inputs,
            max_new_tokens=500,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    feedback = tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True).strip()
    return jsonify({"feedback": feedback})

@app.route("/practice/submit_answer", methods=["POST"])
@app.route("/gurukulai/practice/submit_answer", methods=["POST"])
def submit_answer():
    """Save a user's MCQ response to their history file."""
    try:
        data = request.get_json()
        app.logger.info(f"Received submit_answer request: {data}")
        
        if not all(k in data for k in ["user", "question_id", "selected", "is_correct"]):
            app.logger.warning(f"Missing required fields in submit_answer: {data}")
            return jsonify({"error": "Missing required fields", "received": data}), 400
            
        user_name = data["user"]
        question_id = data["question_id"]
        selected = data["selected"]
        is_correct = data["is_correct"]
        
        file_path = os.path.join("user_responses", f"{user_name}.json")
        app.logger.info(f"Saving MCQ response for user {user_name} to {file_path}")
        
        history = []
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                history = json.load(f)
            
        history.append({
            "timestamp": time.time(),
            "question": question_id,
            "selected": selected,
            "is_correct": is_correct,
            "type": "mcq"
        })
        
        with open(file_path, "w") as f:
            json.dump(history, f, indent=2)
            
        app.logger.info(f"Successfully saved MCQ response for {user_name}")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        app.logger.error(f"Error saving answer: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Failed to save answer", "details": str(e)}), 500

@app.route("/gurukulai/practice/submit_theory_answer", methods=["POST"])
@app.route("/practice/submit_theory_answer", methods=["POST"])
def submit_theory_answer():
    """Save and evaluate a user's theory answer, returning feedback and a rating."""
    try:
        data = request.get_json()
        
        if not all(k in data for k in ["user", "question_id", "user_answer", "expected_answer", "question_text"]):
            app.logger.warning(f"Missing required fields in submit_theory_answer: {data}")
            return jsonify({"error": "Missing required fields"}), 400
            
        user_name = data["user"]
        question_id = data["question_id"]
        user_answer = data["user_answer"]
        expected_answer = data["expected_answer"]
        question_text = data["question_text"]
        
        file_path = os.path.join("user_responses", f"{user_name}.json")
        
        history = []
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                history = json.load(f)
            
        history.append({
            "timestamp": time.time(),
            "question": question_id,
            "user_answer": user_answer,
            "type": "theory"
        })
        
        with open(file_path, "w") as f:
            json.dump(history, f)
        
        prompt = f"""
You are an experienced teacher tasked with evaluating a student's answer to a question. Your response must include two parts: a rating and detailed feedback.
**Question:** {question_text}
**Student's Answer:** {user_answer}
**Expected Answer:** {expected_answer}
As a teacher, provide:
1. A rating out of 10 on the first line, formatted as "Rating: X/10"
2. A detailed paragraph (at least 3-5 sentences) of constructive feedback that:
   - Highlights what the student got right
   - Identifies specific concepts they missed or misunderstood
   - Suggests clear improvements for their answer
   - Provides additional information to enhance their understanding
   - Uses a friendly and supportive tone
**Important**: 
- Always generate both the rating and the feedback paragraph
- Do not include any extra text, markdown, or explanations outside the rating and feedback paragraph
Example Output:
Rating: 8/10
The student's answer correctly identifies the main theme of the narrative but misses the role of symbolism...
"""
        
        inputs = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(DEVICE)

        with torch.no_grad():
            output_ids = model.generate(
                input_ids=inputs,
                max_new_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )

        feedback = tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True).strip()
        app.logger.debug(f"Raw model output: {feedback}")
        rating_match = re.search(r'Rating:\s*(\d+)/10', feedback)
        rating = int(rating_match.group(1)) if rating_match else None
            
        return jsonify({
            "feedback": feedback,
            "rating": rating,
            "success": True
        }), 200
    except Exception as e:
        app.logger.error(f"Error processing theory answer: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Failed to process answer", "details": str(e)}), 500

@app.route("/debug")
def debug():
    """Simple endpoint to check if the backend is running."""
    return jsonify({"status": "Backend is running"})

@app.route("/practice/get_theory_questions/<chapter_id>", methods=["GET"])
@app.route("/gurukulai/practice/get_theory_questions/<chapter_id>", methods=["GET"])
def get_theory_questions_route(chapter_id):
    """Fetch theory questions for a chapter, personalized with user history."""
    app.logger.info(f"Route hit: get_theory_questions({chapter_id})")
    user = request.args.get("user")
    class_name = request.args.get("class")
    subject_name = request.args.get("subject")

    if not all([user, class_name, subject_name, chapter_id]):
        app.logger.warning(f"Missing query parameters: user={user}, class={class_name}, subject={subject_name}, chapter={chapter_id}")
        return jsonify({"error": "Missing query parameters"}), 400

    try:
        questions = generate_theory_questions(
            class_name=class_name,
            subject_name=subject_name,
            chapter_id=chapter_id,
            user_name=user,
            model=model,
            tokenizer=tokenizer,
            device=DEVICE
        )

        if isinstance(questions, list):
            for i, q in enumerate(questions):
                q["id"] = f"theory_{chapter_id}_{i}"
            app.logger.info(f"Generated {len(questions)} theory questions for chapter {chapter_id}")
            return jsonify(questions), 200
        else:
            app.logger.error(f"Theory question generation failed: {questions}")
            return jsonify({"error": "Failed to generate theory questions", "details": questions.get("error", "Unknown error")}), 500
    except Exception as e:
        app.logger.error(f"Error reading theory questions: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": "Could not read theory questions", "details": str(e)}), 500

def generate_fallback_questions(content):
    """Generate fallback theory questions when model generation fails."""
    content_preview = content[:200].replace('"', "'")
    return [
        {
            "id": "theory_fallback_1",
            "question": f"Explain the main ideas presented in this chapter: '{content_preview}...'",
            "answer": "The main ideas include understanding the core concepts, their applications, and the significance in the broader context."
        },
        {
            "id": "theory_fallback_2",
            "question": "What are the key takeaways from this chapter?",
            "answer": "The key takeaways include understanding the fundamental principles, their practical applications, and how they relate to other concepts."
        },
        {
            "id": "theory_fallback_3",
            "question": "How would you summarize this chapter in your own words?",
            "answer": "A good summary would include the main topics covered, key concepts introduced, and their significance."
        }
    ]

def generate_theory_questions(class_name, subject_name, chapter_id, user_name, model, tokenizer, device="cuda:0"):
    """Generate theory questions with expected answers based on chapter content and user history."""
    print(f"Generating theory questions for: Class={class_name}, Subject={subject_name}, Chapter={chapter_id}")
    
    if class_name.startswith("class") and not class_name.startswith("class-"):
        class_name = class_name.replace("class", "class-")
    
    csv_path = get_csv_path(class_name, subject_name)
    print(f"Looking for CSV at: {csv_path}")
    
    if not os.path.exists(csv_path):
        return {"error": f"CSV not found for {class_name} - {subject_name}"}

    try:
        df = pd.read_csv(csv_path)
        print(f"CSV loaded, columns: {df.columns.tolist()}")
        
        if 'chapter_name' not in df.columns:
            chapter_col = None
            for col in df.columns:
                if 'chapter' in col.lower():
                    chapter_col = col
                    break
            if chapter_col:
                df['chapter_name'] = df[chapter_col]
            else:
                return {"error": f"CSV format error: 'chapter_name' column not found in {csv_path}"}
        
        df['chapter_name_lower'] = df['chapter_name'].str.strip().str.lower()
        chapter_id_lower = chapter_id.strip().lower()
        row = df[df['chapter_name_lower'] == chapter_id_lower]
        
        if row.empty:
            for idx, r in df.iterrows():
                if chapter_id_lower in r['chapter_name_lower'] or r['chapter_name_lower'] in chapter_id_lower:
                    row = df.iloc[[idx]]
                    break
        
        if row.empty and not df.empty:
            print(f"Chapter '{chapter_id}' not found, using first chapter instead")
            row = df.iloc[[0]]

        if row.empty:
            return {"error": f"Chapter '{chapter_id}' not found in CSV."}

        content_col = 'content'
        if content_col not in df.columns:
            for col in df.columns:
                if col.lower() in ['text', 'description', 'chapter_content', 'lesson']:
                    content_col = col
                    break
            if content_col not in df.columns and len(df.columns) > 1:
                content_col = df.columns[1]
        
        chapter_context = row.iloc[0][content_col]
        print(f"Found chapter: {row.iloc[0]['chapter_name']}, content length: {len(chapter_context)}")
        
        user_history = load_user_history(user_name)
        history_context = ""
        for i, entry in enumerate(user_history[-5:]):
            history_context += f"Q{i+1}: {entry.get('question', '')}\nA{i+1}: {entry.get('user_answer', entry.get('selected', ''))}\n\n"

        chapter_context = re.sub(r'[\x00-\x1F\x7F]', ' ', chapter_context[:1000])
        history_context = re.sub(r'[\x00-\x1F\x7F]', ' ', history_context)

        prompt = f"""
You are a kind and creative AI tutor. Generate 5 theoretical questions with expected answers based on the following chapter content and user history.
Each question must:
- Be a long-form, open-ended question related to the chapter
- Include an expected answer (a detailed response)
- Be formatted as a JSON object with 'id', 'question', and 'answer' fields
VERY IMPORTANT:
- Your ENTIRE output must ONLY be a valid JSON array
- Do NOT add any extra text, explanations, markdown, or commentary
- Only the JSON array
- Do NOT include any control characters in the output
- Make sure all quotes are properly escaped
- Ensure the output is valid JSON that can be parsed without errors
Example Output Format:
[
  {{
    "id": "theory_1",
    "question": "Explain the significance of photosynthesis.",
    "answer": "Photosynthesis is the process by which plants convert sunlight into energy."
  }}
]
Chapter Content:
{chapter_context}
User History:
{history_context}
"""

        print("Generating questions using model...")
        inputs = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(device)

        with torch.no_grad():
            output_ids = model.generate(
                input_ids=inputs,
                max_new_tokens=1000,
                temperature=0.3,
                top_p=0.8,
                repetition_penalty=1.2,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )

        answer = tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True).strip()
        print(f"Raw model output: {answer[:200]}...")

        answer = re.sub(r'[\x00-\x1F\x7F]', ' ', answer)
        answer = answer.replace('\r\n', '\n').replace('\r', '\n')

        try:
            questions = json.loads(answer)
            print(f"Successfully parsed JSON, questions: {len(questions)}")
            return questions
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            questions = extract_json_from_text_theory(answer)
            if questions:
                print(f"Successfully extracted JSON, questions: {len(questions)}")
                return questions
            else:
                print(f"Failed to extract questions from: {answer[:100]}...")
                return generate_fallback_questions(chapter_context)
                
    except Exception as e:
        print(f"Error in generate_theory_questions: {e}")
        traceback.print_exc()
        return {"error": f"Failed to generate questions: {str(e)}"}

def extract_json_from_text_theory(text):
    """Extract JSON array from text, handling control characters and formatting issues."""
    text = re.sub(r'[\x00-\x1F\x7F]', ' ', text)
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    json_array_match = re.search(r'\[\s*{[\s\S]*}\s*\]', text)
    if json_array_match:
        json_str = json_array_match.group(0)
        json_str = json_str.replace('"', '"').replace('"', '"')
        json_str = re.sub(r'\\(?![\\nrtbf"])', r'\\', json_str)
        json_str = re.sub(r'"\s*,', r'",', json_str)
        json_str = re.sub(r',\s*]', r']', json_str)
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Failed to parse extracted JSON: {e}, JSON string: {json_str[:200]}...")

    try:
        text = re.sub(r"'", '"', text)
        text = re.sub(r'(\w+):', r'"\1":', text)
        text = re.sub(r',\s*}', r'}', text)
        text = re.sub(r',\s*]', r']', text)
        
        json_array_match = re.search(r'\[\s*{[\s\S]*}\s*\]', text)
        if json_array_match:
            json_str = json_array_match.group(0)
            return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to parse after fixing common issues: {e}")

    try:
        start_idx = text.find('[')
        if start_idx != -1:
            bracket_count = 1
            end_idx = -1
            for i in range(start_idx + 1, len(text)):
                if text[i] == '[':
                    bracket_count += 1
                elif text[i] == ']':
                    bracket_count -= 1
                if bracket_count == 0:
                    end_idx = i
                    break
            if end_idx != -1:
                json_str = text[start_idx:end_idx + 1]
                json_str = re.sub(r'[\x00-\x1F\x7F]', ' ', json_str)
                json_str = json_str.replace('"', '"').replace('"', '"')
                return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to parse after manual extraction: {e}")
    
    return None

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint to confirm API is running."""
    return jsonify({"status": "API is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3223, debug=True)
