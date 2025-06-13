import serial
import time
import queue

from typing import List

# print(ser.readline())

# with serial.Serial("/dev/pts/5", 9600, timeout=1) as ser:
#     while True:

#         print(ser.read(1))
#         # ser.write(b'dfdfabc\n\r')
#         # ser.flush()
#         # time.sleep(1)

class InfoReader():
    def __init__(self, port : str = "/dev/pts/5", baud : int = 9600, timeout : int = 1, start_char : str = "{", end_char : str = "}"):
        self.ser : serial.Serial = serial.Serial(port, baud, timeout=timeout)

        self._start_char_ : str = start_char
        self._end_char_ : str = end_char
        self._ser_buf_ : List[str] = []

    def write_info(self, txt : str):
        with self.ser as ser:
            ser.write(bytes(txt, "utf-8"))

    def get_next_info(self) -> str:
        with self.ser as ser:
            buffering : bool = False
            self._ser_buf_ = []

            while True:
                rec_bytes : bytes = ser.read()
                rec_char : str = str(rec_bytes, "utf-8")

                
                
                if(rec_char == self._start_char_ and not buffering):
                    buffering : bool = True

                if(buffering):
                    self._ser_buf_.append(rec_char)

                if(rec_char == self._end_char_ and buffering):
                    return ''.join(self._ser_buf_)

                
                

    def queue_infos(self, queue : queue.Queue):
        while True:
            queue.put(self.get_next_info())

    def queue_next_info(self, queue : queue.Queue):
        queue.put(self.get_next_info())
