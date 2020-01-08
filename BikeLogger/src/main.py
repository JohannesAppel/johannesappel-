'''
Created on Jan 7, 2020

@author: Johannes Appel
'''

'''
Created on Dec 10, 2019

@author: Johannes Appel
'''
import tkinter as tk
import binascii

from canlib import canlib
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
    temp = [tx[i:i+n] for i in range(0, len(tx), n)]
    txt = ', '.join(temp)
    return txt

def display():
    T.delete("1.0", "end")
    show = "%s\t%s" %("ID:", "Data:")
    try:
        frame = ch0.read()
    except (canlib.canNoMsg): 
        print('Error')
        
    if frame.id in dispList1:
        inx = dispList1.index(frame.id)
        dispList1[inx] = frame.id
        dispList2[inx] = text(frame.data)
    else:
        dispList1.extend([frame.id])
        dispList2.extend([text(frame.data)])
    
#     tempList = sorted(zip(dispList1, dispList2))
#     dispList1, dispList2 = map(list, zip(*tempList))
            
    for i in range(len(dispList1)):
        show = show + ("\n%s\t%s" %(dispList1[i], dispList2[i]))
    T.insert("end", show)
    root.after(1, display)

print("canlib version:", canlib.dllversion())
ch0 = setUpChannel(channel=0)

T = tk.Text(root, height=11, width=60)
T.config(state="normal")
T.pack()

listCnt = []

dispList1 = []
dispList2 = []

display()
root.mainloop()     

tearDownChannel(ch0)
