import requests
import re
import time
import streamlit as st
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq

# Initialize LLM (replace with your API key)
llm = ChatGroq(model='gemma2-9b-it', api_key='your_groq_api_key')

# Function to fetch news links
def get_news_links(company_name, num_articles=10):
    wrapper = DuckDuckGoSearchAPIWrapper(region='in-en', time='d')
    search = DuckDuckGoSearchResults(api_wrapper=wrapper, backend='news', num_results=num_articles, output_format='list')
    results = search.invoke(company_name + " latest news")

    # Remove unwanted sources
    filtered_results = [i for i in results if 'www.msn.com' not in i['link'] and 'www.business-standard.com' not in i['link']]
    return filtered_results[:num_articles]  # Limit to num_articles

# Function to extract content from different structures
def extract_article_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return None  # Skip if not accessible

        soup = BeautifulSoup(response.text, 'html.parser')

        # Try different extraction methods
        content = ""
        for tag in ['p', 'div', 'span', 'article', 'a']:  # Try common tags
            elements = soup.find_all(tag)
            text = ' '.join([el.get_text() for el in elements])
            if len(text) > 500:  # If valid content is found
                content = text
                break

        return content.strip()[:4000]  # Limit to 4000 characters
    except Exception as e:
        return None  # Return None if extraction fails

# Function to summarize content
def summarize_content(content):
    if not content:
        return "Summary unavailable."
    
    prompt = f"""Please summarize the following news content in 150 words.
                 Do not add any extra text.
                 <content>{content}</content>"""
    
    result = llm.invoke(prompt)
    time.sleep(1.5)
    
    return result.content.strip()

# Main function to fetch and process news
from sentiment_analysis import analyze_sentiment, compare_sentiments

def get_news_summary(company_name, num_articles=10):
    news_results = get_news_links(company_name, num_articles)
    articles = []

    for news in news_results:
        url = news['link']
        title = news['title']
        
        content = extract_article_content(url)
        if content:  # Only summarize if content was successfully extracted
            summary = summarize_content(content)
            sentiment, scores = analyze_sentiment(summary)
            
            articles.append({
                "title": title,
                "link": url,
                "summary": summary,
                "sentiment": sentiment,
                "scores": scores
            })

    sentiment_counts, overall_sentiment, coverage_differences = compare_sentiments(articles)

    return {
        "articles": articles,
        "sentiment_counts": sentiment_counts,
        "overall_sentiment": overall_sentiment,
        "coverage_differences": coverage_differences
    }


# Test the function
if __name__ == "__main__":
    company = "Tesla"
    articles = get_news_summary(company, 5)
    for article in articles:
        print(f"Title: {article['title']}\nSummary: {article['summary']}\nLink: {article['link']}\n\n")
