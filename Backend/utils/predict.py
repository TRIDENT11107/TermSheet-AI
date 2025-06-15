import pickle
import os
from textblob import TextBlob
from .nlp_utils import preprocess_text, extract_entities, analyze_sentiment

# Get the absolute path to the model directory
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(os.path.dirname(current_dir))
model_dir = os.path.join(os.path.dirname(current_dir), 'model')

# Load model and vectorizer
try:
    with open(os.path.join(model_dir, 'model.pkl'), 'rb') as f:
        model = pickle.load(f)
    with open(os.path.join(model_dir, 'vectorizer.pkl'), 'rb') as f:
        vectorizer = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    # Create dummy model and vectorizer for testing
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    vectorizer = TfidfVectorizer(max_features=100)
    vectorizer.fit(["This is a sample text for testing"])
    model = LogisticRegression()
    model.classes_ = ["valid", "invalid"]
    model.coef_ = [[0.1] * 100]
    model.intercept_ = [0.0]

def predict_text(text):
    """Predict the class of the given text using the trained model"""
    processed_text = preprocess_text(text)
    
    try:
        X_vec = vectorizer.transform([processed_text])
        prediction = model.predict(X_vec)[0]
    except Exception as e:
        print(f"Error during prediction: {e}")
        prediction = "Unable to predict"
    
    # Get additional NLP insights
    entities = extract_entities(text)
    sentiment = analyze_sentiment(text)
    
    return {
        'prediction': prediction,
        'entities': list(entities),
        'sentiment': sentiment
    }
