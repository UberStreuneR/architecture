from fastapi import FastAPI, Depends, WebSocket
from fastapi.openapi.docs import (
    get_swagger_ui_html,
)

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from database import init_models, get_session
from exceptions import DuplicatedEntryError
import service
from typing import List, Union
import json

app = FastAPI(docs_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.14.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.14.0/swagger-ui.css",
    )


# @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
# async def swagger_ui_redirect():
#     return get_swagger_ui_oauth2_redirect_html()


@app.on_event("startup")
async def init_db_models():
    await init_models()
    print("Models initiated")


class CitySchema(BaseModel):
    name: str
    population: int

    class Config:
        orm_mode = True


@app.websocket("/cities/biggest")
async def get_biggest_cities_ws(websocket: WebSocket, session: AsyncSession = Depends(get_session)):
    await websocket.accept()
    cities = await service.get_biggest_cities(session)
    cities = [CitySchema.from_orm(city).dict() for city in cities]
    await websocket.send_json({"cities": cities})


@app.get("/cities/biggest", response_model=List[CitySchema])
async def get_biggest_cities(session: AsyncSession = Depends(get_session)):
    cities = await service.get_biggest_cities(session)
    return [CitySchema(name=city.name, population=city.population) for city in cities]


@app.post("/cities")
async def add_city(city: CitySchema, session: AsyncSession = Depends(get_session)):
    city = service.add_city(session, city.name, city.population)
    try:
        await session.commit()
        return city
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("The city is already stored")
