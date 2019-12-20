'''
Created on Dec 13, 2019

@author: Hex
'''

import tkinter as tk
from canbus import CanBus

class FrameListbox(tk.Listbox):
    def __init__(self, parent, lines=4, **kwargs):
        super().__init__(parent, font=('Consolas', 10), **kwargs)

        self._lines_to_show = lines
        self._lines = 0
        
    def insert(self, frame):
        if self._lines == self._lines_to_show:
            self.delete(0, tk.END)
            self._lines = 0
        
        super().insert(tk.END, frame)
        self._lines += 1

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)

        # Define any widgets
        self.cbus = CanBus(channel=0)
        self.frame_listbox = FrameListbox(self, lines=self.cbus.cnt, height=6, width=60)
        self.frame_listbox.pack()
        self.none_count = 0
        self.cbus.start()
        self.after(10, self.display)

    def quit(self):
        # Add here any shutdown related statements
        self.cbus.stop()
        self.cbus.tearDownChannel()
        print('EXIT, none_count:{}'.format(self.none_count))
        super().quit()
        
    def display(self):
        if self.cbus.is_alive():
            frame = self.cbus.get()
            if frame is not None:
                self.frame_listbox.insert(tk.END, "%s\t%s\n" %(frame.id, frame.data))
            else:
                self.none_count += 1

            self.after(10, self.display)    

#self.ch0 = canbus(channel=0)

if __name__ == "__main__":
    App().mainloop()