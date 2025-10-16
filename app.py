import requests
import streamlit as st

import math
from typing import Optional, List
from dataclasses import dataclass


SERVER_URL = "http://ut-backend:8000"

st.set_page_config(
    page_title="Unthinkable Assignment",
    page_icon=":guardsman:", layout="wide"
)

st.subheader("Unthinkable Assignment", divider="rainbow")


# --------------------------------------------------------------------------------
# Globals:
# --------------------------------------------------------------------------------

st.session_state["query"] = ""


# --------------------------------------------------------------------------------
# Classes:
# --------------------------------------------------------------------------------


@dataclass
class Product:
    rank: int
    product_id: str
    name: str
    url: str
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    image_url: Optional[str] = None
    score: Optional[float] = None

    @staticmethod
    def from_json(data: dict) -> "Product":
        return Product(**data)


# --------------------------------------------------------------------------------
# Helpers:
# --------------------------------------------------------------------------------


def fetch_products_by_query(q: str) -> List[Product]:
    url = f"{SERVER_URL}/search?q={q}"
    response = requests.get(url)
    response = response.json()
    return [Product.from_json(prod) for prod in response.get("results", [])]


# def format_name(name: str, max_len: int = 60) -> str:
#     name = name.strip()
#     if len(name) > max_len:
#         return "**" + name[:max_len - 4] + " ...**"
#     else:
#         name = f"**{name}**"
#         # return name.ljust(max_len, " ")
#         pad_char = ["\u2007", "\u200B", "˙"][2]
#         return name + " " + pad_char * (max_len - len(name) - 1)

def format_name_html(name: str, total_len: int = 60, pad_char: str = "·") -> str:
    """
    Returns an HTML-safe string where the visible name is followed by 'invisible' padding.
    - If name longer than total_len -> truncates to total_len-4 and adds " ..."
    - Else -> appends pad_char repeated to reach total_len, wrapped in a transparent <span>.
    Use with st.markdown(..., unsafe_allow_html=True)
    """
    name = (name or "").strip()
    if len(name) > total_len:
        visible = name[: total_len - 4] + " ..."
        return f"<b>{visible}</b>"
    else:
        # compute count relative to characters (not visual width)
        needed = total_len - len(name)
        pads = pad_char * needed
        # make pads occupy space but be invisible
        invisible_span = f'<span style="color:transparent; font-weight:normal">{pads}</span>'
        return f"<b>{name}</b> {invisible_span}"


# --------------------------------------------------------------------------------
# UI:
# --------------------------------------------------------------------------------

query: str | None = st.text_input(
    "Enter your search query", value=st.session_state["query"]
)

if st.button("Search"):
    if not query:
        st.warning("Please enter a search query.")
        st.stop()

    else:
        st.session_state["query"] = query
        with st.spinner("Fetching products..."):
            products: List[Product] = fetch_products_by_query(query)

            if products:
                st.session_state["products"] = products
                st.toast("Products fetched successfully!", icon="✅")
            else:
                st.warning("No products found for the given query.")


# Grid settings
products: List[Product] = st.session_state.get("products", [])
cols_per_row = 4
total = len(products)
rows = math.ceil(total / cols_per_row)

for row in range(rows):
    cols = st.columns(cols_per_row)
    
    
    for idx in range(cols_per_row):
        prod_index = row * cols_per_row + idx
        if prod_index >= total:
            break

        product = products[prod_index]
        with cols[idx]:
            # prod_container = st.container(horizontal=False, vertical_alignment='distribute', height=500)
            prod_container = st.container(horizontal=False, vertical_alignment='distribute', border=True)

            # Extract first image
            img = (product.image_url or "").split("|")[0]
            prod_container.image(img)

            # Name:
            # prod_container.markdown(format_name(product.name, max_len=60))
            formatted_html = format_name_html(product.name, total_len=80, pad_char="·")
            prod_container.markdown(formatted_html, unsafe_allow_html=True)


            # Price and Rating:
            p_sub_cont = prod_container.container(horizontal=True, horizontal_alignment='distribute')
            p_sub_cont.markdown(f"₹ {product.price}")
            p_sub_cont.markdown(f"⭐ {round(product.rating or 0, 1)} ({product.reviews_count or 0})")
            # st.markdown(f"₹ {product.price}  |  ⭐ {round(product.rating or 0, 1)}")

            # Buttons:
            cont = prod_container.container(horizontal=True, horizontal_alignment='distribute')
            # cont.link_button("🛒 Shop", product.url, use_container_width=True)
            cont.link_button("🛒 Shop", product.url)
            cont.button(":orange[AI Explaination]", key=f"btn_{idx}_{product.product_id}", icon="✨")
