
import json
import os

import pymupdf
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(
    page_title="Career Assistant",
    page_icon="🎯",
    layout="centered",
)

st.title("🎯 AI Career Assistant")
st.write(
    "Upload your resume and paste a job description "
    "to see how well your skills match the role."
)

resume_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
)

job_description = st.text_area(
    "Paste the job description",
    height=250,
    placeholder="Paste the full job description here...",
)

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


if st.button("Analyze my resume", type="primary"):
    if resume_file is None:
        st.error("Please upload a PDF resume.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    elif not os.getenv("OPENROUTER_API_KEY"):
        st.error("OPENROUTER_API_KEY was not found in your .env file.")
    else:
        try:
            with st.spinner("Analyzing your resume..."):
                # Extract text from the uploaded PDF
                pdf_bytes = resume_file.getvalue()

                with pymupdf.open(
                    stream=pdf_bytes,
                    filetype="pdf",
                ) as pdf:
                    resume = "\n".join(
                        page.get_text() for page in pdf
                    )

                if not resume.strip():
                    st.error(
                        "No selectable text was found in this PDF. "
                        "Try a text-based PDF rather than a scanned image."
                    )
                    st.stop()

                # Connect to OpenRouter
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=os.getenv("OPENROUTER_API_KEY"),
                )

                prompt = f"""
Extract skills from the resume and job description.

Resume:
{resume}

Job Description:
{job_description}

Return ONLY valid JSON in this format:
{{
    "resume_skills": [],
    "required_skills": []
}}

Rules:
- resume_skills: skills explicitly supported by the resume.
- required_skills: skills requested by the job description.
- Do not invent skills or experience.
- Do not include a match percentage.
- Do not wrap the JSON in Markdown code fences.
"""

                response = client.chat.completions.create(
                    model="openrouter/free",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                )

                result = response.choices[0].message.content

                if not result or not result.strip():
                    raise ValueError("The AI returned an empty response.")

                result = result.strip()

                if result.startswith("```"):
                    result = result.removeprefix("```json")
                    result = result.removeprefix("```")
                    result = result.removesuffix("```").strip()

                data = json.loads(result)

                # Validate the returned structure
                if not isinstance(data.get("resume_skills"), list):
                    raise ValueError("Invalid resume_skills in AI response.")

                if not isinstance(data.get("required_skills"), list):
                    raise ValueError("Invalid required_skills in AI response.")

                # Normalize skills before matching
                resume_skills = {
                    normalize_skill(skill)
                    for skill in data["resume_skills"]
                    if isinstance(skill, str)
                }

                required_skills = {
                    normalize_skill(skill)
                    for skill in data["required_skills"]
                    if isinstance(skill, str)
                }

                matching_skills = resume_skills & required_skills
                missing_skills = required_skills - resume_skills

                match_percentage = (
                    len(matching_skills) / len(required_skills) * 100
                    if required_skills else 0
                )

            # Display results
            st.subheader("Resume Match Results")

            st.metric(
                "Required skills matched",
                f"{match_percentage:.2f}%",
                f"{len(matching_skills)} of {len(required_skills)} skills",
            )

            st.progress(match_percentage / 100)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### ✅ Matching skills")
                if matching_skills:
                    for skill in sorted(matching_skills):
                        st.write(f"• {skill}")
                else:
                    st.write("No matching skills found.")

            with col2:
                st.markdown("#### 📌 Skills to develop")
                if missing_skills:
                    for skill in sorted(missing_skills):
                        st.write(f"• {skill}")
                else:
                    st.write("No missing skills identified.")

            with st.expander("View all extracted skills"):
                st.markdown("**Skills found in resume**")
                st.write(sorted(resume_skills))

                st.markdown("**Skills required by the job**")
                st.write(sorted(required_skills))

            st.caption(
                "This is an approximate skill-coverage score, "
                "not a guarantee of job suitability."
            )

        except json.JSONDecodeError:
            st.error(
                "The AI returned a response that wasn't valid JSON. "
                "Please try again."
            )
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")