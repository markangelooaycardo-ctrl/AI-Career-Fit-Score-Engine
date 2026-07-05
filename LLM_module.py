import json
import streamlit as st
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from huggingface_hub import InferenceClient

# Pydantic models for structured validation of the JSON output from the LLM
class JobRankItem(BaseModel):
    rank: int = Field(description="The numeric rank position from 1 to 5")
    job_title: str = Field(description="The title of the job")
    fit_score:  float = Field(description="The fit score for the job, from 0 to 100")
    reason: str =  Field(description="A brief explanation of why this job received its fit score")
    salary: Optional[float] =  Field(description="The salary for the job, if available")

class BestMatchItem(BaseModel):
    job_title: str = Field(description="The title of the job")
    fit_score: float = Field(description="The fit score for the job, from 0 to 100")
    why: str = Field(description="A brief explanation of why this job is a good match")
    matching_skills: List[str] = Field(description="List of skills that match the candidate's profile")
    missing_skills: List[str] = Field(description="List of skills that the candidate is missing but required for the job")
    recommendations: List[str] = Field(description="List of recommendations for improving fit for the selected career")

class CareerAssessmentSchema(BaseModel):
    best_career_match: BestMatchItem
    career_ranking: List[JobRankItem]


# Caching the InferenceClient to avoid re-initialization on every run
@st.cache_resource
def get_inference_client():
    return InferenceClient(
        model="Qwen/Qwen2.5-7B-Instruct",
        api_key=st.secrets["HF_TOKEN"]
    )

client = get_inference_client()

# Main function to generate career assessment using the LLM
def generate_career_assessment(profile, top5_jobs):
    
    # Using json.dumps on a dummy structure lets us pass a clean string blueprint to Qwen
    schema_blueprint = {
        "best_career_match": {
            "job_title": "string", "fit_score": 0.0, "why": "string",
            "matching_skills": ["string"], "missing_skills": ["string"], "recommendations": ["string"]
        },
        "career_ranking": [
            {"rank": 1, "job_title": "string", "fit_score": 0.0, "reason": "string", "salary": 0.0}
        ]
    }

    prompt = f"""
You are an AI Career Fit Scoring Engine. Your output must be a single, valid JSON object matching the exact key structures specified in this blueprint. Do not wrap text in markdown code blocks.

STUDENT PROFILE:
{profile}

TOP 5 RETRIEVED JOBS DATA:
{top5_jobs}

REQUIRED JSON STRUCTURE Blueprint:
{json.dumps(schema_blueprint, indent=2)}
"""

    # We call the regular text generation pipeline but force JSON output constraints
    response = client.chat_completion( messages=[{"role": "user", "content": prompt}],
                                      max_tokens=2048,
                                      temperature=0.1,
                                      response_format={"type": "json_object"})
    
    raw_text = response.choices[0].message.content

    try:
        # Load the raw text into a Python dictionary
        parsed_dict = json.loads(raw_text)
        
        # Feed the dictionary directly into Pydantic for structural validation!
        validated_object = CareerAssessmentSchema(**parsed_dict)
        print(validated_object.model_dump())
        return validated_object.model_dump()
        
    except (json.JSONDecodeError, ValidationError) as e:
        # In case Qwen skips a key or drops data, fallback safely
        st.error(f"Data mapping mismatch: {e}")
        return None