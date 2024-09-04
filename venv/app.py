from flask import Flask, request, jsonify, render_template
from inference_sdk import InferenceHTTPClient
import os

app = Flask(__name__)

# Initialize the Inference Client
CLIENT = InferenceHTTPClient(
    api_url="https://classify.roboflow.com",
    api_key="cvcTSkApmzakxa3MJeXx"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        # Save the file to a temporary location
        file_path = os.path.join('', file.filename)
        file.save(file_path)

        # Perform inference
        result = CLIENT.infer(file_path, model_id="drug-dvkcr/1")

        # Remove the file after inference
        os.remove(file_path)

        return jsonify(result)

    return jsonify({'error': 'Something went wrong'}), 500

if __name__== '_main_':
    app.run(debug=True, port=5001)
