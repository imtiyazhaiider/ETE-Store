import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Image upload folder
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
    UPLOAD_TEMP = os.path.join(BASE_DIR, 'uploads')