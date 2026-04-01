import pandas as pd
import numpy as np
import faiss
import pickle
import logging
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def train_model():
    """
    Trains the recommendation engine using FAISS and SentenceTransformers 
    for pure semantic search based on titles, genres, and user tags,
    incorporating average ratings for boosting.
    """
    logging.info("Loading datasets...")
    try:
        movies = pd.read_csv("data/movies.csv")
        ratings = pd.read_csv("data/ratings.csv")
        tags = pd.read_csv("data/tags.csv")
    except FileNotFoundError as e:
        logging.error(f"Missing a dataset file: {e}")
        return

    logging.info("Merging tags into movies...")
    # Group tags by movie ID and join them with spaces
    tags_grouped = tags.groupby("movieId")["tag"].apply(lambda x: " ".join(x.astype(str))).reset_index()
    movies = movies.merge(tags_grouped, on="movieId", how="left")
    movies["tag"] = movies["tag"].fillna("")

    logging.info("Computing average ratings...")
    # Calculate each movie's mean rating
    avg_ratings = ratings.groupby("movieId")["rating"].mean().reset_index()
    movies = movies.merge(avg_ratings, on="movieId", how="left")
    movies["rating"] = movies["rating"].fillna(0.0)

    logging.info("Creating rich content metadata...")
    # Replace pipings in genres with spaces
    movies['genres'] = movies['genres'].str.replace('|', ' ', regex=False)
    
    # Bundle title, genres, and tags into a single text blob representing the movie
    movies["content"] = movies["title"] + " " + movies["genres"] + " " + movies["tag"]

    # Filter to what we need functionally in the backend
    movies = movies[["movieId", "title", "content", "rating"]]

    logging.info("Initializing SentenceTransformer (Downloads ~80MB logic if first run)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    logging.info("Encoding movie contents into meaning vectors (Takes ~40s)...")
    embeddings = model.encode(movies['content'].tolist(), show_progress_bar=True)
    dimension = embeddings.shape[1]

    logging.info("Building FAISS Vector Index...")
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype=np.float32))

    logging.info(f"Total Movies Indexed: {index.ntotal}")

    logging.info("Exporting the FAISS index and the movie database...")
    # Save the pure C++ FAISS index
    faiss.write_index(index, "model/faiss_index.bin")
    
    # We no longer save the model or embeddings directly (FAISS handles embeddings). 
    # Just the fast Dataframe for lookups!
    with open("model/movie_data.pkl", "wb") as f:
        pickle.dump(movies, f)

    logging.info("✅ Semantic NLP Model trained & Vector DB stored successfully!")

if __name__ == "__main__":
    train_model()