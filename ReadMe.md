# Unthinkable Solutions - Assignment Project : 


| Sr. | Particular | Details |
|-----|------------|---------|
| 1.  | Name       | Sarvesh Nalawade |
| 2.  | Email ID   | nalawadesarvesh98@gmail.com |
| 3.  | Reg Number | 22BCE1575 | 
| 4.  | GitHub Repo | [Sarvesh-Nalawade/Unthinkable-Cosmetics-Shop](https://github.com/Sarvesh-Nalawade/Unthinkable-Cosmetics-Shop) |
| 5.  | Video Link | [Demo Video](https://drive.google.com/drive/folders/1YGSzRTdgRAmUAxV8jcEx12TUXNJWOEP8?usp=sharing) |


---


# E-commerce Product Recommendation System


[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=flat&logo=streamlit)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)



# 📖 About the Project
## Unthinkable Cosmetics Recommender System
This project is a complete E-commerce product search and recommendation system. It leverages modern machine learning techniques for semantic search and personalized recommendations. The backend is built with FastAPI, the frontend with Streamlit, and everything is containerized using Docker for easy setup and deployment.

The system combines **product recommendation logic** with **LLM-powered explanations**. It provides personalized product recommendations along with natural language explanations about why each product was suggested.

### Objective
- Provide users with relevant product recommendations.
- Explain the reasoning behind each recommendation using a Large Language Model (LLM).

1. Query: lipstick
  ![Dashboard Sample](https://cdn.jsdelivr.net/gh/Sarvesh-Nalawade/Unthinkable-Cosmetics-Shop/assets/lipstick.png)


1. Query: perfume
  ![Dashboard Sample](https://cdn.jsdelivr.net/gh/Sarvesh-Nalawade/Unthinkable-Cosmetics-Shop/assets/perfume.png)

3. Sample Recommendation Response
  ![Dashboard Sample](https://cdn.jsdelivr.net/gh/Sarvesh-Nalawade/Unthinkable-Cosmetics-Shop/assets/j2.png)

4. Code Snippet: Load index
  ![Dashboard Sample](https://cdn.jsdelivr.net/gh/Sarvesh-Nalawade/Unthinkable-Cosmetics-Shop/assets/load_index.png)
   
5. Code Snippet: Similarity Search
  ![Dashboard Sample](https://cdn.jsdelivr.net/gh/Sarvesh-Nalawade/Unthinkable-Cosmetics-Shop/assets/similarity_search.png)

---

## ✨ Features

- **Semantic Search**: Uses Sentence-Transformers to understand the meaning behind a user's query, going beyond simple keyword matching.
- **Personalized Re-ranking**: Ranks products based on inferred user preferences for brands, categories, and price points.
- **Popularity Boosting**: Highlights popular products by factoring in ratings and review counts.
- **RESTful API**: A FastAPI backend provides robust endpoints for product search and retrieval.
- **Interactive UI**: A Streamlit-based frontend offers a seamless and responsive user experience.
- **Containerized**: Easy one-command setup with Docker and Docker Compose.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, LangChain, FAISS, Sentence-Transformers, Pandas, Pydantic
- **Frontend**: Streamlit
- **Infrastructure**: Docker, Docker Compose
- **Language**: Python 3.11

---

## 📂 Project Structure

```text
.
├── Docker-Compose.yml
├── Dockerfile.backend
├── Dockerfile.ui
├── ReadMe.md
├── app.py                # Streamlit Frontend
├── config.py             # Configuration variables
├── create_vector_db.py   # Script to build the FAISS index
├── main.py               # FastAPI Backend
├── ranking.py            # Re-ranking logic
├── search_engine.py      # Core similarity search functions
├── requirements.txt
├── data/
│   └── ...
├── dataset/
│   └── Nykaa_Product_Review_Cleaned.csv
└── faiss_index/          # Generated vector index
```


## 🚀 Getting Started
This project is fully containerized, making setup quick and easy.

### Prerequisites
Docker installed and running.
Docker Compose (typically included with Docker Desktop).

### Installation & Running the Application
The entire application stack (backend and frontend) can be built and launched with a single command. The FAISS vector database is automatically created during the backend image build process.

### Clone the repository:

```bash
git clone https://github.com/Sarvesh-Nalawade/Unthinkable-Cosmetics-Shop.git
cd Unthinkable-Cosmetics-Shop
```
### Build
Run with Docker Compose: Execute the following command from the root of the project directory. This command will build the images and start the containers.
```bash
docker-compose up --build
```

## Access the application:

### Frontend UI: 
Open your browser and go to http://localhost:8501

### Backend API Docs: 
The interactive API documentation is available at http://localhost:8000/docs

## 🔧 Usage
### Search for Products: 
Navigate to the Streamlit UI and enter a product query like "lipstick" or "moisturizer for dry skin" in the search bar.

### View Recommendations: 
Recommended products will appear, ranked by relevance and personalization scores.

### Get AI Explanations: 
Each product includes an "AI Explanation" button. Clicking it will provide a reason why that specific product was recommended.

### Sample API Request
You can also query the backend API directly using tools like curl, Postman, or your browser.

### Request:

```
HTTP
GET http://localhost:8000/search?q=lipstick
```

### Sample Response:

```JSON
{
  "query": "lipstick",
  "category": null,
  "count": 20,
  "results": [
    {
      "rank": 1,
      "product_id": "5862930756fbef68849d9ba594ffd3ed",
      "name": "Givenchy Gentle Lipstick",
      "brand": "Givenchy",
      "category": "Lips",
      "price": 3050.0,
      "rating": 4.2,
      "reviews_count": 15,
      "image_url": "[https://images-static.nykaa.com/media/catalog/product/tr:w-276,h-276,cm-pad_resize/5/8/5862930756fbef68849d9ba594ffd3ed.jpg](https://images-static.nykaa.com/media/catalog/product/tr:w-276,h-276,cm-pad_resize/5/8/5862930756fbef68849d9ba594ffd3ed.jpg)",
      "url": "[https://www.nykaa.com/givenchy-rouge-interdit-vinyl-color-enhancing-lipstick/p/372033](https://www.nykaa.com/givenchy-rouge-interdit-vinyl-color-enhancing-lipstick/p/372033)",
      "score": 0.897
    }
  ]
}
```

## ⚙️ Running Services Individually (Optional)
If you prefer to run the services without Docker Compose, you can build and run each container separately.


### Backend Service
```bash
## Build the backend image
docker build -f Dockerfile.backend -t img-backend .
```

### Run the backend container
```bash
docker run -p 8000:8000 --name cont-backend img-backend
```

### Frontend Service
```bash
## Build the frontend image
docker build -f Dockerfile.ui -t img-frontend .
```

### Run the frontend container
```bash
docker run -p 8501:8501 --name cont-frontend img-frontend
```

## 🎬 Demo Video
[https://drive.google.com/drive/folders/1YGSzRTdgRAmUAxV8jcEx12TUXNJWOEP8?usp=sharing](https://drive.google.com/drive/folders/1YGSzRTdgRAmUAxV8jcEx12TUXNJWOEP8?usp=sharing)

## 📜 License
This project is for educational and demonstration purposes.