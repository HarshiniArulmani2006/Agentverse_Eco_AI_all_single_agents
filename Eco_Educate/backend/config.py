import os
from dotenv import load_dotenv

# Load .env from backend directory or project root
basedir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.dirname(basedir)

load_dotenv(os.path.join(basedir, '.env'))
load_dotenv(os.path.join(parentdir, '.env'))

class Config:
    PORT = int(os.environ.get('PORT', 5000))
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/ecoguide_db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    KNOWLEDGE_BASE_DIR = os.path.join(parentdir, 'knowledge_base')
