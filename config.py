import os

MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
CSV_PATH = os.getenv("CSV_PATH", "./dataset/Nykaa_Product_Review_Cleaned.csv")
INDEX_DIR = os.getenv("INDEX_DIR", "./faiss_index")
INTERACTIONS_PATH = os.getenv("INTERACTIONS_PATH", "./data/interactions_u0001.csv")
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "u_0001")
APP_NAME = os.getenv("APP_NAME", "E-commerce Recommender API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
