from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas, crud
from dependencies import get_db
from temperature.utils import create_temp_entries

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temp])
async def read_temp_list_router(db: AsyncSession = Depends(get_db)):
    return await crud.get_temp_list(db=db)


@router.post("/temperatures/update", response_model=schemas.TempCreate)
async def read_temp_list_router(db: AsyncSession = Depends(get_db)):
    return await crud.populate_temp_db(db=db)
