from fastapi import FastAPI
from pydantic import BaseModel
from news_extraction import get_news_summary
from text_to_speech import text_to_speech_hindi

# Initialize FastAPI app
app = FastAPI()

# Define request model
class NewsRequest(BaseModel):
    company_name: str
    num_articles: int = 10  # Default to 10 articles

# Root endpoint 
@app.get("/")
def home():
    return {"message": "News Sentiment API is running!"}

# API endpoint to fetch news and sentiment analysis
@app.post("/fetch-news/")
def fetch_news(request: NewsRequest):
    result = get_news_summary(request.company_name, request.num_articles)

    # Convert each summary to Hindi
    for i, article in enumerate(result["articles"]):
        tts_file = f"tts_audio_{i}.mp3"
        text_to_speech_hindi(article["summary"], tts_file)
        article["tts_audio"] = tts_file  # Attach audio file name

    return result

# Running the API
# uvicorn api:app --host 0.0.0.0 --port 8000 --reload