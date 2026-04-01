import faiss
import pickle
import numpy as np
import logging
import traceback
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_system():
    """Lazily loads the FAISS Vector Engine and Semantic models into memory."""
    try:
        logging.info("Loading Semantic Embeddings Model into memory...")
        # Since the model is global, this loads once into RAM
        mod = SentenceTransformer('all-MiniLM-L6-v2') 
        
        logging.info("Mounting FAISS Memory Vector Index...")
        idx = faiss.read_index("model/faiss_index.bin")
        
        with open("model/movie_data.pkl", "rb") as f:
            mo = pickle.load(f)
            
        logging.info("✅ Semantic Recommendation Engine Ready!")
        return mod, idx, mo
    except Exception:
        logging.error(f"Failed loading recommendation system. Run train script: {traceback.format_exc()}")
        return None, None, None

model, index, movies = load_system()

def recommend_movies(user_message, num=5):
    """
    Intelligent Retrieval-Augmented Generation (RAG) algorithm.
    Utilizes FAISS semantic searching against the meaning vector instead of raw text chunks. 
    It naturally manages both title specifications and vague sentiment intents alike.
    """
    if model is None or index is None or movies is None:
        return {"error": "Vector DB not loaded. Please ensure train_model.py was executed!"}

    try:
        # Encode user's message intent into math
        query_embedding = model.encode([user_message])
        
        # Pull 3x our final target length to allow quality rating re-ranking
        # L2 Distance means lower math values actually mean a 'closer' intent
        distances, indices = index.search(np.array(query_embedding, dtype=np.float32), num * 3)

        # Retrieve candidate rows via integer FAISS indexes
        candidates = movies.iloc[indices[0]].copy()
        
        # Calculate semantic hybrid score natively using the exact heuristic formula from the logic notebook
        # (1 / (1 + distance)) flips distance to a relevance scale so higher is better
        # + 0.3 * rating strongly pushes beloved movies to the top of equally matched semantic searches!
        candidates["score"] = (1 / (1 + distances[0])) + 0.3 * candidates["rating"]

        # Re-sort descending based on the powerful hybrid Score (FAISS Semantic Meaning + User Average Ratings)
        results = candidates.sort_values(by="score", ascending=False).head(num)

        # Format cleanly to pass back to the Chatbot Prompt Pipeline
        recs = []
        for _, row in results.iterrows():
            # Format to 1 decimal place cleanly for the UI
            rating_star = round(row["rating"], 1)
            recs.append(f"{row['title']} (⭐ {rating_star})")

        # The backend now considers every prompt universally a "Semantic Search", no more Item / Genre bifurcation.
        return {
            "type": "semantic",
            "matched": user_message[:50].strip() + ("..." if len(user_message) > 50 else ""),
            "recommendations": recs
        }
        
    except Exception as e:
        logging.error(f"RAG Error during recommendation generation: {traceback.format_exc()}")
        return {
            "type": "fallback",
            "matched": "Your Request",
            "recommendations": [f"{r['title']} (⭐ {round(r['rating'], 1)})" for _, r in movies.sample(num).iterrows()]
        }