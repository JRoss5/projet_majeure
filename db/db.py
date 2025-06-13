import json
from tinydb import TinyDB, Query
from models.db import RegisteredCar, ParkingStatus

from typing import List, Dict

class ParkingDB:
    def __init__(self, db_file : str, init_cars : List[RegisteredCar] = None):
        self.db = TinyDB(db_file)

        if init_cars is not None:
            for car in init_cars:
                self.add_car(car)

    def add_car(self, new_car : RegisteredCar):
        self.db.insert(new_car.__dict__)

    def remove_car_id(self, name):
        self.db.remove(Query().name == name)

    def update_car(self, name):
        pass

    def toggle_car_status_by_id(self, name : int):
        car : Query = Query()
        res = self.db.search(car.name == name)[0]
        res_car : RegisteredCar = RegisteredCar(**res)

        if(res_car.status == ParkingStatus.IN_GARAGE):
            self.db.update({'status': ParkingStatus.NOTIN_GARAGE}, car.name == name)
        else:
            self.db.update({'status': ParkingStatus.IN_GARAGE}, car.name == name)

    def toggle_car_status_by_pin(self, pin : int):
        car : Query = Query()
        res = self.db.search(car.pin == pin)[0]
        res_car : RegisteredCar = RegisteredCar(**res)

        if(res_car.status == ParkingStatus.IN_GARAGE):
            self.reset_car_status_by_pin(pin)
        else:
            self.set_car_status_by_pin(pin)
    
    def set_car_status_by_pin(self, pin : int):
        car : Query = Query()
        self.db.update({'status': ParkingStatus.IN_GARAGE}, car.pin == pin)

    def reset_car_status_by_pin(self, pin : int):
        car : Query = Query()
        self.db.update({'status': ParkingStatus.NOTIN_GARAGE}, car.pin == pin)

    def toggle_car_status_by_rfid(self, rfid : int):
        car : Query = Query()
        res = self.db.search(car.rfid == rfid)[0]
        res_car : RegisteredCar = RegisteredCar(**res)

        if(res_car.status == ParkingStatus.IN_GARAGE):
            self.db.update({'status': ParkingStatus.NOTIN_GARAGE}, car.rfid == rfid)
        else:
            self.db.update({'status': ParkingStatus.IN_GARAGE}, car.rfid == rfid)

    def set_car_status_by_rfid(self, rfid : int):
        car : Query = Query()
        self.db.update({'status': ParkingStatus.IN_GARAGE}, car.rfid == rfid)

    def reset_car_status_by_rfid(self, rfid : int):
        car : Query = Query()
        self.db.update({'status': ParkingStatus.NOTIN_GARAGE}, car.rfid == rfid)

    def get_car_by_id(self, name : int) -> RegisteredCar:
        car : Query = Query()
        res = self.db.search(car.name == name)
        print(res)
        return RegisteredCar(**res[0])

    def get_all(self) -> List[RegisteredCar]:
        car : Query = Query()

        return [RegisteredCar(**car) for car in self.db.search(car.status.matches('.*'))]
    
    def is_pin_registered(self, pin : int) -> bool:
        car : Query = Query()
        return len(self.db.search(car.pin == pin)) > 0

    def is_rfid_registered(self, rfid : int) -> bool:
        car : Query = Query()
        return len(self.db.search(car.rfid == rfid)) > 0



    