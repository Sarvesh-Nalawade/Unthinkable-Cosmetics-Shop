import re
import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# 2) Load CSV
csv_path = "./dataset/Nykaa_Product_Review_Cleaned.csv"
df = pd.read_csv(csv_path)


def safe(x):
    return "" if pd.isna(x) else str(x)


def safe_int(x):
    if pd.isna(x):
        return 0
    s = str(x).strip()
    # Check if it's a valid integer or float
    if re.fullmatch(r"[+-]?\d+(\.\d+)?", s):
        return int(float(s))
    return 0  # fallback for invalid strings


# Build texts
texts = (
    df["Product Name"].map(safe) + " | " +
    df["Product Category"].map(safe) + " | " +
    df["Product Brand"].map(safe) + " | " +
    df["Product Tags"].map(safe) + " | " +
    df["Product Contents"].map(safe) + " | " +
    df["Product Description"].map(safe)
).tolist()

# Build metadatas (FIXED)
metadatas = [
    {
        "product_id": safe(r["Product Id"]),
        "brand_code": safe(r["Product Brand Code"]),
        "retailer": safe(r["Retailer"]),
        "category": safe(r["Product Category"]),
        "brand": safe(r["Product Brand"]),
        "name": safe(r["Product Name"]),
        "price": float(r["Product Price"]) if pd.notna(r["Product Price"]) else 0.0,
        "url": safe(r["Product Url"]),
        "market": safe(r["Market"]),
        "currency": safe(r["Product Currency"]),
        "image_url": safe(r["Product Image Url"]),
        "tags": safe(r["Product Tags"]),
        "contents": safe(r["Product Contents"]),
        "rating": float(r["Product Rating"]) if pd.notna(r["Product Rating"]) else 0.0,
        "reviews_count": safe_int(r["Product Reviews Count"]),
        "exp_cat_count": safe_int(r["Expected Category Count"]),
        "exp_brand_count": safe_int(r["Expected Brand Count"])
    }
    for _, r in df.iterrows()
]


# 4) Embeddings (Sentence-Transformers via HuggingFace)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)


# 5) Create FAISS vector store and persist
faiss_store = FAISS.from_texts(
    texts=texts, embedding=embeddings, metadatas=metadatas)
INDEX_DIR = "faiss_index"
faiss_store.save_local(INDEX_DIR)
print(f"Index saved to ./{INDEX_DIR}")
