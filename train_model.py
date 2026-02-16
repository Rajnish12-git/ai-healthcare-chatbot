import pandas as pd
import pickle
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("dataset/dataset.csv")

# Combine symptom columns
symptom_cols = [col for col in df.columns if col != "Disease"]
df["symptoms"] = df[symptom_cols].values.tolist()

# Remove empty values
df["symptoms"] = df["symptoms"].apply(lambda x: [s for s in x if str(s) != "nan"])

# Convert symptoms → binary numbers
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(df["symptoms"])
y = df["Disease"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

# Check accuracy
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))

# Save model
import os
os.makedirs("model", exist_ok=True)

pickle.dump(model, open("model/disease_model.pkl", "wb"))
pickle.dump(mlb, open("model/mlb.pkl", "wb"))

print("Model saved successfully!")

