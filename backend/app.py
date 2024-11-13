import os
from flask import Flask, request, jsonify
import requests
from base64 import b64encode
from dotenv import load_dotenv
from urllib.parse import quote
from datetime import datetime  # Add import for datetime

load_dotenv()

app = Flask(__name__)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'ManyDaughters'
REPO_NAME = 'ManyDaughters.github.io'
FILE_PATH = 'files'  # Ensure this path is correct and does not contain invalid characters

# Debug print to verify the GitHub token
print(f'GITHUB_TOKEN: {GITHUB_TOKEN}')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    team_id = request.form.get('team-id')
    print('Received team ID:', team_id)  # Log the received team ID for debugging
    if not team_id:
        return jsonify({'error': 'No team ID provided'}), 400

    content = file.read()
    encoded_content = b64encode(content).decode('utf-8')

    # Generate the timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H:%M:%S')

    # Create the new filename with timestamp and team ID
    new_filename = f'{timestamp}_{team_id}_{file.filename}'

    # URL encode the file path and file name
    file_path = quote(f'{FILE_PATH}/{new_filename}')

    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Check if the file already exists
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()['sha']
        data = {
            'message': 'Update uploaded file',
            'content': encoded_content,
            'sha': sha
        }
    else:
        data = {
            'message': 'Add uploaded file',
            'content': encoded_content
        }

    # Debug: Log the request details
    print(f'URL: {url}')
    print(f'Headers: {headers}')
    print(f'Data: {data}')

    response = requests.put(url, headers=headers, json=data)
    
    # Debug: Log the response details
    print(f'Response Status Code: {response.status_code}')
    print(f'Response Content: {response.content}')

    if response.status_code == 201:
        return jsonify({'message': 'File uploaded successfully'}), 201
    else:
        # Add debug message to display the path
        return jsonify({'error': response.json(), 'path': file_path}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)