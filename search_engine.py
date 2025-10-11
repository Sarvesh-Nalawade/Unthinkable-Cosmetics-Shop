# search_engine.py (root)
from typing import Optional, List, Tuple
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_index(index_dir: str, model_name: str):
    emb = HuggingFaceEmbeddings(model_name=model_name)
    vs = FAISS.load_local(index_dir, emb, allow_dangerous_deserialization=True)
    return vs, emb

def _norm(x: Optional[str]) -> str:
    return (x or "").strip().lower()

def _cat_match(meta_category: Optional[str], requested: Optional[str]) -> bool:
    if not requested:
        return True
    return _norm(meta_category) == _norm(requested)

def search_candidates(vs, query: str, k: int = 50, category: Optional[str] = None) -> List[Tuple[object, float]]:
    raw = vs.similarity_search_with_score(query, k=max(5*k, 100))
    if category:
        strict = [(d, s) for (d, s) in raw if _cat_match(d.metadata.get("category"), category)]
        return strict[:k]
    return raw[:k]
