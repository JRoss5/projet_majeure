import random
import threading
import queue
import json

import tkinter as tk

from typing import List

from gui.AppGUI import AppGUI
from db.db import ParkingDB
from models.db import RegisteredCar, ParkingStatus
from models.uart import FPGAStatus, FPGAState
from uart.uart import InfoReader

DB_PATH = 'data/car_db.json'

def check_uart():
    if(not uart_queue.empty()):
        queue_top : str = uart_queue.get()

        try:
            fs : FPGAStatus = FPGAStatus(**json.loads(queue_top))
            print(fs)

            match fs.state:
                case FPGAState.ENTRY:
                    if(db.is_pin_registered(fs.pin)):
                        db.set_car_status_by_pin(fs.pin)
                        ir.write_info("PIN found!\r\n")
                    elif(db.is_rfid_registered(fs.rfid)):
                        db.set_car_status_by_rfid(fs.rfid)
                        ir.write_info("RFID found!\r\n")
                    else:
                        ir.write_info("User not found!\r\n")
                        
                        
                case FPGAState.EXIT:
                    if(db.is_pin_registered(fs.pin)):
                        db.reset_car_status_by_pin(fs.pin)
                        ir.write_info("PIN found, exit!\r\n")
                    elif(db.is_rfid_registered(fs.rfid)):
                        db.reset_car_status_by_rfid(fs.rfid)
                        ir.write_info("RFID found, exit!\r\n")
                    else:
                        pass
                    
                case FPGAState.OCCUPATON_UPDATE:
                    gui.redraw_occupation_frame(fs.occupation)

            gui.redraw_db_tree_view()

        except TypeError:
            ir.write_info("NACK\r\n")

        uart_thread : threading.Thread = threading.Thread(target=ir.queue_next_info, args=[uart_queue])
        uart_thread.start()

    root.after(100, check_uart)

if __name__ == '__main__':
    # testcars : List[RegisteredCar] = []
    # for i in range(12):
    #     testcars.append(RegisteredCar(id=i, rfid=100*i, pin=(1234*i)%10000, status=random.choice(list(ParkingStatus))))

    # db : ParkingDB = ParkingDB(DB_PATH, testcars)
    # db.remove_car_id(1)

    ### Initialise thread to filter UART and queue through which it can communicate
    uart_queue : queue.Queue = queue.Queue()
    ir : InfoReader = InfoReader()
    uart_thread : threading.Thread = threading.Thread(target=ir.queue_next_info, args=[uart_queue])
    uart_thread.start()

    ### Initialise database and tkinter root from which to generate GUI
    db : ParkingDB = ParkingDB(DB_PATH)
    root : tk.Tk = tk.Tk()
    gui : AppGUI = AppGUI(root, db)

    root.after(100, check_uart)
    root.mainloop()


