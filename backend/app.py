import os
from flask import Flask, request, jsonify
import requests
from base64 import b64encode
from dotenv import load_dotenv
from urllib.parse import quote
from datetime import datetime  # Add import for datetime
from flask_cors import CORS  # Add this import

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://manydaughters.github.io"])  # Enable CORS for the specified origin

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'ManyDaughters'
REPO_NAME = 'RT_uploads'
FILE_PATH = 'do-files'  # Ensure this path is correct and does not contain invalid characters

# Debug print to verify the GitHub token
print(f'GITHUB_TOKEN: {GITHUB_TOKEN}')

@app.route('/upload', methods=['POST'])
def upload_file():
    files = [request.files.get(f'file{i}') for i in range(1, 5)]
    if not any(files):
        return jsonify({'error': 'No files part'}), 400

    team_id = request.form.get('team-id')
    print('Received team ID:', team_id)  # Log the received team ID for debugging
    if not team_id:
        return jsonify({'error': 'No team ID provided'}), 400

    responses = []
    uploaded_files = []
    for i, file in enumerate(files, start=1):
        if file and file.filename:
            content = file.read()
            encoded_content = b64encode(content).decode('utf-8')

            # Generate the timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Create the new filename with timestamp and team ID
            new_filename = f'{timestamp}_{team_id}_{file.filename}'
            uploaded_files.append(new_filename)

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
                responses.append({'message': f'File {file.filename} uploaded successfully'})
            else:
                responses.append({'error': response.json(), 'path': file_path})
        else:
            responses.append({'error': f'No file selected for file{i}'})

    print('Responses:', responses)  # Log the responses
    return jsonify({'responses': responses, 'uploaded_files': uploaded_files}), 201 if all('message' in res for res in responses) else 400

@app.route('/')
def index():
    return "Server is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
