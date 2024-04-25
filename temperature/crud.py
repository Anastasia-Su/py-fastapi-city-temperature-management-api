import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models as temperature_models
from city import models as city_models
from temperature.utils import create_temp_entries

from fastapi.responses import JSONResponse


async def get_temp_list(db: AsyncSession):
    query = select(temperature_models.DbTemperature)
    temp_list = await db.execute(query)
    return temp_list.scalars().all()


async def populate_temp_db(db: AsyncSession):
    async with httpx.AsyncClient() as client:
        query = select(city_models.DbCity)
        city_list = await db.execute(query)
        cities = city_list.scalars().all()

        for city in cities:
            temperature = await create_temp_entries(city=city, client=client)

            existing_entry = (
                await db.execute(
                    select(temperature_models.DbTemperature).filter(
                        temperature_models.DbTemperature.city_id == city.id
                    )
                )
            ).scalar_one_or_none()

            if existing_entry:
                existing_entry.date_time = temperature.date_time
                existing_entry.temperature = temperature.temperature

            else:
                db.add(temperature)

        await db.commit()
    return JSONResponse(content={"message": "Temperature entries updated successfully"})


#
# async def get_city_temp_detail(db: AsyncSession, city_id: int):
#     query = select(models.DbTemperature).filter(models.DbTemperature.city_id == city_id)
#     result = await db.execute(query)
#     city = result.scalars().first()
#     return [city] if city else []
