from fastapi import FastAPI,HTTPException
from db import hotel_db
from models import hotel_models

api= FastAPI()

from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
    "http://localhost", "http://localhost:8080", "https://g3m3-e9-hoteles-app.herokuapp.com",
]

api.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@api.get("/hoteles/resumen")
async def get_hoteles_api():
    return hotel_db.get_Hotels()

@api.post("/hotel")
async def auth_hotel(hotel_in: hotel_models.HotelIn): #email query param
    hotel_in_db = hotel_db.get_Hotel_email(hotel_in.email)

    if hotel_in_db ==None:
        raise HTTPException(status_code=404,detail="El hotel no existe")
    
    if hotel_in_db.password != hotel_in.password:

        return {"Autenticado": False}

    return {"Autenticado": True}

@api.get("/hotel/profile/{email}")
async def get_profile(email: str):
    
    hotel_in_db = hotel_db.get_Hotel_email(email)

    if hotel_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    hotel_out = hotel_models.HotelOut(**hotel_in_db.dict())

    return  hotel_out
    
@api.post("/hotel/agregar")
async def add_hotel(hotel_add: hotel_models.HotelAdd):
    hotel_add_db = hotel_db.enter_Hotel(hotel_add)

    if hotel_add_db:
        return {"Mensaje" : "Agregado satisfactoriamente"}
    else:
        raise HTTPException(status_code=400 , detail="El hotel ya existe en el db")


