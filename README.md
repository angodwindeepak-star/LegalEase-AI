# LegalEase

LegalEase is an AI-powered legal document drafting application.

## Features

- AI-powered legal document drafting
- FastAPI backend
- Streamlit frontend
- Gemini integration
- Editable document preview
- TXT export
- DOCX export
- PDF export
- Company logo support
- Terms table
- Local demo mode
- API health check
- Automated tests

---

## Project Structure

```text
LegalEase/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   │
│   └── services/
│       ├── __init__.py
│       └── gemini_generator.py
│
├── frontend/
│   ├── __init__.py
│   └── app.py
│
├── document_utils/
│   ├── __init__.py
│   ├── common.py
│   ├── docx_export.py
│   └── pdf_export.py
│
├── tests/
│   ├── test_api.py
│   └── test_exports.py
│
├── assets/
│   └── .gitkeep
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── pytest.ini
├── README.md
├── Dockerfile
└── docker-compose.yml