<div align="center">
  
# 🎬 CineBot
### Advanced Semantic AI Movie Recommendation Engine
  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey.svg?style=for-the-badge&logo=flask&logoColor=black)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg?style=for-the-badge&logo=huggingface&logoColor=black)
![FAISS](https://img.shields.io/badge/Meta-FAISS-blue.svg?style=for-the-badge&logo=meta&logoColor=white)

**Project By / Designed By:** Nikita Wagh  
**Developed By:** TE AIML Students

</div>



## 📖 Overview

**CineBot** is a state-of-the-art cinematic conversational agent built entirely on modern **Retrieval-Augmented Generation (RAG)** architecture. It goes beyond simple keyword matching and understands *human context*, meaning, and abstract emotional vibes using cutting-edge Natural Language Processing.

Featuring a fully bespoke **Glassmorphic Light/Dark User Interface**, it delivers a premium desktop-class web application experience natively through standard HTML/CSS.

## ✨ Core Architecture

- **Contextual Semantic Matching:** Replaced legacy TF-IDF matrices with deep `Sentence Transformers` (`all-MiniLM-L6-v2`) which mathematically translates entire movie plots, tags, and titles into dense meaning vectors.
- **Lightning-Fast Vector Databases:** Utilizes **Facebook AI Similarity Search (FAISS)**, allowing the engine to search 10,000+ movie embeddings natively on the CPU in under 5 milliseconds.
- **Organic Heuristic Re-ranking:** Automatically mathematically penalizes horrible movies and aggressively promotes high-quality films that match your exact query using average rating boosts.
- **Conversational LLM:** Integrates Google's `flan-t5` language model as an enthusiastic conversational agent that parses intents, naturally greets the user, and presents the FAISS semantic calculations natively.
- **Zero-Dependency Styling Engine:** Features an aggressively beautiful multi-layered background with morphing dynamic grid-mesh shapes and perfectly engineered CSS variables to support robust local-storage persistent **Dark and Light Modes**.



## ⚙️ How It Works Internally

1. **The Vector Knowledge Base (`train_model.py`)**  
   The pipeline aggregates thousands of movies with their massive user metadata tags (`tags.csv`), their average ratings (`ratings.csv`), and their core information (`movies.csv`). It encodes them into dense embedding floats natively using `all-MiniLM-L6-v2`. This creates a massive 384-dimensional mathematical universe of movies stored locally as a lightning-fast `faiss_index.bin` database.

2. **The Recommendation Search (`recommender.py`)**  
   When a user asks for *"a devastating emotional sci-fi"*, the engine rapidly translates that small sentence into mathematics and fires it into the FAISS L2 memory lookup. It yanks out the closest contextual points rather than relying on exact word overlaps, ensuring phenomenal thematic intelligence.

3. **The Interactive AI Layer (`app.py`)**  
   First, an **Intent Router** gracefully intercepts standard human greetings (e.g. *"Hi"*, *"How are you?"*, *"Who are you?"*). It bypasses the movie engine completely for these to act as a realistic, friendly Assistant. For genuine movie requests, the FAISS results are securely injected into a carefully constrained `FLAN-T5` prompt layout that mimics the persona of a professional film critic!


## 🚀 How to Run and Execute the Project

Follow these exact steps to clone the project, build the Machine Learning engine, and launch the Web Application.

### Step 1. Clone the Repository
Download the project code natively from GitHub onto your machine:
```bash
git clone https://github.com/manoj-chavan-13/MV_CT.git
cd MV_CT
```

### Step 2. Setup Your Python Environment
Ensure you have Python 3.8+ installed on your local machine. It is deeply recommended to use a clean virtual environment to securely hold the Machine Learning packages.
```bash
# Initialize a Virtual Environment (Windows)
python -m venv venv

# Activate the Virtual Environment
venv\Scripts\activate
```

### Step 3. Install Dependencies
Download PyTorch, Flask, FAISS, Sentence-Transformers, and all required libraries:
```bash
pip install -r requirements.txt
```

### Step 4. Build the Semantic Vector Engine
Before starting the chatbot, you **MUST** encode the dataset `.csv` rows into the super-fast FAISS index engine! 
```bash
python model/train_model.py
```
> **Important Note:** The `all-MiniLM-L6-v2` embedding model will download locally (approx. 80MB) and crunch the strings into mathematics. Depending on your CPU, this building process will generally take about *40 seconds to 1 minute*. 

### Step 5. Boot the Neural Flask Server
Once the `faiss_index.bin` finishes building inside the `model/` folder, you can launch the actual Web application:
```bash
python app.py
```
> *The Google FLAN-T5 Large Language Model will quickly initialize and dynamically mount to your memory. You can access the stunning UI simply by opening `http://127.0.0.1:5000` in your browser!*



## 👤 Credits & Authors

* **Project Designed By:** Nikita Wagh (Frontend, Web Application, UI/UX Glassmorphism & Aesthetics)
* **Developed By:** TE AIML Students (Backend Vector Logic, System Pipeline, and Neural Architecture)
