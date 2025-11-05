import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_gemini

st.title("🕸️ AI Web Scraper ")

url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("🔄 Scraping the website...")
        try:
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)
            st.session_state.dom_content = cleaned_content

            with st.expander("View Extracted Content"):
                st.text_area("Cleaned DOM Content", cleaned_content, height=300)

        except Exception as e:
            st.error(f"Error scraping website: {e}")

# Step 2: Parse Content with Gemini
if "dom_content" in st.session_state:
    parse_description = st.text_area("🧠 Describe what you want to extract")

    if st.button("Parse Content"):
        if parse_description:
            st.write("✨ Parsing content using Gemini 2.5 Flash...")
            try:
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_gemini(dom_chunks, parse_description)
                st.success("✅ Parsing complete!")
                st.text_area("Parsed Result", parsed_result, height=300)
            except Exception as e:
                st.error(f"Error parsing with Gemini: {e}")
