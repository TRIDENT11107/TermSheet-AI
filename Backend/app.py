from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.ocr_utils import extract_text_from_image
from utils.pdf_utils import extract_text_from_pdf
from utils.predict import predict_text
import os
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    logger.debug("Received request to /predict endpoint")
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Request headers: {request.headers}")
    logger.debug(f"Request files: {request.files}")
    
    try:
        if 'file' not in request.files:
            logger.debug("No file part in the request")
            if request.is_json and 'text' in request.json:
                logger.debug("Using JSON text input")
                text = request.json['text']
            else:
                logger.warning("No file or text provided")
                return jsonify({'error': 'No file or text provided'}), 400
        else:
            file = request.files['file']
            if file.filename == '':
                logger.warning("Empty filename")
                return jsonify({'error': 'No selected file'}), 400
                
            filename = file.filename.lower()
            logger.debug(f"Processing file: {filename}")
            logger.debug(f"File content type: {file.content_type}")
            
            # OCR for images
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                logger.debug("Processing as image")
                text = extract_text_from_image(file.stream)
            # PDF processing
            elif filename.endswith('.pdf'):
                logger.debug("Processing as PDF")
                text = extract_text_from_pdf(file.stream)
            # Text extraction for txt/csv
            elif filename.endswith(('.txt', '.csv')):
                logger.debug("Processing as text file")
                text = file.read().decode('utf-8')
            # Word document processing - treat as text for now
            elif filename.endswith(('.doc', '.docx')):
                logger.debug("Processing as Word document (text only)")
                text = "Word document processing is limited. Please convert to PDF or text."
            # Excel processing - treat as text for now
            elif filename.endswith(('.xls', '.xlsx')):
                logger.debug("Processing as Excel file (text only)")
                text = "Excel file processing is limited. Please convert to CSV or text."
            else:
                extension = filename.split(".")[-1] if "." in filename else "unknown"
                logger.warning(f"Unsupported file type: {extension}")
                return jsonify({
                    'error': f'Unsupported file type: {extension}',
                    'supported_types': [
                        'pdf', 'txt', 'csv', 
                        'png', 'jpg', 'jpeg', 'bmp', 'tiff',
                        'doc', 'docx', 'xls', 'xlsx'
                    ],
                    'filename': filename,
                    'content_type': file.content_type
                }), 400

        # Get prediction and NLP insights
        logger.debug("Getting prediction for text")
        result = predict_text(text)
        logger.debug(f"Prediction result: {result['prediction']}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'TermSheet AI Backend is running'})

@app.route('/test-upload', methods=['POST'])
def test_upload():
    """Test endpoint for file uploads"""
    logger.debug("Received request to /test-upload endpoint")
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Request headers: {request.headers}")
    
    response = {
        'status': 'received',
        'files': {},
        'form': {},
        'json': None
    }
    
    if 'file' in request.files:
        file = request.files['file']
        response['files'] = {
            'filename': file.filename,
            'content_type': file.content_type,
            'size': 'stream, size unknown'
        }
    
    if request.form:
        response['form'] = {k: v for k, v in request.form.items()}
    
    if request.is_json:
        response['json'] = request.json
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
