'''
Created on Dec 13, 2019

@author: Hex
'''

import tkinter as tk
from canbus import CanBus

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)

        # Define any widgets
        self.text = tk.Text(self, height=6, width=60)
        self.text.pack()
        self.none_count = 0
        self.cbus = CanBus(channel=0)
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
                self.text.insert(tk.END, "%s\t%s\n" %(frame.id, frame.data))
            else:
                self.none_count += 1

            self.after(10, self.display)    

#self.ch0 = canbus(channel=0)

if __name__ == "__main__":
    App().mainloop()