# main.py (root) - FastAPI app: pure similarity search
import os
from typing import Optional, List
import pandas as pd
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from search_engine import load_index, similarity_search

# Config
MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
# adjust if needed
CSV_PATH = os.getenv("CSV_PATH", "./dataset/Nykaa_Product_Review_Cleaned.csv")
# adjust if needed
INDEX_DIR = os.getenv("INDEX_DIR", "./faiss_index")

app = FastAPI(title="Ecom Similarity Search API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Schemas


class SearchResult(BaseModel):
    rank: int
    product_id: str | None
    name: str | None
    brand: str | None
    category: str | None
    price: float | None
    rating: float | None
    reviews_count: int | None
    image_url: str | None
    url: str | None
    score: float


class SearchResponse(BaseModel):
    query: str
    category: str | None
    count: int
    results: List[SearchResult]


class ProductResponse(BaseModel):
    product_id: str
    name: str | None
    brand: str | None
    category: str | None
    price: float | None
    rating: float | None
    reviews_count: int | None
    url: str | None
    image_url: str | None
    currency: str | None
    retailer: str | None
    market: str | None
    tags: str | None
    contents: str | None
    description: str | None


# Globals
vs = None
emb = None
df_products = None


@app.on_event("startup")
def startup():
    global vs, emb, df_products
    if not os.path.exists(CSV_PATH):
        raise RuntimeError(f"CSV missing at {CSV_PATH}")
    df_products = pd.read_csv(CSV_PATH)
    df_products["Product Id"] = df_products["Product Id"].astype(str)
    vs, emb = load_index(INDEX_DIR, MODEL_NAME)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "index_loaded": vs is not None,
        "products": int(df_products.shape[0] if df_products is not None else 0),
    }


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    rows = df_products[df_products["Product Id"] == product_id]
    if rows.empty:
        raise HTTPException(status_code=404, detail="Product not found")
    r = rows.iloc[0]
    return {
        "product_id": str(r["Product Id"]),
        "name": r.get("Product Name"),
        "brand": r.get("Product Brand"),
        "category": r.get("Product Category"),
        "price": float(r["Product Price"]) if pd.notna(r.get("Product Price")) else None,
        "rating": float(r["Product Rating"]) if pd.notna(r.get("Product Rating")) else None,
        "reviews_count": int(r["Product Reviews Count"]) if pd.notna(r.get("Product Reviews Count")) else None,
        "url": r.get("Product Url"),
        "image_url": r.get("Product Image Url"),
        "currency": r.get("Product Currency"),
        "retailer": r.get("Retailer"),
        "market": r.get("Market"),
        "tags": r.get("Product Tags"),
        "contents": r.get("Product Contents"),
        "description": r.get("Product Description"),
    }


@app.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = Query(
        None, description="Exact category filter (optional)"),
    k: int = Query(20, ge=1, le=50),
):
    cands = similarity_search(vs, q, k=k, category=category)
    results: List[SearchResult] = []
    for rank, (doc, score) in enumerate(cands, start=1):
        m = doc.metadata or {}
        results.append(SearchResult(
            rank=rank,
            product_id=m.get("product_id"),
            name=m.get("name"),
            brand=m.get("brand"),
            category=m.get("category"),
            price=m.get("price"),
            rating=m.get("rating"),
            reviews_count=m.get("reviews_count"),
            image_url=m.get("image_url"),
            url=m.get("url"),
            score=float(score),
        ))
    return SearchResponse(query=q, category=category, count=len(results), results=results)
