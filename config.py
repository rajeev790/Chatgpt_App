import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
