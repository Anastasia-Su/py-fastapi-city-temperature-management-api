import os
from datetime import datetime
from httpx import AsyncClient

from temperature import models as temperature_models
from city import models as city_models
from dotenv import load_dotenv

load_dotenv()


async def create_temp_entries(
    city: city_models.DbCity, client: AsyncClient
) -> temperature_models.DbTemperature:

    base_url = os.environ.get("BASE_URL")
    api_key = os.environ.get("API_KEY")

    params = {"key": api_key, "q": city.name}

    response = await client.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()

        current = weather_data.get("current")
        formatted_date = datetime.strptime(current["last_updated"], "%Y-%m-%d %H:%M")

        temperature_entry = temperature_models.DbTemperature(
            city_id=city.id, date_time=formatted_date, temperature=current["temp_c"]
        )

        return temperature_entry
