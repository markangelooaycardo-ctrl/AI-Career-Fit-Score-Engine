from sentence_transformers import SentenceTransformer
import faiss
import pickle
import json

print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded!")

faiss_index = None
job_data = None


def build_job_index_from_json(json_path="career_data.json", index_path="job_index.faiss", data_path="job_data.pkl"):
    global job_data

    with open(json_path, "r", encoding="utf-8") as f:
        job_data = json.load(f)

    print(f"Loaded {len(job_data)} careers from {json_path}")

    job_texts = []
    for job in job_data:
        title = job.get("Title", "")
        skills = job.get("Skills", "") or ""
        description = job.get("Description", "") or ""
        salary = job.get("Salary")

        if salary is not None:
            salary_str = f"Salary: PHP {salary:,.2f} per year"
        else:
            salary_str = "Salary: Not available"

        text = f"Title: {title}. Skills: {skills}. Description: {description}. {salary_str}"
        job_texts.append(text)

    print(f"Embedding {len(job_texts)} jobs...")
    job_vectors = model.encode(job_texts, show_progress_bar=True)
    faiss.normalize_L2(job_vectors)

    dimension = 384
    index = faiss.IndexFlatIP(dimension)
    index.add(job_vectors)
    faiss.write_index(index, index_path)

    with open(data_path, "wb") as f:
        pickle.dump(job_data, f)

    print(f"Index saved: {index_path} ({index.ntotal} jobs)")
    return index


def load_index(index_path="job_index.faiss", data_path="job_data.pkl"):
    global faiss_index, job_data
    faiss_index = faiss.read_index(index_path)
    with open(data_path, "rb") as f:
        job_data = pickle.load(f)
    print(f"Index loaded: {faiss_index.ntotal} jobs")


def search_matching_jobs(user_profile_text, top_k=5):
    query_vector = model.encode([user_profile_text])
    faiss.normalize_L2(query_vector)

    scores, indices = faiss_index.search(query_vector, top_k)

    results = []
    for i in range(top_k):
        job_idx = indices[0][i]
        score = scores[0][i]

        job = job_data[job_idx].copy()
        job['similarity_score'] = round(float(score) * 100, 2)
        results.append(job)

    return results


def get_top_job_matches(user_profile_dict, top_k=5):
    profile_text = (
        f"Skills: {user_profile_dict.get('Skills', '')}. "
        f"Preferred Work Location: {user_profile_dict.get('Preferred Work Location', '')}. "
        f"Academic Degree: {user_profile_dict.get('Academic Degree', '')}. "
        f"Field of Study: {user_profile_dict.get('Field of Study', '')}. "
        f"University Name: {user_profile_dict.get('University Name', '')}. "
        f"GPA: {user_profile_dict.get('GPA', '')}. "
        f"Previous Roles: {user_profile_dict.get('Previous Roles', '')}. "
        f"Years of Experience: {user_profile_dict.get('Years of Experience', '')}. "
        f"Previous Salary: {user_profile_dict.get('Previous Salary', '')}."
    )

    print (search_matching_jobs(profile_text, top_k=top_k))
    return search_matching_jobs(profile_text, top_k=top_k)


try:
    load_index()
except Exception as e:
    print("Warning: Could not auto-load index. Build it first using build_job_index_from_json().")

build_job_index_from_json("career_data.json", "job_index.faiss", "job_data.pkl")

print("\nDone. Files created:")
print("   1. embeddings_module.py")
print("   2. job_index.faiss")
print("   3. job_data.pkl")