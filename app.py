import streamlit as st # type: ignore
import requests # type: ignore

# Set FastAPI URL
API_URL = "http://127.0.0.1:8000/fetch-news/"

st.title("🔍 Company News Sentiment Analyzer")

# User input for company name
company_list = ["Tesla", "Microsoft", "Google", "Reliance", "Adani"]
selected_company = st.selectbox("Choose a company:", company_list)
custom_input = st.text_input("Or enter another company:")

# Decide final input
if custom_input:
    company_name = custom_input
else:
    company_name = selected_company

if st.button("Fetch News"):
    st.write(f"Fetching latest news for **{company_name}**...")
    response = requests.post(API_URL, json={"company_name": company_name, "num_articles": 5})

    if response.status_code == 200:
        result = response.json()

        st.subheader("📊 Sentiment Analysis Summary")
        st.write(f"**Overall Sentiment:** {result['overall_sentiment']}")
        st.write(f"**Sentiment Distribution:** {result['sentiment_counts']}")

        for article in result["articles"]:
            st.subheader(article["title"])
            st.write(f"📝 **Summary:** {article['summary']}")
            st.write(f"📊 **Sentiment:** {article['sentiment']}")
            st.markdown(f"[🔗 Read More]({article['link']})")

            # Play Hindi TTS
            audio_file = article["tts_audio"]
            if audio_file:
                st.audio(audio_file, format="audio/mp3")
                st.download_button(label="Download Audio", data=open(audio_file, "rb"), file_name=audio_file)

        st.subheader("🔎 Coverage Differences")
        for diff in result["coverage_differences"]:
            st.write(f"🧐 **Comparison:** {diff['Comparison']}")
            st.write(f"⚖ **Impact:** {diff['Impact']}")
    else:
        st.write("Error fetching news data.")


