import streamlit as st
from analysis_agent import AnalysisAgent
from review_fetcher import ReviewFetcher
from vector_db import VectorDB
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(page_title="Google Reviews Insight", layout="wide")
st.title(" Google Reviews Insight Dashboard")

# Load Claude API key
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

if not anthropic_api_key:
    st.error(" Missing required ANTHROPIC_API_KEY. Please set it in your environment.")
    logging.error("ANTHROPIC_API_KEY not set. Application stopped.")
    st.stop()

# Get Place ID (optional)
place_id = st.text_input("Enter Google Place ID:", "")

# Initialize components
fetcher = ReviewFetcher()
agent = AnalysisAgent(anthropic_api_key=anthropic_api_key)
vector_db = VectorDB()

# Step 1: Fetch Reviews (mock)
with st.spinner(" Fetching mock reviews..."):
    reviews = fetcher.fetch_reviews(place_id)
logging.info(f"Fetched {len(reviews)} mock reviews.")
st.success(f"Fetched {len(reviews)} reviews.")

# Step 2: Analyze Reviews
with st.spinner(" Analyzing reviews using Claude..."):
    analysis_results = agent.analyze_reviews(reviews)
logging.info("Completed review analysis using Claude.")

# Step 3: Display Sentiment Results
st.subheader(" Sentiment Analysis")
for i, (review, sentiment) in enumerate(zip(reviews, analysis_results["sentiments"]), 1):
    st.markdown(f"**{i}.** _{review['text']}_  **Sentiment:** `{sentiment}`")

# Step 4: Display Topics
st.subheader(" Extracted Topics")
flat_topics = sorted(set(topic for sublist in analysis_results["topics"] for topic in sublist))
st.write(", ".join(flat_topics))

# Optionally show topics per review
with st.expander("View Topics per Review"):
    for i, (review, topics) in enumerate(zip(reviews, analysis_results["topics"]), 1):
        st.markdown(f"**{i}.** _{review['text']}_  Topics: {', '.join(topics)}")

# Step 5: Display Summary
st.subheader("Summary & Action Items")
st.write(analysis_results["summary"])

# Step 6: Vector DB Storage
with st.spinner(" Storing reviews in vector database..."):
    vector_db.add_reviews(reviews)
    vector_db.persist()
logging.info("Reviews stored in vector DB.")
st.success(" Reviews stored successfully for semantic search.")

# Step 7: Semantic Search
query = st.text_input(" Search reviews semantically:", "")
if query:
    with st.spinner("Searching..."):
        results = vector_db.query(query)
    if results:
        st.subheader(" Search Results")
        for idx, res in enumerate(results, 1):
            st.markdown(f"**{idx}.** {res}")
        logging.info(f"Displayed {len(results)} semantic search results for query: '{query}'")
    else:
        st.info("No matching reviews found.")
        logging.info(f"No semantic search results found for query: '{query}'")
