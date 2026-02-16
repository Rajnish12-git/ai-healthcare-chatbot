from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import numpy as np
from rapidfuzz import process, fuzz
import re

app = Flask(__name__)

# ---------------- LOAD MODEL ----------------
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model", "disease_model.pkl")
mlb_path = os.path.join(BASE_DIR, "model", "mlb.pkl")

model = pickle.load(open(model_path, "rb"))
mlb = pickle.load(open(mlb_path, "rb"))


# -------- CLEAN DATASET SYMPTOMS ----------
def clean_symptom(s):
    return s.strip().lower().replace(" ", "_").replace("__","_")

clean_classes = [clean_symptom(s) for s in mlb.classes_]
symptom_index = {clean_classes[i]: i for i in range(len(clean_classes))}

# ---------------- TEXT NORMALIZATION ----------------
def normalize(text):
    text = text.lower()
    text = text.replace("-", " ").replace("_", " ")
    text = re.sub(r'[^a-z\s]', '', text)
    return " ".join(text.split())

# map normalized → real dataset symptom
normalized_choices = {normalize(s): clean_symptom(s) for s in mlb.classes_}

def closest_symptom(word):

    word = normalize(word)

    if len(word) < 3:
        return None

    match = process.extractOne(
        word,
        normalized_choices.keys(),
        scorer=fuzz.token_sort_ratio
    )

    if match and match[1] >= 65:
        return normalized_choices[match[0]]

    return None


# ---------------- LOAD EXTRA DATA ----------------
description_df = pd.read_csv("dataset/symptom_Description.csv")
precaution_df = pd.read_csv("dataset/symptom_precaution.csv")

descriptions = dict(zip(description_df['Disease'], description_df['Description']))
precautions = precaution_df.set_index('Disease').T.to_dict('list')

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# --------- EXTRACT WORDS FROM SENTENCE ----------
def extract_symptoms_from_sentence(text):

    text = text.lower()

    # remove common useless words
    stop_words = ["i", "have", "having", "and", "with", "suffering", "from", "the", "a", "an"]
    words = [w for w in re.split(r'[,\s]+', text) if w not in stop_words]

    return words


# ---------------- PREDICTION LOGIC ----------------
def predict_disease(user_text):

    words = extract_symptoms_from_sentence(user_text)
    cleaned = set()

    for word in words:

        formatted = clean_symptom(word)
        if formatted in symptom_index:
            cleaned.add(formatted)
            continue

        close = closest_symptom(word)
        if close:
            cleaned.add(close)

    if len(cleaned) == 0:
        return None

    input_vector = np.zeros(len(clean_classes))

    for symptom in cleaned:
        input_vector[symptom_index[symptom]] = 1

    probs = model.predict_proba([input_vector])[0]
    top3 = np.argsort(probs)[-3:][::-1]

    return [(model.classes_[i], round(probs[i]*100,2)) for i in top3]


# ---------------- API ROUTE ----------------
@app.route("/predict", methods=["POST"])
def predict():

    text = request.json["message"]

    results = predict_disease(text)

    if results is None:
        return jsonify({
            "reply":"I couldn't understand 😅\nTry writing symptoms like:\nfever headache vomiting skin rash"
        })

    disease = results[0][0]

    desc = descriptions.get(disease,"No description available.")
    prec = precautions.get(disease,[])

    response = "🧠 Possible conditions:\n"
    for d,p in results:
        response += f"{d} — {p}%\n"

    response += f"\n🩺 Description:\n{desc}\n\n💊 Precautions:\n"
    for p in prec:
        if str(p)!="nan":
            response += f"- {p}\n"

    return jsonify({"reply":response})


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

