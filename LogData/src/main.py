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
    listCnt = []
    j = 0
    firstID = 0
    while j < 1000:
        try:
            frame = ch0.read()
            firstID = frame.id
            while True:
                frame = ch0.read()
                if frame.id not in listCnt:
                    listCnt.append(frame.id)
                if frame.id == firstID:
                    break  
        except (canlib.canNoMsg):
            pass
        j += 1
        time.sleep(0.01)        
#     try:
#         cnt = 0
#         frame = ch0.read()
#         firstID = frame.id
#         while True:
#             frame = ch0.read()
#             cnt += 1
#             if frame.id == firstID:
#                 break 
#     except (canlib.canNoMsg):
#         pass
#     except (canlib.canError):
#         pass
    listCnt.sort()
    print(listCnt)
    return len(listCnt)

def display():
    T.delete("1.0", "end")
    dispList = [[],[]]
    show = ""
    i = 1
    while i <= cnt:
        try:
            frame = ch0.read()
            if frame.id not in dispList:
                dispList.extend([frame.id, frame.data])
            else:
                inx = dispList.index(frame.id)
                dispList[inx] = [frame.id], [frame.data]
                #dispList()
            #print(dispList)
            show = show + ("%s\t%s\n" %(frame.id, text(frame.data)))
            i += 1             
        except (canlib.canNoMsg):
            pass
    print(show)
    T.insert("end", show)
    root.after(1, display)

def cycle(firstID):
    while True:
        try:
            frame = ch0.read()
            if frame.id == firstID:
                break
        except (canlib.canNoMsg):
            pass

print("canlib version:", canlib.dllversion())

ch0 = setUpChannel(channel=0)

cnt = counter()
print("Counter: %d" %(cnt))

T = tk.Text(root, height=20, width=100)
T.config(state="normal")
T.pack()

#cycle()

display() 
root.mainloop()     

tearDownChannel(ch0)
