"""
WildGuard AI – Education Hub Router
Quizzes, daily facts, species of the day, conservation reports.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.education_service import (
    get_daily_fact,
    get_random_fact,
    get_quiz,
    get_species_of_the_day,
    generate_quiz_with_ai,
    generate_conservation_report,
)

router = APIRouter(prefix="/education", tags=["Education Hub"])


@router.get("/daily-fact")
async def daily_fact():
    """Get today's wildlife fact."""
    return get_daily_fact()


@router.get("/random-fact")
async def random_fact():
    """Get a random wildlife fact."""
    return get_random_fact()


@router.get("/quiz/{difficulty}")
async def quiz(difficulty: str = "beginner", count: int = 5):
    """Get a quiz at the given difficulty level (beginner/intermediate/expert)."""
    return get_quiz(difficulty, count)


@router.get("/species-of-the-day")
async def species_of_day():
    """Get an AI-generated Species of the Day profile."""
    return {"content": get_species_of_the_day()}


class QuizTopicRequest(BaseModel):
    topic: str
    difficulty: str = "intermediate"


@router.post("/custom-quiz")
async def custom_quiz(req: QuizTopicRequest):
    """Generate a custom AI-powered quiz on any wildlife topic."""
    return {"topic": req.topic, "quiz": generate_quiz_with_ai(req.topic, req.difficulty)}


class ReportRequest(BaseModel):
    topic: str


@router.post("/conservation-report")
async def conservation_report(req: ReportRequest):
    """Generate a conservation awareness report on any topic."""
    return {"topic": req.topic, "report": generate_conservation_report(req.topic)}
