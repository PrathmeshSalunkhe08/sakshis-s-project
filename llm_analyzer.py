import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from models import LLMArticleInsight

load_dotenv()

# Initialize ChatGroq LLM
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# Enforce structured Pydantic output
structured_model = model.with_structured_output(LLMArticleInsight)


def analyze_article(content):
    """Sends article content to LLM and returns structured insight."""
    prompt = f"Analyze this news article and return key insights:\n\n{content[:3000]}"
    return structured_model.invoke(prompt)