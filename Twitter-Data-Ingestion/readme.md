# Data Ingestion from Social Media

This project demonstrates how to build a pipeline to collect data from a social media platform (e.g., Twitter), store it in a NoSQL database, and analyze trends.

---

## **Step 1: Set Up Your Environment**

1. **Install Python**:

   - Download and install Python from [python.org](https://www.python.org/).

2. **Install Required Libraries**:

   - Use `pip` to install the following libraries:
     ```bash
     pip install tweepy pandas pymongo python-dotenv
     ```
   - Libraries:
     - `tweepy`: To interact with the Twitter API.
     - `pandas`: To manipulate and analyze data.
     - `pymongo`: To interact with MongoDB.
     - `python-dotenv`: To load environment variables from a `.env` file.

3. **Set Up MongoDB**:
   - Install MongoDB locally or use a cloud-based solution like MongoDB Atlas or Azure Cosmos DB.
   - Create a database and collection to store tweets. Example:
     ```bash
     use twitter_db
     db.createCollection("tweets")
     ```

---

## **Step 2: Extract Data from Twitter**

1. **Create a Twitter Developer Account**:

   - Go to [Twitter Developer](https://developer.twitter.com/) and create a developer account.
   - Create an app to get your API keys (`API Key`, `API Secret Key`, `Access Token`, `Access Token Secret`, and `Bearer Token`).

2. **Create a `.env` File**:

   - In the root directory of your project, create a file named `.env`.
   - Add your API keys and MongoDB URI to the `.env` file:
     ```
     TWITTER_BEARER_TOKEN=your_bearer_token
     MONGO_URI=your_mongo_uri
     ```

3. **Write Python Code to Fetch Tweets**:

   - Use the `tweepy` library to fetch tweets by user ID.
   - Example code:

     ```python
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
     user_id = "user_id_here"  # Replace with the actual user ID
     tweets = client_v2.get_users_tweets(id=user_id, tweet_fields=["created_at", "entities"], max_results=50)

     # Process and store tweets
     for tweet in tweets.data:
         data = {
             "text": tweet.text,
             "created_at": tweet.created_at,
             "user_id": user_id,
             "hashtags": [hashtag["tag"] for hashtag in tweet.entities["hashtags"]] if "hashtags" in tweet.entities else []
         }
         collection.insert_one(data)

     print("Tweets fetched and stored successfully!")
     ```

---

## **Step 3: Transform the Data**

1. **Extract Relevant Fields**:

   - Extract fields like `text`, `created_at`, `user_id`, and `hashtags` from the tweets.

2. **Clean and Format the Data**:

   - Use `pandas` to create a DataFrame and clean the data.
   - Example code:

     ```python
     import pandas as pd

     # Extract relevant fields
     tweet_data = []
     for tweet in tweets.data:
         tweet_info = {
             "text": tweet.text,
             "created_at": tweet.created_at,
             "user_id": user_id,
             "hashtags": [hashtag["tag"] for hashtag in tweet.entities["hashtags"]] if "hashtags" in tweet.entities else []
         }
         tweet_data.append(tweet_info)

     # Create a DataFrame
     df = pd.DataFrame(tweet_data)
     print(df.head())
     ```

---

## **Step 4: Load Data into MongoDB**

1. **Connect to MongoDB**:

   - Use `pymongo` to connect to your MongoDB instance.

2. **Insert Data into the Collection**:

   - Example code:

     ```python
     from pymongo import MongoClient

     # MongoDB connection string
     MONGO_URI = "mongodb://localhost:27017/"
     client = MongoClient(MONGO_URI)

     # Connect to the database and collection
     db = client["twitter_db"]
     collection = db["tweets"]

     # Insert data into the collection
     records = df.to_dict("records")
     collection.insert_many(records)
     print("Data inserted successfully!")
     ```

---

## **Step 5: Analyze Trends**

1. **Query the Database**:

   - Use MongoDB queries to analyze trends (e.g., most common hashtags).
   - Example query:

     ```python
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
     ```

2. **Visualize Trends (Optional)**:

   - Use `matplotlib` or `seaborn` to create visualizations like bar charts or word clouds.
   - Example code:

     ```python
     import matplotlib.pyplot as plt

     # Plot top hashtags
     hashtags = [hashtag["_id"] for hashtag in top_hashtags]
     counts = [hashtag["count"] for hashtag in top_hashtags]

     plt.bar(hashtags, counts)
     plt.xlabel("Hashtags")
     plt.ylabel("Number of Tweets")
     plt.title("Top Hashtags")
     plt.xticks(rotation=45)
     plt.show()
     ```

---

## **Step 6: Automate the Pipeline**

1. **Schedule the Script**:

   - Use a task scheduler like **cron** (Linux/Mac) or **Task Scheduler** (Windows) to run the script at regular intervals (e.g., every hour).

2. **Add Error Handling**:
   - Add try-except blocks to handle API errors or database connection issues.
   - Example:
     ```python
     try:
         tweets = client_v2.get_users_tweets(id=user_id, tweet_fields=["created_at", "entities"], max_results=50)
     except tweepy.TweepError as e:
         print(f"Error fetching tweets: {e}")
     ```

---

## **Tools and Technologies Used**

- **API**: Twitter API
- **Programming Language**: Python
- **Libraries**: `tweepy`, `pandas`, `pymongo`, `python-dotenv`
- **Database**: MongoDB or Azure Cosmos DB
- **Visualization**: `matplotlib` or `seaborn` (optional)

---

## **Next Steps**

1. **Expand the Project**:

   - Fetch tweets from multiple keywords or hashtags.
   - Store historical data and analyze trends over time.

2. **Deploy to the Cloud**:

   - Use Azure Functions or AWS Lambda to run the pipeline in the cloud.
   - Store data in Azure Cosmos DB or MongoDB Atlas.

3. **Add Logging**:
   - Use Python’s `logging` module to log pipeline execution details.

---

## **Conclusion**

By completing this project, you’ll gain hands-on experience with:

- Working with APIs.
- Storing and querying data in NoSQL databases.
- Analyzing and visualizing social media trends.
