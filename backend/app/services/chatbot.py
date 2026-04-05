import numpy as np
from app.utils.ml_loader import ml_loader

CANNED_RESPONSES = {
    "admissions": "You can apply for admission through our online portal. Make sure you have your transcripts and recommendation letters ready.",
    "scholarships": "We offer various merit and need-based scholarships. The application opens in November.",
    "housing": "Our on-campus housing includes dorms and apartments. Freshman are guaranteed housing if they apply by May 1st.",
    "deadlines": "The regular decision deadline is January 15th, and early action is November 1st.",
    "unknown": "I'm sorry, I'm not sure how to answer that regarding admissions. Could you please rephrase?"
}

def process_chat(message: str):
    if not ml_loader.vectorizer:
        ml_loader.load_models()

    if not ml_loader.vectorizer:
        return {"answer": "Bot is not initialized yet.", "confidence": 0.0, "model": "None"}

    # Vectorize input
    X = ml_loader.vectorizer.transform([message])

    try:
        # Get probabilities from all 3 models
        # Assuming the classes are identical across models and in same order
        prob_a = ml_loader.model_a.predict_proba(X)[0]
        prob_b = ml_loader.model_b.predict_proba(X)[0]
        prob_c = ml_loader.model_c.predict_proba(X)[0]

        # Soft voting: average probabilities
        avg_probs = (prob_a + prob_b + prob_c) / 3.0

        # Max probability and its corresponding class index
        max_idx = np.argmax(avg_probs)
        confidence = avg_probs[max_idx]
        
        # Get classes (assumes model_a.classes_ is the standard)
        classes = ml_loader.model_a.classes_
        predicted_class = classes[max_idx]

        # Confidence threshold
        if confidence < 0.3:
            intent = "unknown"
        else:
            intent = predicted_class

        answer = CANNED_RESPONSES.get(intent, CANNED_RESPONSES["unknown"])

        return {
            "answer": answer,
            "confidence": float(confidence),
            "model": "Soft Voting (A+B+C)"
        }
    except Exception as e:
        print(f"Error in prediction: {e}")
        return {"answer": "I encountered an error processing your request.", "confidence": 0.0, "model": "Error"}
