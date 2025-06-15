import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import os

# Load preprocessed data
df = pd.read_csv('./Datasets/term_sheet_preprocessed.csv')
print(f"Loaded {len(df)} rows with columns: {df.columns.tolist()}")

if 'text' not in df.columns or 'label' not in df.columns:
    raise ValueError("Dataset must contain 'text' and 'label' columns")

# Split data
X = df['text']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize
vectorizer = TfidfVectorizer(max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# Save model and vectorizer
os.makedirs('./Backend/model', exist_ok=True)
with open('./Backend/model/model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('./Backend/model/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
print("Model and vectorizer saved.")


