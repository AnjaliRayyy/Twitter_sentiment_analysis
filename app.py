import streamlit as st
import preprocessor
import pickle

# Load model and vectorizer
model = pickle.load(open('sentiment_model.pkl', 'rb'))
tfidf = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Twitter Sentiment Analysis", layout="centered")
st.title("🐦 Twitter Sentiment Analysis")

# Hide Streamlit UI elements
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.write(
    "Analyze the sentiment of a tweet using a trained Machine Learning model."
)

# ---------------- TEXT INPUT MODE ----------------
text = st.text_area("Enter your tweet text", height=200)

if st.button("Analyze Sentiment"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        cleaned_text = preprocessor.clean_text(text)
        vectorized_text = tfidf.transform([cleaned_text])
        prediction = model.predict(vectorized_text)[0]

        if prediction == 1:
            st.success("😊 Positive Sentiment")
        else:
            st.error("☹️ Negative Sentiment")