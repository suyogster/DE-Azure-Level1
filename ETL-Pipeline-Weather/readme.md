# ETL Pipeline for Weather Data

This project demonstrates how to build an ETL (Extract, Transform, Load) pipeline to fetch weather data from an API, transform it, and load it into a database.

---

## **Step 1: Set Up Your Environment**

1. **Install Python**:

   - Download and install Python from [python.org](https://www.python.org/).

2. **Install Required Libraries**:

   - Use `pip` to install the following libraries:
     ```bash
     pip install requests pandas sqlalchemy
     ```
   - Libraries:
     - `requests`: To make HTTP requests to the weather API.
     - `pandas`: To manipulate and transform data.
     - `sqlalchemy`: To interact with the database.

3. **Set Up a Database**:
   - Install PostgreSQL locally or use a cloud-based database like Azure SQL Database.
   - Create a database and table to store weather data. Example table schema:
     ```sql
     CREATE TABLE weather_data (
         id SERIAL PRIMARY KEY,
         city VARCHAR(100),
         temperature FLOAT,
         humidity FLOAT,
         wind_speed FLOAT,
         timestamp TIMESTAMP
     );
     ```

---

## **Step 2: Extract Data from the Weather API**

1. **Sign Up for OpenWeatherMap API**:

   - Go to [OpenWeatherMap](https://openweathermap.org/api) and sign up for a free API key.

2. **Write Python Code to Fetch Data**:

   - Use the `requests` library to fetch weather data for a specific city.
   - Example code:

     ```python
     import requests
     import json

     API_KEY = "your_openweathermap_api_key"
     CITY = "London"
     URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

     response = requests.get(URL)
     data = response.json()

     print(json.dumps(data, indent=4))  # Pretty-print the JSON response
     ```

---

## **Step 3: Transform the Data**

1. **Extract Relevant Fields**:

   - Extract fields like temperature, humidity, wind speed, and city name from the JSON response.

2. **Clean and Format the Data**:

   - Use `pandas` to create a DataFrame and clean the data.
   - Example code:

     ```python
     import pandas as pd

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
     ```

---

## **Step 4: Load Data into the Database**

1. **Connect to the Database**:

   - Use `sqlalchemy` to connect to your PostgreSQL or Azure SQL Database.

2. **Insert Data into the Table**:

   - Example code:

     ```python
     from sqlalchemy import create_engine

     # Database connection string
     DATABASE_URI = "postgresql://username:password@localhost:5432/weather_db"
     engine = create_engine(DATABASE_URI)

     # Insert data into the table
     df.to_sql("weather_data", engine, if_exists="append", index=False)
     print("Data inserted successfully!")
     ```

---

## **Step 5: Automate the Pipeline**

1. **Schedule the Script**:

   - Use a task scheduler like **cron** (Linux/Mac) or **Task Scheduler** (Windows) to run the script at regular intervals (e.g., every hour).

2. **Add Error Handling**:
   - Add try-except blocks to handle API errors or database connection issues.
   - Example:
     ```python
     try:
         response = requests.get(URL)
         response.raise_for_status()  # Raise an error for bad status codes
     except requests.exceptions.RequestException as e:
         print(f"Error fetching data: {e}")
     ```

---

## **Step 6: Visualize the Data (Optional)**

1. **Connect Power BI or Tableau**:

   - Connect your database to Power BI or Tableau to create visualizations like:
     - Temperature trends over time.
     - Humidity vs. wind speed scatter plots.

2. **Example Dashboard**:
   - Create a dashboard showing real-time weather data for multiple cities.

---

## **Tools and Technologies Used**

- **API**: OpenWeatherMap
- **Programming Language**: Python
- **Libraries**: `requests`, `pandas`, `sqlalchemy`
- **Database**: PostgreSQL or Azure SQL Database
- **Scheduler**: cron or Task Scheduler
- **Visualization**: Power BI or Tableau (optional)

---

## **Next Steps**

1. **Expand the Project**:

   - Add more cities to the pipeline.
   - Store historical data and analyze trends.

2. **Deploy to the Cloud**:

   - Use Azure Data Factory or AWS Glue to orchestrate the pipeline.
   - Store data in Azure Blob Storage or AWS S3.

3. **Add Logging**:
   - Use Python’s `logging` module to log pipeline execution details.

---

## **Conclusion**

By completing this project, you’ll gain hands-on experience with:

- Building ETL pipelines.
- Working with APIs and databases.
- Automating data workflows.
