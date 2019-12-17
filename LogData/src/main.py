'''
Created on Dec 10, 2019

@author: Johannes Appel
'''
import keyboard
import time
import sys
import tkinter as tk
import binascii

from canlib import canlib, Frame
from canlib.canlib import ChannelData

root = tk.Tk()

def setUpChannel(channel,
                 openFlags=canlib.canOPEN_ACCEPT_VIRTUAL,
                 bitrate=canlib.canBITRATE_500K,
                 bitrateFlags=canlib.canDRIVER_NORMAL):
    ch = canlib.openChannel(channel, openFlags)
    print("Using channel: %s, EAN: %s" % (ChannelData(channel).channel_name,
                                          ChannelData(channel).card_upc_no)
                                                )
    ch.setBusOutputControl(bitrateFlags)
    ch.setBusParams(bitrate)
    ch.busOn()
    return ch

def tearDownChannel(ch):
    ch.busOff()
    ch.close()

def text(t):
    tx = binascii.hexlify(t).decode('utf-8')
    n = 2
    txt = [tx[i:i+n] for i in range(0, len(tx), n)]
    return txt

def counter():
    try:
        cnt = 1
        frame = ch0.read()
        firstID = frame.id
        while True:
            frame = ch0.read()
            cnt += 1
            if frame.id == firstID:
                break
        pass    
    except (canlib.canNoMsg):
        pass
    except (canlib.canError):
        print("Rerun")
    return cnt

def display():
    T.delete("1.0", "end")
    show = ""
    i = 1
    while i <= 4:
        frame = ch0.read()
        show = show + ("%s\t%s\n" %(frame.id, text(frame.data)))
        i += 1
    print(show) 
    T.insert("end", show)
    root.after(10, display)

print("canlib version:", canlib.dllversion())

ch0 = setUpChannel(channel=0)
ch1 = setUpChannel(channel=1)

# frame = Frame(id_=100, data=[1, 2, 3, 4], flags=canlib.canMSG_EXT)
# ch1.write(frame)
# print(frame)

cnt = counter()
print("Counter: %d" %(cnt))

T = tk.Text(root, height=6, width=60)
T.config(state="normal")
T.pack()
 
display()
root.mainloop()     

tearDownChannel(ch0)
tearDownChannel(ch1)
