# Reelo AI Assessment
This is the combined README content.
# Review Insight Agent Prototype

## Overview
This prototype is an AI-powered tool to extract insights from Google Reviews for small businesses. It fetches reviews, analyzes sentiment and topics, generates summaries, stores semantic embeddings for retrieval, and visualizes insights on a dashboard. Weekly summaries can be sent to Notion via Zapier automation.

## Features
- Fetch Google Reviews using Outscraper API
- Sentiment analysis, topic extraction, and summary generation using LangChain and OpenAI APIs
- Semantic search with embeddings stored in Chroma Vector DB
- Interactive dashboard built with Streamlit
- Automated weekly summary delivery to Notion via Zapier webhook

## Setup Instructions

### Prerequisites
- Python 3.8+
- API keys for:
  - Outscraper API
  - OpenAI API
  - Zapier Webhook URL (for summary delivery)

### Installation
1. Clone the repository or copy the files.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set environment variables:

   On Unix/Linux/macOS (bash):
   ```
   export OUTSCRAPER_API_KEY="your_outscraper_api_key"
   export OPENAI_API_KEY="your_openai_api_key"
   export ANTHROPIC_API_KEY="your_anthropic_api_key"
   export ZAPIER_WEBHOOK_URL="your_zapier_webhook_url"
   ```

   On Windows (cmd):
   ```
   set OUTSCRAPER_API_KEY=your_outscraper_api_key
   set OPENAI_API_KEY=your_openai_api_key
   set ANTHROPIC_API_KEY=your_anthropic_api_key
   set ZAPIER_WEBHOOK_URL=your_zapier_webhook_url
   ```

### Running the Dashboard
```
streamlit run dashboard_app.py
```
Enter the Google Place ID to fetch and analyze reviews.

## Modules Description
- `review_fetcher.py`: Fetches Google reviews using Outscraper API.
- `analysis_agent.py`: Performs sentiment analysis, topic extraction, and summary generation.
- `vector_db.py`: Embeds and stores reviews in Chroma Vector DB for semantic search.
- `dashboard_app.py`: Streamlit app to visualize insights and perform semantic search.
- `zapier_notifier.py`: Sends weekly summaries to Zapier webhook for Notion integration.

## Deployment
- Host the Streamlit app on Replit or Vercel.
- Configure Zapier to trigger weekly and call the webhook with summary data.

## Future Improvements
- Add real-time review monitoring and alerting.
- Enhance topic modeling with advanced NLP techniques.
- Support multi-location or multi-service classification.
- Integrate more visualization options and user controls.

## Demo and Write-up
- Record a 2-4 minute video demo showcasing the tool and AI usage.
- Prepare a one-page write-up explaining approach, tools, challenges, and future plans.

---
This prototype demonstrates a lightweight, AI-powered workflow to help businesses gain actionable insights from their online reviews.
