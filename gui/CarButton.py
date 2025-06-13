import tkinter as tk
from tkinter import ttk

from models.db import ParkingStatus


class CarButton(ttk.Button):
    def __init__(self, master, id : int, text : str = None, status : ParkingStatus = ParkingStatus.NOTIN_GARAGE, ing_clr : str = "green", ning_clr : str = "gray"):
        self.bstyle : ttk.Style = ttk.Style()

        self.id : int = id
        self.status : ParkingStatus = status

        self._ing_clr_ = ing_clr
        self._ning_clr_ = ning_clr
        self._style_name_ = f"cbutton{self.id}.TButton"

        if(text is None):
            btext : str = str(self.id)
        else:
            btext : str = text

        self._update_clr()
        self.button : ttk.Button = super().__init__(master, style=f"cbutton{self.id}.TButton", text=btext)

    def _update_clr(self):
        if(self.status == ParkingStatus.IN_GARAGE):
            self.bstyle.configure(self._style_name_, background=self._ing_clr_)
        else:
            self.bstyle.configure(self._style_name_, background=self._ning_clr_)

    def set_parking_state(self):
        self.status = ParkingStatus.IN_GARAGE
        self._update_clr()

    def reset_parking_state(self):
        self.status = ParkingStatus.NOTIN_GARAGE
        self._update_clr()

    def toggle_parking_state(self):
        if(self.status == ParkingStatus.IN_GARAGE):
            self.reset_parking_state()
        else:
            self.set_parking_state()

    def update_status(self, new_status : ParkingStatus):
        if(new_status == ParkingStatus.IN_GARAGE):
            self.reset_parking_state()
        else:
            self.set_parking_state()