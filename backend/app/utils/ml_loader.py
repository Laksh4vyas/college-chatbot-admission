import os
import joblib

# Paths to models
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

class MLLoader:
    def __init__(self):
        self.vectorizer = None
        self.model_a = None
        self.model_b = None
        self.model_c = None

    def load_models(self):
        try:
            self.vectorizer = joblib.load(os.path.join(MODEL_DIR, "vectorizer.pkl"))
            self.model_a = joblib.load(os.path.join(MODEL_DIR, "model_a.pkl"))
            self.model_b = joblib.load(os.path.join(MODEL_DIR, "model_b.pkl"))
            self.model_c = joblib.load(os.path.join(MODEL_DIR, "model_c.pkl"))
            print("Models loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}")

ml_loader = MLLoader()
