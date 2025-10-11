# main.py (root)
import os
from typing import Optional, List
import pandas as pd
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

from search_engine import load_index, search_candidates

MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
CSV_PATH = os.getenv("CSV_PATH", "./dataset/Nykaa_Product_Review_Cleaned.csv")  # adjust if your CSV is elsewhere
INDEX_DIR = os.getenv("INDEX_DIR", "./faiss_index")

# 1) Create app FIRST
app = FastAPI(title="Ecom API", version="1.0.0")

# 2) Schemas
class SearchResult(BaseModel):
    rank: int
    product_id: str | None
    name: str | None
    brand: str | None
    category: str | None
    price: float | None
    rating: float | None
    image_url: str | None
    url: str | None
    score: float

class SearchResponse(BaseModel):
    query: str
    category: str | None
    count: int
    results: List[SearchResult]

# 3) Globals
vs = None
emb = None
df_products = None

# 4) Startup
@app.on_event("startup")
def startup():
    global vs, emb, df_products
    if not os.path.exists(CSV_PATH):
        raise RuntimeError(f"CSV missing at {CSV_PATH}")
    df_products = pd.read_csv(CSV_PATH)
    df_products["Product Id"] = df_products["Product Id"].astype(str)
    vs, emb = load_index(INDEX_DIR, MODEL_NAME)

# 5) Endpoints
@app.get("/health")
def health():
    return {"status": "ok", "index_loaded": vs is not None, "products": int(df_products.shape[0])}

# main.py (root) — only /search endpoint changed
from ranking import rerank_candidates

@app.get("/search", response_model=SearchResponse)
def search(q: str = Query(...), category: Optional[str] = Query(None), k: int = Query(5, ge=1, le=50)):
    # Stage 1: pure similarity retrieval with strict category
    cands = search_candidates(vs, q, k=max(50, k), category=category)

    # Optional: provide tiny behavior priors if available; for root setup, pass empty dicts
    brand_aff = {}
    cat_aff = {}
    price_band = (None, None)

    # Stage 2: rerank only these candidates
    final = rerank_candidates(cands, brand_aff, cat_aff, price_band, top_k=k)

    results: List[SearchResult] = []
    for rank, (doc, score) in enumerate(final, start=1):
        m = doc.metadata or {}
        results.append(SearchResult(
            rank=rank,
            product_id=m.get("product_id"),
            name=m.get("name"),
            brand=m.get("brand"),
            category=m.get("category"),
            price=m.get("price"),
            rating=m.get("rating"),
            image_url=m.get("image_url"),
            url=m.get("url"),
            score=round(float(score), 3),
        ))
    return SearchResponse(query=q, category=category, count=len(results), results=results)

