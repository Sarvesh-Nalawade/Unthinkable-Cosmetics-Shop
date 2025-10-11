# ranking.py (root)
from typing import Dict, Any, Tuple, List
import numpy as np

def _minmax_norm(vals: List[float]) -> List[float]:
    v = np.array(vals, dtype=float)
    if v.size == 0:
        return []
    v = np.nan_to_num(v, nan=0.0, posinf=0.0, neginf=0.0)
    lo, hi = float(v.min()), float(v.max())
    if hi - lo < 1e-9:
        return [0.0 for _ in v]
    return list((v - lo) / (hi - lo))

def popularity_prior(m: Dict[str, Any]) -> float:
    rating = float(m.get("rating", 0.0) or 0.0)
    reviews = float(m.get("reviews_count", 0.0) or 0.0)
    return 0.7*(rating/5.0) + 0.3*(np.tanh(reviews/1000.0))

def price_match(price_val: Any, band: Tuple[float | None, float | None]) -> float:
    lo, hi = band
    try:
        price = float(price_val) if price_val is not None else None
    except Exception:
        price = None
    if price is None or lo is None or hi is None:
        return 0.0
    return 1.0 if (lo <= price <= hi) else 0.0

def rerank_candidates(
    query_docs_scores: List[tuple],
    brand_aff: Dict[str,float] | None = None,
    cat_aff: Dict[str,float] | None = None,
    price_band: Tuple[float | None, float | None] = (None, None),
    top_k: int = 5
):
    brand_aff = brand_aff or {}
    cat_aff = cat_aff or {}
    # normalize similarity within the retrieved set
    base_sims = [float(s) for _, s in query_docs_scores]
    base_norm = _minmax_norm(base_sims)

    ranked = []
    for (doc, base_sim), base_n in zip(query_docs_scores, base_norm):
        m = doc.metadata or {}
        b = float(brand_aff.get((m.get("brand") or "").strip().lower(), 0.0))
        c = float(cat_aff.get((m.get("category") or "").strip().lower(), 0.0))
        pm = price_match(m.get("price", 0.0), price_band)
        pop = popularity_prior(m)

        # retrieval-first weights
        score = (
            0.70*base_n +
            0.10*b +
            0.10*c +
            0.05*pm +
            0.05*pop
        )
        ranked.append((doc, score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
