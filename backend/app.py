from flask import Flask, request, jsonify
import pdfplumber
from flask_cors import CORS
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend access

# Configure Gemini API Key
genai.configure(api_key="AIzaSyCqR2AQZc43CPcU0cM3ZyILD-pC3jcMsHs")

# Use a valid model that supports generateContent
MODEL_NAME = "models/gemini-1.5-pro"

# PDF Summarization Route
@app.route('/summarize', methods=['POST'])
def summarize_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        # Extract text from PDF
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        # Check for empty text
        if not text.strip():
            return jsonify({'error': 'No readable text in PDF'}), 400

        # Generate summary using Gemini
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = (
            "You are a study assistant. Analyze the following syllabus text and:\n"
            "1. Summarize the main topics clearly.\n"
            "2. Provide a weekly study schedule in a table (Week, Topics, Estimated Time).\n"
            "Here is the content:\n\n" + text
        )
        response = model.generate_content(prompt)

        return jsonify({'summary': response.text})
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


# Chatbot Route
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message.strip():
            return jsonify({'reply': 'Please type something!'}), 400

        # Generate response from Gemini using a valid model
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(user_message)

        return jsonify({'reply': response.text})

    except Exception as e:
        return jsonify({'reply': f'Error: {str(e)}'}), 500
    
@app.route('/schedule', methods=['POST'])
def generate_schedule():
    uploaded_files = request.files.getlist("pdfs")
    if not uploaded_files:
        return jsonify({"error": "No PDFs uploaded"}), 400

    model = genai.GenerativeModel("models/gemini-1.5-pro")
    summaries = []

    for file in uploaded_files:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        prompt = (
            "You are a study assistant. Based on the following content, "
            "summarize the main topics and suggest how to study them over a fixed schedule:\n\n" + text[:3000]
        )
        response = model.generate_content(prompt)
        summaries.append(response.text)

    return jsonify({"schedule": summaries})
    


if __name__ == '__main__':
    app.run(debug=True)
