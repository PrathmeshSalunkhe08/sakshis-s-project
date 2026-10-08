from typing import List, Literal
from pydantic import BaseModel, Field


# 1. Model for fetched article data
class ArticleInput(BaseModel):
    url: str
    content: str
    fetch_status: str


# 2. Model for structured LLM insight output
class LLMArticleInsight(BaseModel):
    title: str
    summary: str
    topics: List[str]
    urgency_score: int = Field(..., ge=1, le=10)
    category: Literal["Tech", "Business", "Health", "Other"]