from pathlib import Path
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import pymupdf
api_key = os.getenv("OPENROUTER_API_KEY")

load_dotenv()

client =OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

resume_input = input(
    "Enter resume PDF path (default: data/resume.pdf): "
).strip()

if not resume_input:
    resume_input = "data/resume.pdf"

resume_path = Path(resume_input)

job_description_path = input(
    "Enter job description file path (default: data/job_description.txt): "
).strip()

if not job_description_path:
    job_description_path = "data/job_description.txt"

job_description = Path(job_description_path).read_text(
    encoding="utf-8"
)

with pymupdf.open(resume_path) as pdf:
    resume = "\n".join(page.get_text() for page in pdf)


prompt= f"""
Extract skills from the resume and job description.

Resume:
{resume}

Job Description:
{job_description}

Do Not use Markdown.
Do NOT USE ```json.
Do NOT add any explanation before or after the JSON.
Return ONLY valid JSON object using exactly this structure:
{{
    "resume_skills": [],
    "required_skills": [],
}}
Rules:
- resume_skills: skills explicitly supported by the resume.
- required_skills: skills requested by the job description.
- Do not invent skills or experience.
- Do not include matching_skills or missing_skills.
- Do not include a match percentage.
- Do not wrap the JSON in Markdwon code fences.

"""

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

result= response.choices[0].message.content
#print("RAW response:\n")
#print(result)
data = json.loads(result)

def normalize_skill(skill):
    skill = skill.strip().lower()

    aliases = {
        "sklearn": "scikit-learn",
        "numpy library": "numpy",
        "pandas library": "pandas",
        "ml": "machine learning",
        "basic machine learning": "machine learning",
    }

    return aliases.get(skill, skill)

resume_skills ={
    skill.strip().lower()
    for skill in data["resume_skills"]
}

required_skills={
    skill.strip().lower()
    for skill in data["required_skills"]
}
matching_skills =resume_skills & required_skills
missing_skills =required_skills - resume_skills

match_percentage = (
    len(matching_skills)/ len(required_skills)* 100
    if required_skills else 0
) 

print("Resume Skills:", sorted(resume_skills))
print("Required Skills:", sorted(required_skills))
print("Matching Skills:", sorted(matching_skills))
print("Missing Skills:", sorted(missing_skills))
print("Match Percentage:", round(match_percentage, 2))
#print("RAW response:\n")
#print(result)

if not result or not result.strip():
    raise ValueError("The LLM returned an empty response.")

result = result.strip()

if result.startswith("```"):
    result = result.removeprefix("```json").removeprefix("```")
    result = result.removesuffix("```").strip()

data = json.loads(result)