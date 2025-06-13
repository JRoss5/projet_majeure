from enum import Enum
from pydantic import BaseModel

class ParkingStatus(str, Enum):
    IN_GARAGE = "IN_GARAGE"
    NOTIN_GARAGE = "NOTIN_GARAGE"

class RegisteredCar(BaseModel):
    name : str
    rfid : int
    pin : int
    status : ParkingStatus