<div align="center">
  
# 🎬 CineBot
### Semantic AI Movie Recommendation Engine
  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey.svg?style=for-the-badge&logo=flask&logoColor=black)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg?style=for-the-badge&logo=huggingface&logoColor=black)
![FAISS](https://img.shields.io/badge/Meta-FAISS-blue.svg?style=for-the-badge&logo=meta&logoColor=white)

**Made by TE AIML students and Designed by NIKITA WAGH**

</div>

---

## 📖 Overview

**CineBot** is a state-of-the-art cinematic conversational agent built entirely on modern **Retrieval-Augmented Generation (RAG)** architecture. It goes beyond simple keyword matching and understands *human context*, meaning, and abstract emotional vibes using cutting-edge Natural Language Processing.

Featuring a fully bespoke **Glassmorphic Light/Dark User Interface**, it delivers a premium desktop-class web application experience natively through standard HTML/CSS.

## ✨ Core Architecture

- **Contextual Semantic Matching:** Replaced legacy TF-IDF matrices with deep `Sentence Transformers` (`all-MiniLM-L6-v2`) which mathematically translates entire movie plots, tags, and titles into dense meaning vectors.
- **Lightning-Fast Vector Databases:** Utilizes **Facebook AI Similarity Search (FAISS)**, allowing the engine to search 10,000+ movie embeddings natively on the CPU in under 5 milliseconds.
- **Organic Heuristic Re-ranking:** Automatically mathematically penalizes horrible movies and aggressively promotes high-quality films that match your exact query using average rating boosts.
- **Conversational LLM:** Integrates Google's `flan-t5` language model as an enthusiastic conversational agent that parses intents, naturally greets the user, and presents the FAISS semantic calculations natively.
- **Zero-Dependency Styling Engine:** Features an aggressively beautiful multi-layered background with morphing dynamic grid-mesh shapes and perfectly engineered CSS variables to support robust local-storage persistent **Dark and Light Modes**.

---

## 🛠️ Technology Stack

| Architecture Layer | Technology |
| :--- | :--- |
| **Backend API** | Python, Flask |
| **Vector Indexing (DB)** | FAISS (`faiss-cpu`) |
| **Embeddings Pipeline** | Sentence Transformers, Numpy, Pandas |
| **Language Generation** | Hugging Face `transformers`, PyTorch |
| **UI/UX Engineering** | HTML5, Advanced CSS3, Native ES6 JS, Phosphor Icons |

---

## ⚙️ How It Works Internally

### 1. The Vector Knowledge Base (`train_model.py`)
Because parsing massive text data in real-time is slow, the pipeline aggregates thousands of movies with their aggregated user metadata (`tags.csv`), and encodes them into dense embedding floats natively. This maps out a massive 384-dimensional mathematical universe of movies.

### 2. The Recommendation Search (`recommender.py`)
When a user asks for *"a devastating emotional sci-fi"*, the engine rapidly encodes that small sentence and fires it into the FAISS L2 memory lookup. It yanks out the closest contextual points rather than relying on exact word overlaps, ensuring phenomenal thematic intelligence.

### 3. The Interactive AI Layer (`app.py`)
Rather than risking hallucinations (asking the LLM to remember complex movie statistics), the FAISS results are safely injected into a carefully constrained `FLAN-T5` prompt layout that mimics the persona of a professional film critic.

---

## 🚀 Installation & Deployment

### 1. Pre-requisites
Ensure you have Python 3.8+ installed on your local machine.

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/cinebot.git
cd cinebot

# Initialize a Virtual Environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install all Machine Learning dependencies
pip install -r requirements.txt
```

### 3. Build the Vector Graph
Before starting the chatbot, you must encode the datasets into the FAISS memory engine.
```bash
python model/train_model.py
```
> **Note:** The `all-MiniLM-L6-v2` embedding model will download locally (approx. 80MB) and crunch the strings. It generally takes ~40 seconds on an average CPU.

### 4. Boot the Neural Server
```bash
python app.py
```
> The FLAN-T5 LLM will initialize and dynamically mount to your memory. You can access the stunning Web GUI simply by opening `http://127.0.0.1:5000` in your browser!

---

## 👤 Credits

* **Logic, Pipeline, and Neural Architecture:** TE AIML Students
* **Frontend, UI/UX Glassmorphism & Aesthetics:** Nikita Wagh 
