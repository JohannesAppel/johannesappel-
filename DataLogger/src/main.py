'''
Created on Dec 13, 2019

@author: Hex
'''

import tkinter as tk
from canbus import CanBus

class FrameListbox(tk.Listbox):
    def __init__(self, parent, lines=9, **kwargs):
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
        #self.frame_listbox = FrameListbox(self, lines=self.cbus.cnt, height=0, width=0)
        #self.frame_listbox.pack()
        self.none_count = 0
        self.cbus.start()
        self.after(1, self.display)
        self.received_frame = {}
        self.frame_labels = FrameLabels(self, width=280, height=100)
        self.frame_labels.pack()

    def quit(self):
        # Add here any shutdown related statements
        self.cbus.stop()
        self.cbus.tearDownChannel()
        print('EXIT, frame_count:{}, none_count:{}, trashed_count:{}'.format(self.cbus.frame_count, self.none_count, self.cbus.trashed_count)) 
        super().quit()
        
    def display(self):
        if self.cbus.is_alive():
            frame = self.cbus.get()

            if frame is not None:
                text = "{:<5} {}".format(frame.id, self.cbus.text(frame.data))
                self.frame_labels.set(frame_id=frame.id, text=text)

            else:
                self.none_count += 1

            self.after(4, self.display)
        else:
            print('Received Frame ids:{}'.format(sorted(FrameLabels.received.keys())))
#         if self.cbus.is_alive():
#             frame = self.cbus.get()
#             if frame is not None:
#                 self.frame_listbox.insert("{:<5} {}".format(frame.id, self.cbus.text(frame.data)))
#             else:
#                 self.none_count += 1
# 
#             self.after(1, self.display)    

class FrameLabels(tk.Frame):
    received = {}
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg='white', **kwargs)        
        self.grid_columnconfigure(0, weight=1)
        
    def new_label(self, text):
        label = tk.Label(self, text=text, bg=self.cget('bg'), font=('Consolas', 10), anchor='nw', justify=tk.LEFT)
        return label
    
    def layout(self, _sorted, text):
        # Forget all layouted Label
        for c in self.children.values():
            c.grid_forget()
        
        # Layout all Label in sorted order
        for _id in _sorted:
            FrameLabels.received[_id].grid(column=0, sticky='ew')
            
    def set(self, frame_id, text):
        label = FrameLabels.received.get(frame_id, None)

        if label is None:
            label = self.new_label(text=text)
            FrameLabels.received[frame_id] = label
            
            _sorted = sorted(FrameLabels.received.keys())
            
            if _sorted[-1] != frame_id:
                self.layout(_sorted, text)

            else:  # append Label
                label.grid(column=0, sticky='ew')

        else:
            label.configure(text=text)
#self.ch0 = canbus(channel=0)

if __name__ == "__main__":
    App().mainloop()