import tkinter as tk
from tkinter import ttk

from typing import List, Dict

from db.db import ParkingDB
from models.db import RegisteredCar, ParkingStatus
from gui.CarButton import CarButton

class AppGUI:
    def __init__(self, root : tk.Tk, db : ParkingDB, parking_rows=4, parking_cols=3, max_spaces=10):

        self.db = db
        self.max_spaces = max_spaces
        self._buttons_ : Dict[int, CarButton] = {}
        self._parking_subframes_ : Dict[int, ttk.Frame] = {}
        self._buffer_subframes_ : Dict[int, ttk.Frame] = {}
        
        root.title("Gestion Parking")

        self.main_notebook : ttk.Notebook = ttk.Notebook(root)
        self.occupation_frame : ttk.Frame = ttk.Frame(self.main_notebook, padding=(3, 3, 12, 12))
        self.occupation_frame.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))

        self.mgmt_frame : ttk.Frame = ttk.Frame(self.main_notebook, padding=(3, 3, 12, 12))

        self.db_tree : ttk.Treeview = ttk.Treeview(self.mgmt_frame, columns=("pin", "rfid", "status"))
        self.db_tree.heading('#0', text="Nom")
        self.db_tree.heading("pin", text="PIN")
        self.db_tree.heading("rfid", text="RFID")
        self.db_tree.heading("status", text="Status")
        self.db_tree.column('#0', width=100, anchor='center')
        self.db_tree.column("pin", width=100, anchor='center')
        self.db_tree.column("rfid", width=100, anchor='center')
        self.db_tree.column("status", width=100, anchor='center')
        self.db_tree.grid(column=0, row=0)

        self.delete_frame : ttk.Frame = ttk.Frame(self.mgmt_frame)
        self.delete_button : ttk.Button = ttk.Button(self.delete_frame, text="Supprimer Selection", command=self.delete_car_selection)
        self.delete_button.grid(column=0, row=0)
        self.delete_frame.grid(column=0, row=1)

        self.entry_frame : ttk.Frame = ttk.Frame(self.mgmt_frame)
        self.entry_subframe : ttk.Frame = ttk.Frame(self.entry_frame)
        ENTRY_WIDTH = 5
        self.id_entry : ttk.Entry = ttk.Entry(self.entry_subframe, width=ENTRY_WIDTH)
        self.pin_entry : ttk.Entry = ttk.Entry(self.entry_subframe, width=ENTRY_WIDTH)
        self.rfid_entry : ttk.Entry = ttk.Entry(self.entry_subframe, width=ENTRY_WIDTH)

        self.id_label : ttk.Label = ttk.Label(self.entry_subframe, text="ID:")
        self.pin_label : ttk.Label = ttk.Label(self.entry_subframe, text="PIN:")
        self.rfid_label : ttk.Label = ttk.Label(self.entry_subframe, text="RFID:")

        self.confirm_btn : ttk.Button = ttk.Button(self.entry_subframe, text="Ajouter", command=self.submit_new_car)

        self.id_label.grid(column=0, row=0)
        self.id_entry.grid(column=1, row=0)
        self.pin_label.grid(column=2, row=0)
        self.pin_entry.grid(column=3, row=0)
        self.rfid_label.grid(column=4, row=0)
        self.rfid_entry.grid(column=5, row=0)
        self.confirm_btn.grid(column=6, row=0)
        self.entry_subframe.grid(column=0, row=0)

        self.missing_txt_label : ttk.Label = ttk.Label(self.entry_frame, text="", foreground="red", anchor="center")
        self.missing_txt_label.grid(column=0, row=1)

        self.entry_frame.grid(column=0, row=2)
        self.mgmt_frame.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))

        self.main_notebook.add(self.occupation_frame, text="Apercu")
        self.main_notebook.add(self.mgmt_frame, text="Gestion")
        self.main_notebook.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))

        self.redraw_db_tree_view()
        self.redraw_occupation_frame([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

    def submit_new_car(self):
        new_name : str = self.id_entry.get()
        new_rfid : str = self.rfid_entry.get()
        new_pin : str = self.pin_entry.get()

        if(new_name != '' and new_pin != '' and new_rfid != ''):
            self.missing_txt_label['text'] = ""
            self.db.add_car(RegisteredCar(name=new_name, rfid=new_rfid, pin=new_pin, status=(ParkingStatus.NOTIN_GARAGE)))

            self.id_entry.delete(0, "end")
            self.pin_entry.delete(0, "end")
            self.rfid_entry.delete(0, "end")

            self.redraw_db_tree_view()
        else:
            self.missing_txt_label['text'] = "Fill in all fields please!"

    def delete_car_selection(self):
        selections : tuple = self.db_tree.selection()

        for selection in selections:
            id_to_delete : str = self.db_tree.item(selection)['text']
            self.db.remove_car_id(id_to_delete)

        self.redraw_db_tree_view()

    def redraw_db_tree_view(self):
        car_list : List[RegisteredCar] = self.db.get_all()

        for item in self.db_tree.get_children():
            self.db_tree.delete(item)

        for car in car_list:
            self.db_tree.insert('', 'end', text=car.name, values=(car.pin, car.rfid, "Intérieur" if car.status == ParkingStatus.IN_GARAGE else "Dehors"))

    def redraw_occupation_frame(self, occupation_list : List[int], parking_rows=4, parking_cols=4):
        # car_list : List[RegisteredCar] = self.db.get_all()
        self._buttons_ : Dict[int, CarButton] = {}

        for child in self.occupation_frame.winfo_children():
            child.destroy()

        for i in range(parking_cols):
            parking_field : ttk.Frame = ttk.Frame(self.occupation_frame)
            s = ttk.Style()
            s.configure('Road.TFrame', background="black")

            if(i%2 == 0):
                buffer_field : ttk.Frame = ttk.Frame(self.occupation_frame, width=10, style='Road.TFrame')
                buffer_field.grid(column=(2*i)+1, row=0, sticky=('N', 'W', 'E', 'S'))
                self._buffer_subframes_[i] = buffer_field

            parking_field.grid(column=2*i, row=0)
            self._parking_subframes_[i] = parking_field

        car_cnt : int = 0
        for i in occupation_list:
            if(i == 1):
                bsubframe : ttk.Frame = self._parking_subframes_[car_cnt%parking_cols]
                button = CarButton(bsubframe, car_cnt, '', ParkingStatus.IN_GARAGE)
                button.grid(column=0, row=int((car_cnt/parking_cols)))
            elif(i == 0):
                bsubframe : ttk.Frame = self._parking_subframes_[car_cnt%parking_cols]
                button = CarButton(bsubframe, car_cnt, '', ParkingStatus.NOTIN_GARAGE)
                button.grid(column=0, row=int(car_cnt/parking_cols))

            car_cnt += 1


        # for car in car_list:
        #     if(car.status == ParkingStatus.IN_GARAGE):
        #         button = CarButton(self.occupation_frame, car_cnt, str(car.id), car.status)
        #         button.grid(column=car_cnt%parking_cols, row=int(car_cnt/parking_cols))
        #         car_cnt += 1

        # for i in range(car_cnt, self.max_spaces):
        #     button = CarButton(self.occupation_frame, -1, '')

        #     button.grid(column=car_cnt%parking_cols, row=int(car_cnt/parking_cols))
        #     car_cnt += 1


