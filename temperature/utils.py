from datetime import datetime
import httpx
import os
from dotenv import load_dotenv
from temperature import models

load_dotenv()


async def create_temp_entries(city, client):
    base_url = os.environ.get("BASE_URL")
    api_key = os.environ.get("API_KEY")

    params = {"key": api_key, "q": city.name}

    response = await client.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        print("wdata", weather_data)

        current = weather_data.get("current")
        formatted_date = datetime.strptime(current["last_updated"], "%Y-%m-%d %H:%M")

        temperature_entry = models.DbTemperature(
            city_id=city.id, date_time=formatted_date, temperature=current["temp_c"]
        )

        return temperature_entry
