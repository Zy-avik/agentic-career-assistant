# 🎯 AI Career Assistant

An LLM-powered career assistant that analyzes a resume against a job description, identifies matching and missing skills, and calculates a skill-coverage score to help job seekers understand their skill gaps.

## 🚀 Features

- **Resume Parsing:** Extracts text from PDF resumes using PyMuPDF.
- **AI-Powered Skill Extraction:** Uses a Large Language Model (LLM) to identify skills from resumes and job descriptions.
- **Skill Matching:** Compares resume skills with job requirements using Python sets.
- **Skill Gap Analysis:** Identifies matching skills and skills that may need further development.
- **Match Percentage:** Calculates an approximate skill-coverage score using Python.
- **Interactive Web Interface:** Provides a Streamlit interface for uploading a resume and entering a job description.
- **Environment Variable Support:** Loads API credentials securely from a local `.env` file.

## 🛠️ Tech Stack

- **Language:** Python
- **LLM API:** OpenRouter
- **LLM Client:** OpenAI Python SDK
- **Web Interface:** Streamlit
- **PDF Processing:** PyMuPDF
- **Environment Management:** python-dotenv
- **Version Control:** Git and GitHub

## ⚙️ How It Works

1. Upload a resume in PDF format.
2. Paste the target job description.
3. The LLM extracts the skills present in the resume and the skills required by the job.
4. Python normalizes and compares the extracted skills.
5. The application displays matching skills, missing skills, and an approximate skill-coverage percentage.

The matching percentage is calculated using:

`(Number of matching skills / Number of required skills) × 100`

This score represents skill coverage, not a prediction of hiring success.

## 📋 Prerequisites

- Python 3.10 or later
- An OpenRouter account and API key
- Git (optional, for cloning the repository)

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Zy-avik/agentic-career-assistant.git
cd agentic-career-assistant
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root and add:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Replace the placeholder with your own API key.

**Important:** Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
streamlit run src/app.py
```

Open the local URL displayed in the terminal, upload a PDF resume, paste a job description, and click **Analyze my resume**.

## 📁 Project Structure

```text
agentic-career-assistant/
├── src/
│   ├── app.py
│   └── main.py
├── data/
│   └── job_description.txt
├── .env                 # Local only; not committed
├── .gitignore
├── requirements.txt
└── README.md
```

The exact files in `src/` and `data/` may vary as the project evolves. Do not commit private resumes or API credentials.

## 🔮 Future Improvements

- More reliable skill extraction and normalization
- Better handling of API errors and malformed LLM responses
- Personalized learning recommendations based on skill gaps
- Job description analysis and role-specific preparation plans
- Resume improvement suggestions
- LLM tool calling and multi-step agent workflows
- Automated tests and improved evaluation of matching accuracy

## ⚠️ Limitations

- Skill extraction depends on the quality and consistency of the LLM response.
- The match percentage is an approximate skill-coverage measure.
- The application does not currently assess overall candidate suitability or guarantee job outcomes.
- Scanned PDFs without selectable text may require OCR support.

## 👨‍💻 About

This project is being developed as a hands-on learning project to explore Python, LLM APIs, prompt engineering, structured JSON outputs, PDF processing, and AI application development.

