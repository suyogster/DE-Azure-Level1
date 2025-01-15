import tweepy
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")

# Set up Twitter API client
client_v2 = tweepy.Client(bearer_token=BEARER_TOKEN)

# Set up MongoDB client
client = MongoClient(MONGO_URI)
db = client.twitter_db
collection = db.tweets

# Fetch tweets by user ID
user_id = "4398626122"  # Open AI
tweets = client_v2.get_users_tweets(id=user_id, tweet_fields=["created_at", "entities"], max_results=1)

# Process and store tweets
for tweet in tweets.data: # type: ignore
    data = {
        "text": tweet.text,
        "created_at": tweet.created_at,
        "user_id": user_id,
        "hashtags": [hashtag["tag"] for hashtag in tweet.entities["hashtags"]] if "hashtags" in tweet.entities else []
    }
    collection.insert_one(data)

print("Tweets fetched and stored successfully!")