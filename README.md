# AI-Career-Fit-Score-Engine
An interactive RAG + LLM career assessment platform using Qwen-2.5 and O*NET data. Features a bulletproof Pydantic data validation pipeline and an intuitive Streamlit dashboard to analyze skill sets and career match rankings.

## Technologies Used

### Frontend
- Streamlit

### Backend
- Python

### Artificial Intelligence
- Hugging Face Inference API
- Qwen2.5-7B-Instruct

### Retrieval-Augmented Generation (RAG)
- FAISS (Facebook AI Similarity Search)
- Sentence Transformers (Embeddings)

### Data Source
- O*NET Web Services API

### Data Processing
- JSON
- NumPy
- Pandas
- Requests


## Features

- Interactive Streamlit Web Application
- Student Profile Collection
- Semantic Career Search using FAISS
- O*NET Occupation Retrieval
- AI Career Fit Assessment
- Top 5 Career Recommendations
- Best Career Match Identification
- Matching and Missing Skills Analysis
- Personalized Career Recommendations
- JSON-based AI Response Parsing

## System Architecture

```
                    +----------------------+
                    |    Streamlit UI      |
                    |  Student Interface   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Student Profile      |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Embedding Generation |
                    | SentenceTransformer  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   FAISS Vector Index |
                    | Semantic Search      |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Top 5 O*NET Careers  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Qwen2.5-7B-Instruct  |
                    | Career Assessment    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | JSON Career Analysis |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Streamlit Dashboard  |
                    +----------------------+
```
## Workflow

1. Student enters their academic and professional profile.
2. The profile is converted into vector embeddings.
3. FAISS performs semantic similarity search against indexed O*NET occupations.
4. The Top 5 most relevant careers are retrieved.
5. The retrieved careers and student profile are sent to the Qwen2.5-7B-Instruct model.
6. The AI generates:
   - Career Fit Scores
   - Best Career Match
   - Matching Skills
   - Missing Skills
   - Career Rankings
   - Recommendations
7. The results are returned as structured JSON and displayed through the Streamlit interface.


## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Vector Database | FAISS |
| Embedding Model | Sentence Transformers |
| LLM | Qwen2.5-7B-Instruct |
| AI Platform | Hugging Face Inference API |
| Career Database | O*NET Web Services API |
| Data Format | JSON |
