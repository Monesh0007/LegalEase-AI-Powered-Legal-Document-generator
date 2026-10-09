# LegalEase AI — AI-Powered Legal Document Generator

LegalEase AI is a starter web app that helps users prepare **first drafts** of common legal documents from structured information. It uses Streamlit for the interface and can use the OpenAI API for AI-assisted drafting. Without an API key, it still creates a basic template draft.

> **Legal disclaimer:** This project is for educational and drafting assistance only. It does not provide legal advice, and it does not guarantee that a document is valid or enforceable. Laws differ by jurisdiction. A qualified lawyer should review any document before it is signed, sent, or relied on. Avoid entering sensitive personal or confidential information.

## Features

- Drafts for NDA, rental agreement, employment offer letter, general legal notice, and service agreement
- Structured fields to collect key details
- Optional OpenAI API integration
- Template fallback when no API key is configured
- Download generated draft as a Markdown file
- Environment variables for API configuration

## Requirements

- Python 3.10 or newer
- Optional OpenAI API key for AI mode

## Run locally

### 1. Clone your repository

```bash
git clone https://github.com/YOUR-USERNAME/LegalEase-AI-Powered-Legal-Document-generator.git
cd LegalEase-AI-Powered-Legal-Document-generator
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AI mode (optional)

Copy `.env.example` to `.env` and add your API key:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

Keep `.env` private. Never commit API keys to GitHub. If you do not configure a key, LegalEase uses the built-in template fallback.

### 5. Start the app

```bash
streamlit run app.py
```

Streamlit will show a local URL, usually `http://localhost:8501`.

## Push this project to GitHub

If you already created an empty GitHub repository:

```bash
git init
git add .
git commit -m "Initial LegalEase AI document generator"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/LegalEase-AI-Powered-Legal-Document-generator.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. If the repository already contains files, clone it first and copy these project files into that cloned folder to avoid overwriting existing work.

## Suggested next improvements

- Add user authentication and access controls
- Add DOCX/PDF export
- Add jurisdiction-specific templates reviewed by legal professionals
- Add secure storage only if genuinely needed, with retention and deletion controls
- Add automated tests and CI
- Add a clear privacy notice and rate limiting before public deployment

## Project structure

```text
LegalEase-AI-Powered-Legal-Document-generator/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
