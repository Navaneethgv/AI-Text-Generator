from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

api_key = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {api_key}"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    user_input = data.get('prompt', '')
    
    if not user_input:
        return jsonify({"error": "Prompt is required"}), 400
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": user_input})
        response.raise_for_status()
        output = response.json()
        return jsonify({"generated_text": output[0]["generated_text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)