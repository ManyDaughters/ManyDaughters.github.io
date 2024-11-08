import os
from flask import Flask, request, jsonify
import requests
from base64 import b64encode
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GITHUB_TOKEN  os=.getenv('GITHUB_TOKEN')
REPO_OWNER = 'your-github-username'
REPO_NAME = 'your-repo-name'
FILE_PATH = 'path/to/save/file'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    content = file.read()
    encoded_content = b64encode(content).decode('utf-8')

    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}/{file.filename}'
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