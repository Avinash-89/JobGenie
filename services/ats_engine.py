# services/ats_engine.py
import os
import json
import httpx

def analyze_resume_vs_jd(resume_text: str, job_description: str) -> dict:
    """
    Evaluates a resume against a job description using an LLM API gateway.
    Returns a structured dictionary containing scoring metrics.
    """
    api_key = os.getenv("OPENAI_API_KEY", "your-fallback-mock-key")
    
    # Define a strict system prompt to guarantee clean JSON extraction
    system_prompt = (
        "You are an expert Enterprise ATS Scan Engine. Your task is to evaluate the provided resume text "
        "against the Job Description. You must respond ONLY with a valid JSON object matching this structure:\n"
        "{\n"
        '  "ats_score": 85,\n'
        '  "skills_matched": ["Python", "SQL"],\n'
        '  "skills_missing": ["Docker", "Kubernetes"],\n'
        '  "summary_critique": "Brief structured professional feedback summary here."\n'
        "}\n"
        "Do not include markdown code block backticks (```json) or conversational preamble."
    )
    
    user_prompt = f"--- JOB DESCRIPTION ---\n{job_description}\n\n--- RESUME TEXT ---\n{resume_text}"

    # For safety/mock-testing if no API key is provided
    if api_key == "your-fallback-mock-key":
        return {
            "ats_score": 72,
            "skills_matched": ["Python", "Streamlit", "SQLAlchemy"],
            "skills_missing": ["PostgreSQL Optimization", "Enterprise Security Architecture"],
            "summary_critique": "[MOCK MODE] Strong engineering fundamentals present, but missing deep cloud scaling infrastructure validation."
        }

    # Production API connection layer
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2
        }
        
        response = httpx.post("[https://api.openai.com/v1/chat/completions](https://api.openai.com/v1/chat/completions)", json=payload, headers=headers, timeout=30.0)
        response.raise_for_status()
        
        result_json = response.json()["choices"][0]["message"]["content"].strip()
        return json.loads(result_json)
        
    except Exception as e:
        # Resilient fallback state block
        return {
            "ats_score": 0,
            "skills_matched": [],
            "skills_missing": [],
            "summary_critique": f"AI Parsing pipeline encountered an execution error: {str(e)}"
        }