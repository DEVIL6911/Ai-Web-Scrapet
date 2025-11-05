import requests
from bs4 import BeautifulSoup

def scrape_website(website):
    """Fetch website HTML using requests (works on Streamlit Cloud)."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; AI-WebScraper/1.0)"}
    response = requests.get(website, headers=headers)
    response.raise_for_status()
    return response.text

def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body_content = soup.body
    if body_content:
        return body_content.get_text(separator='\n', strip=True)
    return "No body content found."

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = '\n'.join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

def split_dom_content(dom_content, max_size=2000):
    return [dom_content[i:i+max_size] for i in range(0, len(dom_content), max_size)]
