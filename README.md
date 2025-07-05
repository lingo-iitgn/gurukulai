# 📘 GurukulAI: Curriculum-Aligned Generative QA Platform for Indian School Students

*GurukulAI* is an open-source, AI-powered educational platform designed to assist students in the Indian school system with NCERT-aligned question answering. It features a fine-tuned LLaMA 3.1 8B model integrated into a Retrieval-Augmented Generation (RAG) pipeline, enabling students to ask questions, practice MCQs, and get chapter-specific answers.

---

## 📝 Dataset Summary

- *Languages:* English, Hindi  
- *Tags:* education, ncert, rag, qa-dataset, bilingual, india
- *Size:* 18k+ Question–Answer–Context triples  
- *License:* [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
- *Access:* [HuggingFace Dataset](https://huggingface.co/datasets/LingoIITGN/Gurukul)
  
Note: NCERT textbook content is used under fair-use provisions for non-commercial, educational research purposes.

---

## 💻 Platform Features

- 🗣️ *Multilingual QA Chat*: Ask questions in English or Hindi  
- 📸 *Image-Based Doubt Resolution*: OCR-based query from handwritten text  
- 📄 *Source Grounding*: Chapter and context reference per response  
- 📝 *MCQ Generator*: Topic-based quiz generation and feedback  
- ✍️ *Theory Answer Evaluation*: LLM-suggested improvements  
- 🔁 *Follow-Up Learning*: Suggests next questions for practice  
- 🌐 *Try it here*: [GurukulAI Web App](https://lingo.iitgn.ac.in/gurukulai/)

---
## 📂 Repository Structure

<pre>
gurukul-ai/
├── backend/
│   ├── app.py
│   └── index_llama.py
│
└── frontend/
    ├── app.py
    ├── templates/
    │   └── index.html
    └── static/
        ├── css/
        │   └── style.css
        ├── js/
        │   └── script.js
        └── images/
            └── logo.png
</pre>


---
## 📄 License

This dataset and codebase are distributed under the *Creative Commons Attribution 4.0 International (CC BY 4.0)* license.

---

## 📣 Citation

```bibtex

  title     = {GurukulAI: An Interactive AI-Driven Educational Platform for Indian Education System},
  author    = {Isha Narang and Sneh Gosai and Mayank Singh},
  year      = {2025},
  note      = {Available at https://lingo.iitgn.ac.in/gurukulai/}
}
