import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 설정값 가져오기
api_key = os.getenv('API_KEY')
location = os.getenv('LOCATION')
start_date = os.getenv('START_DATE')
end_date = os.getenv('END_DATE')

def fetch_weather_data(api_key, location, date):
    url = "https://api.weatherapi.com/v1/history.json"
    params = {
        'key': api_key,
        'q': location,
        'dt': date
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'forecast' not in data:
        raise KeyError(f"Expected key 'forecast' not found in response: {data}")

    return pd.DataFrame(data['forecast']['forecastday'][0]['hour'])

def save_to_postgresql(df, conn):
    cur = conn.cursor()
    insert_query = """
        INSERT INTO my_schema.incheon_temperature (time, temperature)
        VALUES %s
    """
    values = [(row['time'], row['temp_c']) for index, row in df.iterrows()]
    execute_values(cur, insert_query, values)
    conn.commit()
    cur.close()

def main():
    # PostgreSQL connection setup
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    while current_date <= end_date_dt:
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"Fetching data for {date_str}")
        df = fetch_weather_data(api_key, location, date_str)
        save_to_postgresql(df, conn)
        current_date += timedelta(days=1)
    
    conn.close()

if __name__ == "__main__":
    main()
