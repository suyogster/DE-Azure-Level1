import requests
import json
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
API_KEY = os.getenv("API_KEY")
DATABASE_URI = os.getenv("DATABASE_URI")
CITY = "London"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

try:
    # Fetch weather data
    logger.info("Fetching weather data for %s", CITY)
    response = requests.get(URL)
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.json()
    logger.info("Weather data fetched successfully")

    # Pretty-print the JSON response
    print(json.dumps(data, indent=4))

    # Extract relevant fields
    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "timestamp": pd.to_datetime("now")
    }

    # Create a DataFrame
    df = pd.DataFrame([weather_info])
    print(df)

    # Database connection string
    if DATABASE_URI is None:
        raise ValueError("DATABASE_URI environment variable is not set")
    engine = create_engine(DATABASE_URI)

    # Insert data into the table
    df.to_sql("weather_data", engine, if_exists="append", index=False)
    logger.info("Data inserted successfully into the database")

except requests.exceptions.RequestException as e:
    logger.error("Error fetching data: %s", e)
except Exception as e:
    logger.error("An error occurred: %s", e)