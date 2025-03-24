# 📄 Company News Summarization & Sentiment Analysis - README

## Project Overview
This project is a **web-based application** that extracts key details from multiple news articles related to a given company, performs **sentiment analysis**, conducts a **comparative analysis**, and generates a **Hindi text-to-speech (TTS) output**. Users can input a company name, and the application will provide a **structured sentiment report** along with **an audio summary**.

---
## 1. Project Setup

### Installation Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/Shivansh1123/News-sentiment-app.git
   cd News-sentiment-app
   ```

2. **Create a virtual environment (Optional but recommended)**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit Web App**
   ```bash
   streamlit run app.py
   ```

---
## 2. Model Details

### 🔹 Summarization Model
- **Method:** Extractive Summarization using `NLTK`
- **Purpose:** Extracts key points from long news articles.
- **Alternative Model:** Hugging Face Transformer models (`bert-extractive-summarizer`)

### 🔹 Sentiment Analysis Model
- **Model:** `VADER (Valence Aware Dictionary and sEntiment Reasoner)`
- **Library:** `NLTK`
- **Purpose:** Classifies news articles as **Positive, Neutral, or Negative**.
- **Why VADER?** Optimized for short texts like news articles.

### 🔹 Text-to-Speech (TTS) Model
- **Model:** `gTTS (Google Text-to-Speech)`
- **Language:** Hindi (`hi`)
- **Purpose:** Converts news summaries into **spoken Hindi audio**.

---
## 3. API Development

### 🔹 APIs Used in This Project
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/fetch_news?company={company_name}` | `GET` | Fetches news articles about a given company |
| `/analyze_sentiment` | `POST` | Analyzes sentiment of the provided text |
| `/generate_tts` | `POST` | Converts text to Hindi speech (MP3) |

### 🔹 How to Access APIs using Postman
1. **Start the API server**  
   ```bash
   python api.py
   ```
2. **Test API using Postman:**
   - **GET Request:** Fetch news for `Tesla`
     ```
     http://127.0.0.1:8000/fetch_news?company=Tesla
     ```
   - **POST Request:** Analyze sentiment
     ```
     Endpoint: http://127.0.0.1:8000/analyze_sentiment
     Body: { "text": "Tesla stock is performing well." }
     ```
   - **POST Request:** Generate Hindi speech
     ```
     Endpoint: http://127.0.0.1:8000/generate_tts
     Body: { "text": "यह टेस्ला की समाचार रिपोर्ट है।" }
     ```

### 🔹 Tech Stack
- **Frontend:** `Streamlit`
- **Backend:** `FastAPI`
- **Web Scraping:** `BeautifulSoup`
- **LLM/AI Models:** `VADER`, `gTTS`
- **APIs:** DuckDuckGo Search, Google TTS

---
## 4. API Usage

### DuckDuckGo Search API
- **Purpose:** Fetches news articles related to a company.
- **How it Works:** Uses `langchain_community.tools.DuckDuckGoSearchRun()`
- **Example Usage:**
  ```python
  from langchain_community.tools import DuckDuckGoSearchRun
  search = DuckDuckGoSearchRun()
  results = search.run("Tesla latest news")
  ```

### Google Text-to-Speech API (gTTS)
- **Purpose:** Converts summarized text into **Hindi speech**.
- **Example Usage:**
  ```python
  from gtts import gTTS
  tts = gTTS("यह टेस्ला की समाचार रिपोर्ट है।", lang='hi')
  tts.save("output.mp3")
  ```

### VADER Sentiment Analysis
- **Purpose:** Analyzes sentiment of news summaries.
- **Example Usage:**
  ```python
  from nltk.sentiment.vader import SentimentIntensityAnalyzer
  analyzer = SentimentIntensityAnalyzer()
  score = analyzer.polarity_scores("Tesla stock is rising")['compound']
  sentiment = "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"
  ```

---
## 5. Assumptions & Limitations

### 🔹 Assumptions
- **DuckDuckGo always returns relevant news articles**.
- **VADER sentiment analysis works well for short news snippets**.
- **Google TTS provides accurate Hindi speech output**.

### 🔹 Limitations
- **Web Scraping Issues**: Some news sites block automated scraping (CAPTCHAs).
- **Accuracy of Sentiment Analysis**: VADER is designed for short texts, so deep learning models (like BERT) would be better.
- **Speech Quality**: `gTTS` sometimes **mispronounces** complex words in Hindi.
- **Limited API Requests**: Third-party APIs (like NewsAPI) may **restrict free usage**.

### 🔹 Future Improvements
Use **LLM-based text summarization** instead of extractive summarization.
Add **multilingual support** for news articles in different languages.
Implement **advanced TTS models** like **Coqui.ai or VITS** for better Hindi voice quality.


## Conclusion
This project automates **news retrieval, sentiment analysis, and text-to-speech conversion**, making it easy for users to **get summarized news insights**. 

