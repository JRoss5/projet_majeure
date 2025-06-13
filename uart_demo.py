import serial
import random
from time import sleep
from typing import List, Dict

class GarageUser:
    def __init__(self, name, pin, rfid, place):
        self.name = name
        self.pin = pin
        self.rfid = rfid
        self.place = place

ser : serial.Serial = serial.Serial("/dev/pts/4", 9600, timeout=1)

paul : GarageUser = GarageUser("Paul",1234,4321,-1)
lisa : GarageUser = GarageUser("Lisa",2345,5432,-1)
gabriel : GarageUser = GarageUser("Gabriel",3456,6543,-1)
george : GarageUser = GarageUser("George",4567,7654,-1)
alex : GarageUser = GarageUser("Alex",5678,8765,-1)
albert : GarageUser = GarageUser("Albert",6789,9876,-1)

# usr_dict : Dict[str, tuple[int, int, int]] = {"Paul":(1234,4321,-1),
#                                               "Lisa":(2345,5432,-1),
#                                               "Gabriel":(3456,6543,-1),
#                                               "George":(4567,7654,-1),
#                                               "Alex":(5678,8765,-1),
#                                               "Albert":(6789,9876,-1)}

usr_dict : Dict[str, GarageUser] = {"Paul": paul,
                                    "Lisa": lisa,
                                    "Gabriel": gabriel,
                                    "George": george,
                                    "Alex": alex,
                                    "Albert": albert}

people_in_garage : List[str] = []
people_outside_garage : List[str] = list(usr_dict.keys())

NUMBER_OF_SPOTS = 16
unoccupied_spots : List[int] = list(range(NUMBER_OF_SPOTS))
occupation_list : List[int] = [0 for x in range(NUMBER_OF_SPOTS)]

with ser as s:
    while True:
        # input("press enter to try next user")
        sleep(1)
        #flip a coin to decide if someone tries to enter or leave the garage
        if(random.randint(0,1) == 0 and len(people_outside_garage) > 0):
            #random person who is not yet in garage tries to enter garage
            waiting_person : str = random.choice(people_outside_garage)
            print(f"trying to park: {waiting_person}")

            #person enters garage
            ser.write(bytes(f"{{\"state\":\"ENTRY\",\"rfid\":{usr_dict[waiting_person].rfid},\"pin\":{usr_dict[waiting_person].pin},\"occupation\":{occupation_list}}}", "utf-8"))

            resp : str = str(ser.readline(), encoding="utf-8").strip()
            if(resp == "PIN found!" or resp == "RFID found!"):
                print(f"parking: {waiting_person}")
                #if person is let in, they choose random spot in garage
                people_outside_garage.remove(waiting_person)
                parking_spot : int = random.choice(unoccupied_spots)
                unoccupied_spots.remove(parking_spot)
                usr_dict[waiting_person].place = parking_spot
                occupation_list[parking_spot] = 1
                sleep(0.1)
                ser.write(bytes(f"{{\"state\":\"OCCUPATION_UPDATE\",\"rfid\":{usr_dict[waiting_person].rfid},\"pin\":{usr_dict[waiting_person].pin},\"occupation\":{occupation_list}}}", "utf-8"))
                people_in_garage.append(waiting_person)
            else:
                print(f"not in database: {waiting_person} (resp: {resp})")
            
        elif(len(people_in_garage) > 0):
            #random person in garage tries to leave
            leaving_person : str = random.choice(people_in_garage)

            #person leaves their parking spot
            people_in_garage.remove(leaving_person)
            parking_spot : int = usr_dict[leaving_person].place
            occupation_list[parking_spot] = 0
            unoccupied_spots.append(parking_spot)
            ser.write(bytes(f"{{\"state\":\"OCCUPATION_UPDATE\",\"rfid\":{usr_dict[leaving_person].rfid},\"pin\":{usr_dict[leaving_person].pin},\"occupation\":{occupation_list}}}", "utf-8"))

            sleep(0.1)

            #person leaves the garage
            people_outside_garage.append(leaving_person)
            ser.write(bytes(f"{{\"state\":\"EXIT\",\"rfid\":{usr_dict[leaving_person].rfid},\"pin\":{usr_dict[leaving_person].pin},\"occupation\":{occupation_list}}}", "utf-8"))

            print(f"leaving: {leaving_person}")