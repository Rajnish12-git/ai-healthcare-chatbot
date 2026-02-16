# 🩺 AI Healthcare Chatbot

An AI-powered web application that analyzes user symptoms and suggests possible related medical conditions along with descriptions and precautions.

> ⚠️ This project is for educational purposes only and does NOT provide medical diagnosis.

---

## 🌐 Live Demo

https://ai-healthcare-chatbot-qw0q.onrender.com

---

## 🚀 Features

* Natural language symptom input (e.g., *"I have fever and headache"*)
* Fuzzy symptom matching using NLP
* Machine Learning disease prediction
* Top-3 probable conditions with confidence scores
* Disease description & precautions
* Clean chat-based UI
* Deployed on cloud (Render)

---

## 🧠 Machine Learning

* Multi-label symptom encoding
* Random Forest Classifier
* Data preprocessing & cleaning
* Fuzzy text matching (RapidFuzz)
* Confidence-based prediction filtering

---

## 🏗️ Tech Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend**

* Python
* Flask

**ML & NLP**

* Scikit-learn
* Pandas
* NumPy
* RapidFuzz

**Deployment**

* Render
* Gunicorn

---

## 📂 Project Structure

```
AI-Healthcare-Chatbot/
│── app.py
│── train_model.py
│── requirements.txt
│── Procfile
│── model/
│   ├── disease_model.pkl
│   └── mlb.pkl
│── dataset/
│── templates/
│── static/
```

---

## ⚙️ Installation (Local Setup)

```bash
git clone https://github.com/Rajnish12-git/ai-healthcare-chatbot.git
cd ai-healthcare-chatbot

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python train_model.py
python app.py
```

Open: http://127.0.0.1:5000

---

## 📊 Example Input

```
fever, headache, cough
```

## Example Output

```
Possible related conditions:
Flu — 52%
Common Cold — 28%
Viral Fever — 20%
```

---

## 📌 Future Improvements

* Voice symptom input
* Doctor recommendation system
* Medical dataset expansion
* Multilingual support

---

## 👨‍💻 Author

**Rajnish Kumar**
B.Tech CSE (AI & ML)

---

## ⭐ If you found this useful

Give the repository a star!
