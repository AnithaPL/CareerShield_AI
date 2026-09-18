
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load EMSCAD dataset
DATA_PATH = "data/emscad_dataset.csv"

data = pd.read_csv(DATA_PATH)

print("Dataset size:", len(data))

# Convert missing values to empty strings
text_columns = [
    "title",
    "location",
    "department",
    "salary_range",
    "company_profile",
    "description",
    "requirements",
    "benefits",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function"
]

for column in text_columns:
    data[column] = data[column].fillna("").astype(str)

# Combine relevant text fields
data["combined_text"] = data[text_columns].agg(" ".join, axis=1)

# Convert labels
# f = Genuine
# t = Likely Scam

data["label"] = data["fraudulent"].map({
    "f": "Genuine",
    "t": "Likely Scam"
})

# Remove invalid labels
data = data.dropna(subset=["label"])

X = data["combined_text"]
y = data["label"]

print("\nCategory distribution:")
print(y.value_counts())

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Create machine learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            ngram_range=(1, 2),
            lowercase=True,
            sublinear_tf=True,
            min_df=2,
            max_df=0.98,
            max_features=100000
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            solver="liblinear"
        )
    )
])

# Train model
print("\nTraining real ML model...")

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nAccuracy:", round(accuracy, 4))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# Save trained model
os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/scam_pipeline.joblib"
)

print("\nReal ML model saved successfully!")
print("Location: models/scam_pipeline.joblib")