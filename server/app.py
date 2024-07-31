from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Directory where invoices are stored
INVOICES_DIR = 'invoices'

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def calculate_similarity(text, documents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text] + documents)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return cosine_similarities

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        uploaded_text = extract_text_from_pdf(file)

        invoice_texts = []
        invoice_data = []

        # Read existing invoices
        for filename in os.listdir(INVOICES_DIR):
            if filename.endswith('.pdf'):
                with open(os.path.join(INVOICES_DIR, filename), 'rb') as f:
                    text = extract_text_from_pdf(f)
                    invoice_texts.append(text)
                    invoice_data.append({
                        "invoice_number": filename.split('.')[0],  # Assuming the filename is the invoice number
                        "text": text
                    })

        if not invoice_texts:
            return jsonify({"error": "No invoices found in database"}), 400

        # Calculate similarity
        similarities = calculate_similarity(uploaded_text, invoice_texts)
        most_similar_index = np.argmax(similarities)
        most_similar_invoice = invoice_data[most_similar_index]
        similarity_score = similarities[most_similar_index]

        return jsonify({
            "most_similar_invoice": {
                "invoice_number": most_similar_invoice["invoice_number"],
                "text": most_similar_invoice["text"]
            },
            "similarity_score": similarity_score
        })

if __name__ == '__main__':
    app.run(debug=True)
