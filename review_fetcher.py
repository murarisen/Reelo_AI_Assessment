import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReviewFetcher:
    def __init__(self, api_key=None):
        self.api_key = api_key
        logging.info("ReviewFetcher initialized (mock mode).")

    def fetch_reviews(self, place_id=None, limit=50):
        """
        Return mock Google reviews data for testing purposes.

        Args:
            place_id (str): Ignored in mock.
            limit (int): Number of reviews to return (default 50).

        Returns:
            list: List of mock review dicts.
        """
        mock_reviews = [
            {"text": "Great service and friendly staff."},
            {"text": "The product quality was poor and delivery was late."},
            {"text": "Amazing experience, will come back again!"},
            {"text": "Not satisfied with the customer support."},
            {"text": "Loved the ambiance and the food was delicious."},
            {"text": "The wait time was too long, very disappointing."},
            {"text": "Staff was helpful and attentive."},
            {"text": "The product did not meet my expectations."},
            {"text": "Excellent value for money."},
            {"text": "I had issues with the billing process."},
            {"text": "Amazing ambiance and great coffee."},
            {"text": "The service was slow and staff were rude."},
            {"text": "Loved the pizza, will come again!"},
            {"text": "Too expensive for the quality offered."},
            {"text": "Friendly staff and clean environment."},
            {"text": "Great customer service and fast delivery."},
            {"text": "The food was cold and bland."},
            {"text": "Affordable and tasty meals."},
            {"text": "Had to wait 30 minutes for a table."},
            {"text": "Clean restrooms and well-maintained space."}
        ]
        logging.info(f"Fetched {min(limit, len(mock_reviews))} mock reviews.")
        return mock_reviews[:limit]

if __name__ == "__main__":
    fetcher = ReviewFetcher()
    reviews = fetcher.fetch_reviews()
    logging.info(f"Fetched {len(reviews)} mock reviews")
