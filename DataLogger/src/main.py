'''
Created on Dec 13, 2019

@author: Hex
'''

import tkinter as tk
from canbus import CanBus

class FrameListbox(tk.Listbox):
    FRAMES_TO_SHOW = 4
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.quit)

        # Define any widgets
        self.text = tk.Text(self, height=6, width=60)
        self.text.pack()
        self.none_count = 0
        self.cbus = CanBus(channel=0)
        self.cbus.start()
        self.after(10, self.display)
        self._count = 0

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
                self.frame_listbox.insert("%s\t%s" %(frame.id, frame.data))
            else:
                self.none_count += 1

            self.after(10, self.display)    
    
    def insert(self, frame):
        if self._count == FrameListbox.FRAMES_TO_SHOW:
            self.delete(0, tk.END)
            self._count = 0
        
        super().insert(tk.END, frame)
        self._count += 1
#self.ch0 = canbus(channel=0)

if __name__ == "__main__":
    FrameListbox().mainloop()