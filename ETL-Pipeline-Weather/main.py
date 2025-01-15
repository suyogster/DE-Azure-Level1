import requests
import json
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URI = os.getenv("DATABASE_URI")
CITY = "Barrie,CA"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

print(json.dumps(data, indent=4))  # Pretty-print the JSON response

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
engine = create_engine(DATABASE_URI) # type: ignore

# Insert data into the table
df.to_sql("weather_data", engine, if_exists="append", index=False)
print("Data inserted successfully!")