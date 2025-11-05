# 🕸️ AI Web Scraper  

An intelligent **web scraping and content parsing app** built with **Streamlit**, **Selenium**, and **Google Gemini (Flash Model) or ollama local model **.  
This tool allows you to extract, clean, and summarize website content automatically using the power of Gemini AI.

---

## 🚀 Features

- 🌐 Scrape website data using Selenium WebDriver  
- 🧠 Parse and summarize scraped data using **Google Gemini Flash API**  
- ⚡ Interactive web UI with **Streamlit**  
- 🧩 Modular Python structure for scalability  
- 🪶 Easy setup, runs locally or on cloud environments (Streamlit Cloud, Render, etc.)

---

## 🗂️ Project Structure
ai-web-scraper/
│
├── main.py # Main Streamlit app entry point
├── scrape.py # Handles website scraping logic (Selenium)
├── parse.py # Handles AI text parsing using Gemini API
├── requirements.txt # All required Python dependencies
├── cromedriver  # use according to your system requirement
│ └── secrets.toml # Stores Gemini API key for Streamlit (optional)
└── README.md # Project documentation




---

## ⚙️ Setup and Installation
python -m venv venv
# Activate it
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux

 
### 1️⃣ Clone this repository
```bash
git clone https://github.com/<your-username>/ai-web-scraper.git
cd ai-web-scraper

# fpr dependencies
pip install -r requirements.txt
GEMINI_API_KEY = "your_google_gemini_api_key_here"
add this Api key in your .env file

