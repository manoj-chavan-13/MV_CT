import logging
import traceback
from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from model.recommender import recommend_movies

# Configure application logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

app = Flask(__name__)

# Load lightweight LLM model once
logging.info("Loading Google FLAN-T5 Chatbot Engine...")
try:
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    def generate_response(prompt):
        inputs = tokenizer(prompt, return_tensors="pt")
        # Added hyper-parameters for a more organic, conversational tone instead of rigid outputs
        outputs = model.generate(
            **inputs, 
            max_length=60, 
            do_sample=True,
            temperature=0.7, 
            repetition_penalty=1.2
        )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
        
    logging.info("✅ Conversational LLM Model loaded natively with RAG Tuning!")
except Exception as e:
    logging.error(f"Failed to load the local LLM! {traceback.format_exc()}")
    generate_response = None

@app.route("/")
def home():
    return render_template("index.html")

import re

@app.route("/chat", methods=["POST"])
def chat():
    """
    RAG generation endpoint with conversational styling. Embeds mathematical intent 
    and passes it through our tuned FLAN-T5 LLM backend to act like a cinematic expert.
    """
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "Oops! I didn't see a message. Try typing a mood or a movie you love!", "error": True}), 400

        user_message = data["message"]
        clean_msg = re.sub(r'[^\w\s]', '', user_message.lower().strip())
        logging.info(f"User Query Intent: '{user_message}'")

        # --- INTENT ROUTER FOR SIMPLE CHATS ---
        basic_greetings = {"hi", "hello", "hey", "hola", "greetings", "sup", "howdy", "heya"}
        # If it's a pure greeting or simple short hi
        if clean_msg in basic_greetings or (clean_msg.startswith(("hi ", "hello ", "hey ")) and len(clean_msg.split()) <= 3) or clean_msg == "how are you":
            return jsonify({
                "reply": "Hello there! 👋 I am ready to help. What kind of movie vibe are you in the mood for?",
                "recommendations": [],
                "error": False
            })
            
        if "who are you" in clean_msg or "what are you" in clean_msg or "who made you" in clean_msg:
            return jsonify({
                "reply": "I am CineBot, an advanced Semantic AI Recommendation Engine! I was made by TE AIML students and designed by NIKITA WAGH. Just tell me what kind of movie you want to watch!",
                "recommendations": [],
                "error": False
            })
        # --------------------------------------

        # Step 1: Process User Message in the FAISS Vector Engine natively
        rec_data = recommend_movies(user_message, num=5)
        
        if isinstance(rec_data, dict) and "error" in rec_data:
            return jsonify({"reply": rec_data["error"], "error": True}), 500

        recs = rec_data.get("recommendations", [])
        
        # Step 3: Construct the Conversational RAG Prompt for FLAN-T5
        # We enforce a persona on the model ("As an enthusiastic movie expert...")
        # Since FLAN-T5 is tiny, we ask it to just write a short 1-sentence opening.
        prompt = f"As an enthusiastic movie expert, write one brief excited sentence recommending amazing movies for someone asking: '{user_message}'"

        # Step 4: Generate Intro Sentence
        if generate_response:
            ai_intro = generate_response(prompt)
            # Failsafe for tiny models returning gibberish/empty arrays:
            if len(ai_intro.strip()) < 10 or "http" in ai_intro:
                ai_intro = f"I've analyzed your amazing vibe and found the absolute perfect matches for you!"
        else:
            ai_intro = f"Here are the absolute best matches based on deep semantic meaning and user rating formulas!"

        # Combine the AI's organic intro with our flawless mathematical hardcoded recommendations
        # The AI doesn't have to struggle formatting arrays, and the user gets a perfect UX.
        # Note: We send the text combined or let the frontend render it. Here we construct the full HTML payload.
        
        final_text = ai_intro

        return jsonify({
            "reply": final_text, 
            "recommendations": recs, # Pass the raw arrays with ⭐ to UI visually intact
            "error": False
        })

    except Exception as e:
        logging.error(f"Exception in /chat: {traceback.format_exc()}")
        return jsonify({"reply": "Uh oh, an unexpected database error occurred while parsing the Vector similarities.", "error": True}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)