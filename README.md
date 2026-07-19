# 🐦 Twitter Sentiment Analysis App

A simple and interactive web application that analyzes the sentiment of user-provided text using a trained machine learning model. The app classifies text as **Positive** or **Negative** and is built using **Python** and **Streamlit**.

---

## 🚀 Features

- Analyze sentiment of custom text input
- Upload Xquik CSV, JSON, or JSONL exports and choose a tweet for analysis
- Uses classical NLP techniques (TF-IDF)
- Fast and lightweight ML model
- Clean and user-friendly Streamlit interface
- Stable (no external API dependencies)

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – Web interface
- **Scikit-learn** – Machine learning model
- **TF-IDF Vectorizer** – Text feature extraction
- **Pickle** – Model serialization

---

## 🧠 Model Overview

1. **Text Preprocessing**
   - Removes noise such as URLs, symbols, and extra spaces
   - Normalizes text for better feature extraction

2. **Feature Extraction**
   - TF-IDF (Term Frequency–Inverse Document Frequency) is used to convert text into numerical vectors

3. **Classification**
   - A supervised machine learning classifier predicts sentiment:
     - `Positive`
     - `Negative`

---

## 📦 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AnjaliRayyy/Twitter-sentiment-analysis.git
   cd Twitter-sentiment-analysis
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

4. Run parser tests:

   ```bash
   python -m unittest -v
   ```

---

## 📄 Requirements

Example `requirements.txt`:

```txt
streamlit
scikit-learn==1.7.2
```

---

## Xquik Export Uploads

Use the optional [Xquik](https://xquik.com) uploader when you already have an
export file. The parser
accepts CSV, JSON, and JSONL files and looks for common text fields such as
`text`, `full_text`, `tweet_text`, `content`, and nested `tweet.text` values.
After upload, choose an imported row and run it through the existing sentiment
model.

Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.

---

## ⚠️ Note on Twitter Data

Live Twitter fetching was intentionally removed due to recent Twitter (X) API restrictions and instability of scraping-based solutions.
This app focuses on **sentiment analysis of user-provided text**, ensuring reliability and consistent performance.

---

## 📈 Limitations

* Does not handle sarcasm or irony effectively
* Binary classification (no neutral sentiment)
* Performance depends on the quality of training data

---

## 🔮 Future Improvements

* Add a **neutral sentiment** class
* Support **CSV upload** for bulk analysis
* Integrate **transformer-based models** (e.g., BERT)
* Display **confidence scores**

---

## 🤝 Contributing

Contributions are welcome!  
If you have ideas for improvements or new features, feel free to:
- Fork the repository
- Create a new branch
- Submit a pull request

---

## 📜 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it.

---

## ⭐ Acknowledgements

* Scikit-learn documentation
* Streamlit community
* Open-source NLP resources
