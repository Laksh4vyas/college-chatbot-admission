import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def create_dummy_models():
    # Dummy data
    texts = [
        "How do I apply for admission?",
        "What are the admission requirements?",
        "Tell me about scholarships.",
        "How to get financial aid?",
        "Where is the housing located?",
        "Can I apply for a dorm?",
        "When is the application deadline?",
        "What is the last date to apply?"
    ]
    labels = [
        "admissions", "admissions",
        "scholarships", "scholarships",
        "housing", "housing",
        "deadlines", "deadlines"
    ]

    # Create models directory
    os.makedirs("backend/app/models", exist_ok=True)

    # 1. Vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    joblib.dump(vectorizer, "backend/app/models/vectorizer.pkl")

    # 2. Model A: Random Forest
    model_a = RandomForestClassifier(n_estimators=10, random_state=42)
    model_a.fit(X, labels)
    joblib.dump(model_a, "backend/app/models/model_a.pkl")

    # 3. Model B: Logistic Regression
    model_b = LogisticRegression(random_state=42)
    model_b.fit(X, labels)
    joblib.dump(model_b, "backend/app/models/model_b.pkl")

    # 4. Model C: Naive Bayes
    model_c = MultinomialNB()
    model_c.fit(X, labels)
    joblib.dump(model_c, "backend/app/models/model_c.pkl")

    print("Successfully generated dummy models in backend/app/models/")

if __name__ == "__main__":
    create_dummy_models()
