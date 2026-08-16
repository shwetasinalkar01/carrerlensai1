import os
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from google import genai

from database import SessionLocal
from models.resume import Resume
from models.job import Job
from models.analysis import Analysis
from routes.auth import get_current_user


load_dotenv()


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


class AnalysisRequest(BaseModel):
    resume_id: int
    job_id: int


@router.post("/")
def analyze_resume(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # current_user is a dictionary
    # Example:
    # {"id": 1, "email": "test@example.com"}

    user_id = current_user["id"]


    # =========================
    # FIND RESUME
    # =========================

    resume = db.query(Resume).filter(
        Resume.id == request.resume_id,
        Resume.user_id == user_id
    ).first()


    if not resume:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


    # =========================
    # FIND JOB
    # =========================

    job = db.query(Job).filter(
        Job.id == request.job_id,
        Job.user_id == user_id
    ).first()


    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )


    # =========================
    # GEMINI API KEY
    # =========================

    api_key = os.getenv("GEMINI_API_KEY")


    if not api_key:

        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured"
        )


    # =========================
    # RESUME FILE
    # =========================

    file_path = getattr(
        resume,
        "file_path",
        None
    )


    if not file_path:

        raise HTTPException(
            status_code=500,
            detail="Resume file path is missing"
        )


    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=404,
            detail=f"Resume file not found: {file_path}"
        )


    # =========================
    # GEMINI CLIENT
    # =========================

    client = genai.Client(
        api_key=api_key
    )


    try:

        # Upload resume PDF to Gemini
        resume_file = client.files.upload(
            file=file_path
        )


        # =========================
        # PROMPT
        # =========================

        prompt = f"""
You are an expert technical recruiter and career coach.

Analyze the candidate's resume against this job description.

JOB TITLE:
{job.title}

COMPANY:
{job.company or "Not specified"}

JOB DESCRIPTION:
{job.description}

Return ONLY valid JSON in this exact structure:

{{
    "match_score": 85,
    "matched_skills": [
        "Python",
        "FastAPI",
        "REST APIs"
    ],
    "missing_skills": [
        "Docker",
        "AWS"
    ],
    "recommendations": [
        "Add a backend deployment project",
        "Highlight REST API experience"
    ]
}}

Rules:

1. match_score must be an integer from 0 to 100.
2. matched_skills should contain skills found in both the resume and job.
3. missing_skills should contain important job skills that are missing or weak in the resume.
4. recommendations should be practical and specific.
5. Do not invent experience for the candidate.
6. Return ONLY JSON.
"""


        # =========================
        # GEMINI ANALYSIS
        # =========================

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=[
                resume_file,
                prompt
            ]
        )


        raw_result = response.text.strip()


        # Remove markdown code fences
        if raw_result.startswith("```"):

            raw_result = raw_result.replace(
                "```json",
                ""
            )

            raw_result = raw_result.replace(
                "```",
                ""
            )

            raw_result = raw_result.strip()


        # Convert AI response to Python dictionary
        result = json.loads(
            raw_result
        )


        # =========================
        # SAVE ANALYSIS
        # =========================

        analysis = Analysis(

            user_id=user_id,

            resume_id=request.resume_id,

            job_id=request.job_id,

            match_score=int(
                result["match_score"]
            ),

            matched_skills=", ".join(
                result.get(
                    "matched_skills",
                    []
                )
            ),

            missing_skills=", ".join(
                result.get(
                    "missing_skills",
                    []
                )
            ),

            recommendations="; ".join(
                result.get(
                    "recommendations",
                    []
                )
            )
        )


        db.add(analysis)

        db.commit()

        db.refresh(analysis)


        # =========================
        # RETURN RESULT
        # =========================

        return {

            "id": analysis.id,

            "match_score":
                analysis.match_score,

            "matched_skills":
                analysis.matched_skills,

            "missing_skills":
                analysis.missing_skills,

            "recommendations":
                analysis.recommendations
        }


    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail="AI returned an invalid analysis format"
        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )