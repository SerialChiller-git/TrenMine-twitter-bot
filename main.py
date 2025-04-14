from datetime import datetime, timezone
import os
import tweepy
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Take a screenshot of the page
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://trendmine.pages.dev/")
    page.screenshot(path="screenshot.png", full_page=True)
    browser.close()

# Load .env variables
load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")


def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client

client_v1 = get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret)
client_v2 = get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret)

media_path = "screenshot.png"
media = client_v1.media_upload(filename=media_path)
media_id = media.media_id
# Get current UTC time

now = datetime.now(timezone.utc)
formatted_time = now.strftime("%B %d, %Y – %I:%M %p UTC")
tweet_text =  f"""
🔥 Top 15 Trending Coins – Live market pulse as of {formatted_time}
Stay ahead of the curve with real-time trend detection 🚀

📈 Powered by #TrendMine  
🌐 https://trendmine.pages.dev
"""

client_v2.create_tweet(text=tweet_text, media_ids=[media_id])