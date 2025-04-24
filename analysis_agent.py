from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AnalysisAgent:
    def __init__(self, anthropic_api_key: str):
        self.llm = ChatAnthropic(model_name="claude-2", api_key=anthropic_api_key, temperature=0.5)
        logging.info("Initialized AnalysisAgent with Claude-2.")

        self.sentiment_prompt = PromptTemplate(
            input_variables=["review"],
            template="Classify the sentiment of this review as Positive, Negative, or Neutral. Respond with just one word:\n\n{review}"
        )

        self.topic_prompt = PromptTemplate(
            input_variables=["review"],
            template=(
                "From the following review, extract exactly 2 to 3 keywords or topics that summarize the main ideas. "
                "Return only a comma-separated list of keywords without any explanation.\n\n"
                "Review:\n{review}\n\nKeywords:"
            )
        )

        self.summary_prompt = PromptTemplate(
            input_variables=["reviews_summary"],
            template="Summarize the following reviews, highlighting key themes and action items in 3-5 lines:\n\n{reviews_summary}"
        )

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2))
    def safe_llm_call(self, prompt: str) -> str:
        try:
            result = self.llm.invoke(prompt)
            logging.info("Claude LLM call successful.")
            return result.content.strip()
        except Exception as e:
            logging.error(f"LLM call failed: {type(e).__name__} - {e}")
            raise e

    def analyze_sentiment(self, review: str) -> str:
        prompt = self.sentiment_prompt.format(review=review)
        return self.safe_llm_call(prompt)

    def extract_topics(self, review: str) -> List[str]:
        prompt = self.topic_prompt.format(review=review)
        topics_text = self.safe_llm_call(prompt)
        return [topic.strip() for topic in topics_text.split(",") if topic.strip()]

    def generate_summary(self, reviews_summary: str) -> str:
        prompt = self.summary_prompt.format(reviews_summary=reviews_summary)
        return self.safe_llm_call(prompt)

    def analyze_reviews(self, reviews: List[Dict]) -> Dict:
        sentiments, topics = [], []

        for review in reviews:
            text = review.get("text", "")
            if not text:
                continue
            sentiments.append(self.analyze_sentiment(text))
            topics.append(self.extract_topics(text))

        combined_summary_input = "\n".join([
            f"Review: {r.get('text', '')}\nSentiment: {s}\nTopics: {', '.join(t)}"
            for r, s, t in zip(reviews, sentiments, topics)
        ])
        summary = self.generate_summary(combined_summary_input)

        logging.info("Completed full review analysis.")
        return {
            "sentiments": sentiments,
            "topics": topics,
            "summary": summary
        }


if __name__ == "__main__":
    import os
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    agent = AnalysisAgent(anthropic_api_key=anthropic_key)
    sample_reviews = [
        {"text": "Great service and friendly staff."},
        {"text": "The product quality was poor and delivery was late."}
    ]

    results = agent.analyze_reviews(sample_reviews)
    logging.info(f"Sentiments: {results['sentiments']}")
    logging.info(f"Topics: {results['topics']}")
    logging.info(f"Summary:\n{results['summary']}")
