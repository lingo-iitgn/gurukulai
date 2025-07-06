import os
import torch
import faiss
import pandas as pd
from transformers import AutoTokenizer, AutoModel
from unsloth import FastLanguageModel

# Set environment variable to control which GPUs are visible and their mapping
os.environ["CUDA_VISIBLE_DEVICES"] = "0,2"  # Makes physical GPU 1 appear as cuda:0
DEVICE = "cuda:0"  # Use first available GPU after environment variable setting

# Define cache directory for storing model files
cache_dir = "./model_cache"

# Load fine-tuned LLaMA model and tokenizer for answering queries
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="ishanarang/lora_model_it_updated",  # Pretrained model identifier
    load_in_4bit=True,  # Load model in 4-bit precision to save memory
    device_map=DEVICE,  # Map model to specified GPU
    cache_dir=cache_dir  # Cache model files locally
)
model = model.to(DEVICE).eval()  # Move model to GPU and set to evaluation mode

# Load separate embedding model and tokenizer for FAISS search
embedding_model = AutoModel.from_pretrained("BAAI/bge-m3").to(DEVICE).eval()  # Load BGE-M3 model for embeddings
embedding_tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")  # Tokenizer for embedding model

def get_full_chapter_context(query, CSV_PATH, faiss_index_path, embeddings_path, top_k=5):
    """Retrieve full chapter text based on the most relevant chunks for a query."""
    # Check if FAISS index and embeddings files exist
    if not os.path.exists(faiss_index_path) or not os.path.exists(embeddings_path):
        raise FileNotFoundError("⚠️ FAISS index or embeddings not found!")

    # Load FAISS index and text metadata (chapter_name, chunk)
    index = faiss.read_index(faiss_index_path)
    with open(embeddings_path, "rb") as f:
        texts = pickle.load(f)  # List of tuples: [(chapter_name, chunk)]

    # Embed the query using the BGE-M3 model
    inputs = embedding_tokenizer(query, return_tensors="pt", truncation=True).to(DEVICE)
    with torch.no_grad():
        outputs = embedding_model(**inputs)
        query_embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()  # Use CLS token embedding
    faiss.normalize_L2(query_embedding)  # Normalize embedding for FAISS search

    # Search for top_k most similar chunks
    distances, indices = index.search(query_embedding, top_k)
    
    # Identify the most frequent chapter among top chunks
    from collections import Counter
    matched_chapter_names = [texts[i][0] for i in indices[0]]
    chapter_scores = Counter(matched_chapter_names)
    best_chapter_name = chapter_scores.most_common(1)[0][0]

    print(f"📘 Most relevant chapter: {best_chapter_name}")

    # Load CSV and retrieve full chapter content
    df = pd.read_csv(CSV_PATH)
    full_chapter_text = df[df['name'] == best_chapter_name]['content'].values[0]

    return best_chapter_name, full_chapter_text

def search_faiss(query, faiss_index_path, embeddings_path, top_k=3):
    """Search FAISS index for top_k chunks most relevant to the query."""
    print("inside search faiss")
    # Verify existence of FAISS index and embeddings files
    if not (os.path.exists(faiss_index_path) and os.path.exists(embeddings_path)):
        print("⚠️ FAISS index not found! Run create_faiss_index() first.")
        return []

    # Load FAISS index and text metadata
    index = faiss.read_index(faiss_index_path)
    with open(embeddings_path, "rb") as f:
        texts = pickle.load(f)  # List of tuples: [(chapter_id, chunk_text)]

    # Tokenize and embed the query
    inputs = embedding_tokenizer(query, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = embedding_model(**inputs)
        query_embedding = outputs.last_hidden_state[:, 0, :].contiguous()  # Use CLS token embedding

    # Normalize embedding and search FAISS index
    query_embedding = query_embedding.cpu().numpy()
    faiss.normalize_L2(query_embedding)
    distances, indices = index.search(query_embedding, top_k)

    # Format results as list of dictionaries with chapter_id and chunk
    results = []
    for idx in indices[0]:
        if idx < len(texts):
            chapter_id, chunk_text = texts[idx]
            results.append({
                "chapter_id": chapter_id,
                "chunk": chunk_text
            })
    print("Results:", results)
    return results

def generate_answer(query, faiss_index_path, embeddings_path):
    """Generate an answer to a query using FAISS-retrieved context and LLaMA model."""
    # Retrieve relevant chunks using FAISS search
    retrieved_chunks = search_faiss(query, faiss_index_path, embeddings_path, top_k=2)
    if not retrieved_chunks:
        return "No relevant context found."

    # Format context for prompt
    context_str = "\n\n".join([f"{i+1}. {chunk[:500]}" for i, (_, chunk) in enumerate(retrieved_chunks)])

    # Create prompt with query and context
    prompt = f"""You are an AI Assistant to help students with their questions. Given question by the student and context chunks, generate a well structured answer to that question. If the context is not relevant answer with your own knowledge.
    Question: {query}
    Relevant Contexts:
    {context_str}
    Provide only the answer. Do not repeat the question or context."""

    # Tokenize prompt for LLaMA model
    inputs = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(DEVICE)

    try:
        # Generate answer using LLaMA model
        with torch.no_grad():
            output_ids = model.generate(
                input_ids=inputs,
                max_new_tokens=400,  # Limit output length
                temperature=0.7,  # Control randomness
                top_p=0.9,  # Nucleus sampling for diversity
                repetition_penalty=1.1,  # Penalize repetitive text
                do_sample=False,  # Use deterministic generation
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
            return "Answer generation failed due to repetition."

        # Clean up answer if it contains "assistant" marker
        if "assistant" in answer.lower():
            answer = answer.split("assistant", 1)[-1].strip()

        return answer
    except RuntimeError as e:
        print(f"Error: {e}")
        return "Error during answer generation."
