"""
This module provides integration with Zapier to automate sending
weekly review summaries to Notion (or any service) using a webhook.

Usage:
1. Initialize the ZapierNotifier with your Zapier webhook URL.
2. Call send_summary(summary_text) with the text you want to send.
"""

import requests
from typing import Optional
import datetime


class ZapierNotifier:
    def __init__(self, webhook_url: str):
        """
        Initialize with Zapier webhook URL.
        Args:
            webhook_url (str): The Zapier webhook URL to which the payload will be sent.
        """
        self.webhook_url = webhook_url

    def send_summary(self, summary: str, extra_info: Optional[dict] = None):
        """
        Send a review summary to the Zapier webhook.

        Args:
            summary (str): The summary text to send.
            extra_info (dict, optional): Additional metadata to send with the summary.
        """
        payload = {
            "summary": summary,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        if extra_info:
            payload.update(extra_info)

        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            print("Summary sent successfully to Zapier.")
        except requests.exceptions.RequestException as e:
            print(f"ailed to send summary: {e}")



if __name__ == "__main__":
    # Example usage (replace with your Zapier webhook URL)
    webhook_url = "https://hooks.zapier.com/hooks/catch/22617788/2xwmgta/"
    notifier = ZapierNotifier(webhook_url)

    test_summary = "Weekly review summary:\n- Positive feedback on staff friendliness\n- Issues with delivery delays"
    notifier.send_summary(test_summary)
