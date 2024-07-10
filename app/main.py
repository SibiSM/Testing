from flask import Flask, Blueprint, render_template, request
from azure.storage.blob import BlobServiceClient
import os
from . import db

# Load environment variables from .env file

main = Blueprint('main', __name__)

# Replace with your storage account name
storage_account_name = 'storageblobsibi1'
# Access storage account key from environment variable
storage_account_key = '4fU38ADACEDqvdZBKv1swP4hVnc5IO978SjGjvwFgivU0TDD+/znu1Te9OYzXL+AFxdex3MGpyx8+AStb3PtDg=='
container_name = 'containerstorage'

connect_str = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        blob_client.upload_blob(file)
        return f"File {file.filename} uploaded successfully."

# Create Flask app
app = Flask(__name__)
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
