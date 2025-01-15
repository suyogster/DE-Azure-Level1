import tweepy
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

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

# Fetch tweets by user ID (commented out)
# user_id = "4398626122"  # Open AI
# tweets = client_v2.get_users_tweets(id=user_id, tweet_fields=["created_at", "entities"])

# Process and store tweets (commented out)
# for tweet in tweets.data: # type: ignore
#     data = {
#         "text": tweet.text,
#         "created_at": tweet.created_at,
#         "user_id": user_id,
#         "hashtags": [hashtag["tag"] for hashtag in tweet.entities["hashtags"]] if "hashtags" in tweet.entities else []
#     }
#     collection.insert_one(data)

# Dummy data for tweets
dummy_tweets = [
    {
        "text": "Excited to announce our latest breakthrough in AI technology! #AI #OpenAI",
        "created_at": "2023-10-01T12:00:00Z",
        "user_id": "4398626122",
        "hashtags": ["AI", "OpenAI"]
    },
    {
        "text": "Our new model can generate human-like text with unprecedented accuracy. #MachineLearning #Innovation",
        "created_at": "2023-10-02T13:00:00Z",
        "user_id": "4398626122",
        "hashtags": ["MachineLearning", "Innovation"]
    },
    {
        "text": "Join us for a webinar on the future of AI and its impact on various industries. #Webinar #FutureOfAI",
        "created_at": "2023-10-03T14:00:00Z",
        "user_id": "4398626122",
        "hashtags": ["Webinar", "FutureOfAI"]
    },
    {
        "text": "We are committed to ensuring AI benefits all of humanity. #EthicsInAI #OpenAI",
        "created_at": "2023-10-04T15:00:00Z",
        "user_id": "4398626122",
        "hashtags": ["EthicsInAI", "OpenAI"]
    },
    {
        "text": "Our team is constantly working to improve AI safety and reliability. #AISafety #Research",
        "created_at": "2023-10-05T16:00:00Z",
        "user_id": "4398626122",
        "hashtags": ["AISafety", "Research"]
    }
]

# Process and store dummy tweets
for tweet in dummy_tweets:
    collection.insert_one(tweet)

print("Dummy tweets inserted successfully!")

# Find the most common hashtags
pipeline = [
    {"$unwind": "$hashtags"},
    {"$group": {"_id": "$hashtags", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]
top_hashtags = list(collection.aggregate(pipeline))

for hashtag in top_hashtags:
    print(f"{hashtag['_id']}: {hashtag['count']} tweets")

    # Plot top hashtags
    hashtags = [hashtag["_id"] for hashtag in top_hashtags]
    counts = [hashtag["count"] for hashtag in top_hashtags]

    plt.bar(hashtags, counts)
    plt.xlabel("Hashtags")
    plt.ylabel("Number of Tweets")
    plt.title("Top Hashtags")
    plt.xticks(rotation=45)
    plt.show()