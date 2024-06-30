from flask import Flask, Blueprint, render_template, request
from azure.storage.blob import BlobServiceClient
import os
from . import db

# Load environment variables from .env file

main = Blueprint('main', __name__)

# Replace with your storage account name
storage_account_name = 'storageblobsibi'
# Access storage account key from environment variable
storage_account_key = 'VT7S9dgXI852GVGOn9j5YEMtm+oLWbcv47alx6WYHon8H1EG5FSazVhjTv3+t/jCXYKD3+G57TXk+AStyQI9gw=='
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
