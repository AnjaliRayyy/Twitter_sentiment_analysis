import streamlit as st
import preprocessor
import pickle
from xquik_import import XquikImportError, load_xquik_texts

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
st.caption("Optionally upload a Xquik CSV, JSON, or JSONL export.")
uploaded_export = st.file_uploader(
    "Upload Xquik export",
    type=["csv", "json", "jsonl"],
)
selected_import_text = ""

if uploaded_export is not None:
    try:
        imported_texts = load_xquik_texts(uploaded_export)
    except XquikImportError as error:
        st.error(f"Could not read this export: {error}")
    else:
        st.success(f"Loaded {len(imported_texts)} text item(s).")
        selected_import_text = st.selectbox(
            "Choose imported tweet",
            imported_texts,
            format_func=lambda value: value[:120],
        )

text = st.text_area("Enter your tweet text", selected_import_text, height=200)

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
