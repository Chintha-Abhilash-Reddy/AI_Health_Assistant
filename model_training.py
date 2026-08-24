"""
model_training.py — Machine Learning model training for disease prediction.
Trains multiple classification models and saves the best performing model.
"""
import os
import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Ensure utf-8 stdout on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "disease_symptoms.csv")
MODEL_PATH = os.path.join(BASE_DIR, "disease_model.pkl")


def load_and_preprocess_data():
    """Load dataset and separate features and target."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    print(f"[+] Dataset loaded successfully. Shape: {df.shape}")
    print(f"[+] Total Diseases ({df['disease'].nunique()}): {list(df['disease'].unique())}")

    X = df.drop(columns=["disease"])
    y = df["disease"]
    feature_names = list(X.columns)

    return X, y, feature_names


def train_models():
    """Train multiple classifiers and select the best model."""
    X, y, feature_names = load_and_preprocess_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Multinomial Naive Bayes": MultinomialNB()
    }

    best_model = None
    best_name = ""
    best_accuracy = 0.0
    evaluation_results = {}

    print("\n[+] Training and evaluating models...")
    print("=" * 60)

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        evaluation_results[name] = acc
        print(f"-> {name:25s} Accuracy: {acc * 100:.2f}%")

        if acc > best_accuracy:
            best_accuracy = acc
            best_model = model
            best_name = name

    print("=" * 60)
    print(f"[OK] Best Model: {best_name} with Accuracy: {best_accuracy * 100:.2f}%\n")

    # Save package containing model, feature names, classes
    model_payload = {
        "model": best_model,
        "model_name": best_name,
        "accuracy": best_accuracy,
        "feature_names": feature_names,
        "classes": list(best_model.classes_)
    }

    joblib.dump(model_payload, MODEL_PATH)
    print(f"[OK] Model saved to: {MODEL_PATH}")
    return model_payload


def predict_from_symptoms(symptoms_dict):
    """
    Given a dictionary of symptom_name -> 0 or 1,
    return predicted disease, confidence score, and top 3 predictions with probabilities.
    """
    if not os.path.exists(MODEL_PATH):
        print("[!] Model file not found. Training model now...")
        train_models()

    payload = joblib.load(MODEL_PATH)
    model = payload["model"]
    feature_names = payload["feature_names"]

    # Construct feature vector as DataFrame with feature names
    input_vector = [1 if symptoms_dict.get(feat, 0) == 1 or symptoms_dict.get(feat) is True else 0 for feat in feature_names]
    input_df = pd.DataFrame([input_vector], columns=feature_names)

    predicted_disease = model.predict(input_df)[0]
    
    # Get probabilities if supported
    probabilities = {}
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_df)[0]
        for cls_name, prob in zip(model.classes_, probs):
            probabilities[cls_name] = round(float(prob) * 100, 2)
        confidence = probabilities.get(predicted_disease, 90.0)
    else:
        confidence = 90.0

    # Top 3 likely diseases
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "predicted_disease": predicted_disease,
        "confidence": confidence,
        "top_predictions": sorted_probs,
        "input_features": dict(zip(feature_names, input_vector))
    }


if __name__ == "__main__":
    train_models()

