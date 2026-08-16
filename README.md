# 🚀 CareerLens AI

**CareerLens AI** is an AI-powered Resume Analyzer and Job Match Platform that helps users analyze their resumes and understand how well their skills match a particular job.

## ✨ Features

* 🔐 User Registration & Login
* 📄 Resume Upload
* 🤖 AI-powered Resume Analysis
* 💼 Job Management
* 🎯 Resume & Job Matching
* 📊 Resume Analysis Results
* 🔍 Skill and Job Requirement Comparison
* ⚡ FastAPI Backend
* ⚛️ React Frontend

## 🛠️ Tech Stack

### Frontend

* React.js
* Vite
* HTML
* CSS
* JavaScript

### Backend

* Python
* FastAPI
* SQLAlchemy

### Database

* SQLite / configured database

### AI

* OpenAI API

### Tools

* VS Code
* Git
* GitHub

## 📁 Project Structure

```text
CareerLensAI/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── auth.py
│   ├── analysis.py
│   ├── job.py
│   ├── resume.py
│   ├── user.py
│   └── __init__.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/shwetasinalkar01/carrerlensai1.git
cd carrerlensai1
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key
```

**Never upload your `.env` file or API keys to GitHub.**

### 5. Start the backend

```bash
cd backend
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

## 🔑 Environment Variables

| Variable         | Description                                 |
| ---------------- | ------------------------------------------- |
| `OPENAI_API_KEY` | API key used for AI-powered resume analysis |

## 🎯 How It Works

1. Create an account.
2. Log in to CareerLens AI.
3. Upload your resume.
4. The system processes the resume.
5. Add or select a job.
6. The system compares your resume with the job requirements.
7. Receive AI-powered resume and job matching insights.

## 🔮 Future Improvements

* Advanced resume recommendations
* Automatic resume improvement suggestions
* Multiple resume formats
* Advanced job matching
* Job search integration
* Resume score history
* Personalized career recommendations
* Improved skill extraction
* Cloud database integration

## 👩‍💻 Author

**Shweta Sinalkar**

GitHub: https://github.com/shwetasinalkar01

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more information.
