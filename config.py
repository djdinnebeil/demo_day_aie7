# config.py
import os
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()

# Set up all required environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY") 
os.environ["CO_API_KEY"] = os.getenv("COHERE_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# Configuration constants
COLLECTION_NAME = "greenwich_docs"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333