# sear.py (root) - pure similarity search utilities
from typing import Optional, List, Tuple
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def load_index(index_dir: str, model_name: str):
    """
    Load a FAISS index and its embedding model.
    """
    emb = HuggingFaceEmbeddings(model_name=model_name)
    vs = FAISS.load_local(index_dir, emb, allow_dangerous_deserialization=True)
    return vs, emb


def _norm(x: Optional[str]) -> str:
    return (x or "").strip().lower()


def _cat_match(meta_category: Optional[str], requested: Optional[str]) -> bool:
    if not requested:
        return True
    return _norm(meta_category) == _norm(requested)


def similarity_search(vs, query: str, k: int = 10, category: Optional[str] = None) -> List[Tuple[object, float]]:
    """
    Perform semantic similarity search and return up to k (doc, score) items.
    If category is provided, apply a strict, case-insensitive filter on metadata.
    """
    pool = max(20 * k, 100)
    raw = vs.similarity_search_with_score(query, k=pool)
    if category:
        strict = [(d, s) for (d, s) in raw if _cat_match(
            d.metadata.get("category"), category)]
        return strict[:k]
    return raw[:k]
