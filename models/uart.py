from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class FPGAState(str, Enum):
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    OCCUPATON_UPDATE = "OCCUPATION_UPDATE"

class FPGAStatus(BaseModel):
    state : FPGAState
    rfid : int
    pin : int
    occupation : List[int]