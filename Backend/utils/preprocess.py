import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Download NLTK stopwords if not already present
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def clean_text(text):
    """Remove special characters, lowercase, and strip whitespace."""
    if isinstance(text, str):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower().strip()
        # Remove stopwords
        tokens = [word for word in text.split() if word not in stop_words]
        return " ".join(tokens)
    return ""

if __name__ == "__main__":
    # Process Term-Sheet.csv
    with open('./Datasets/Term-Sheet.csv', 'r', encoding='utf-8') as f:
        lines = [line.strip().strip('"') for line in f if line.strip().strip('"')]
    
    # Clean the lines
    cleaned_lines = [clean_text(line) for line in lines if len(line.strip()) > 10]
    
    # Create dummy labels for demonstration
    labels = ['valid' if i % 2 == 0 else 'invalid' for i in range(len(cleaned_lines))]
    
    # Create a DataFrame
    df = pd.DataFrame({'text': cleaned_lines, 'label': labels})
    df.to_csv('./Datasets/term_sheet_preprocessed.csv', index=False)
    print("Preprocessing complete. Saved to term_sheet_preprocessed.csv")
