from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_city_list_router(db: AsyncSession = Depends(get_db)):
    return await crud.get_city_list(db=db)


@router.get("/cities/{city_id}/", response_model=list[schemas.City])
async def read_city_detail_router(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_city_detail(city_id=city_id, db=db)


@router.post("/cities/", response_model=schemas.CityCreate)
async def create_city_router(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_city(db=db, city_create=city)


@router.put("/cities/{city_id}/", response_model=schemas.CityCreate)
async def update_city_router(
    city_id: int,
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.update_city(city_id=city_id, city_update=city, db=db)


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def delete_city_router(
    city_id: int,
    db: AsyncSession = Depends(get_db),
):
    city = await crud.get_city_detail(db, city_id)
    print("cty", city)
    return await crud.delete_city(city_id=city_id, db=db)
