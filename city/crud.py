from http.client import HTTPResponse

from fastapi import HTTPException, status, Response
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas
from temperature.utils import create_temp_entries


async def get_city_list(db: AsyncSession):
    query = select(models.DbCity)
    city_list = await db.execute(query)

    return city_list.scalars().all()


async def get_city_detail(db: AsyncSession, city_id: int):
    query = select(models.DbCity).filter(models.DbCity.id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()
    return [city] if city else []


async def create_city(db: AsyncSession, city_create: schemas.CityCreate):
    query = insert(models.DbCity).values(
        name=city_create.name,
        additional_info=city_create.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city_create.model_dump(), "id": result.lastrowid}

    return resp


async def update_city(db: AsyncSession, city_id: int, city_update: schemas.CityCreate):
    city = await db.get(models.DbCity, city_id)

    if city:
        query = (
            update(models.DbCity)
            .where(models.DbCity.id == city_id)
            .values(
                name=city_update.name,
                additional_info=city_update.additional_info,
            )
        )
        await db.execute(query)
        await db.commit()
        return city_update

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"City with id {city_id} not found",
    )


async def delete_city(db: AsyncSession, city_id: int):
    city = await db.get(models.DbCity, city_id)

    if city:
        query = delete(models.DbCity).where(models.DbCity.id == city_id)
        await db.execute(query)
        await db.commit()
        return Response(status_code=status.HTTP_200_OK, content=f"Deleted: {city.name}")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"City with id {city_id} not found",
    )
