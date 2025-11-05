import selenium.webdriver as webdriver
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import time


def scrape_website(website):
    print("Launching chrome browser... ")


    chrome_driver_path = "./chromedriver.exe"  # it is a application that allow us to control chrome
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service = Service(chrome_driver_path) , options=options)

    try:
        driver.get(website) 
        print("Page Loaded...")
        html = driver.page_source
        time.sleep(15) 

        return html
    finally:
        driver.quit()    
def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body_content = soup.body
    if body_content:
        return body_content.get_text(separator='\n', strip=True)
    return "No body content found."
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    
    # Remove script and style tags
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()
    
    # These lines should be OUTSIDE the for loop (unindent them)
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = '\n'.join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    
    return cleaned_content
def split_dom_content(dom_content, max_size=2000):
    return [dom_content[i:i+max_size] for i in range(0, len(dom_content), max_size)]

# def split_dom_content(dom_content,max_size =7000):
#     return [
#         dom_content[i:i+max_size] for i in range (len(dom_content),max_size)
#     ]
          