"""WSGI entry point for production deployment."""
from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == "__main__":
    app.run()
