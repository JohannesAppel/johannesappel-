'''
Created on Dec 13, 2019

@author: Hex
'''

import tkinter as tk
import canbus

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)

        # Define any widgets
        self.text = tk.Text(self, height=6, width=60)
        

    def quit(self):
        # Add here any shutdown related statements
        super().quit()
        
self.ch0 = CanBus(channel=0)

if __name__ == "__main__":
    App().mainloop()