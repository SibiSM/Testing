from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from . import db, create_app
from .models import User, FileUpload
from azure.storage.blob import BlobServiceClient
import os

app = create_app()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_name = file.filename
            blob_service_client = BlobServiceClient.from_connection_string(app.config['AZURE_STORAGE_CONNECTION_STRING'])
            container_client = blob_service_client.get_container_client('uploads')
            container_client.upload_blob(file_name, file)
            file_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/uploads/{file_name}"
            
            new_file = FileUpload(file_name=file_name, file_url=file_url, user=current_user)
            db.session.add(new_file)
            db.session.commit()
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('upload'))

    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
