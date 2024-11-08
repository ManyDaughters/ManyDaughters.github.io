import os
from flask import Flask, request, jsonify
import requests
from base64 import b64encode
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

app = Flask(__name__)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'ManyDaughters'
REPO_NAME = 'ManyDaughters.github.io'
FILE_PATH = 'main/tree/files/'  # Ensure this path is correct and does not contain invalid characters

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    content = file.read()
    encoded_content = b64encode(content).decode('utf-8')

    # URL encode the file path and file name
    file_path = quote(f'{FILE_PATH}/{file.filename}')

    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'message': 'Add uploaded file',
        'content': encoded_content
    }

    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        return jsonify({'message': 'File uploaded successfully'}), 201
    else:
        return jsonify({'error': response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)