'''
Created on Jan 10, 2020

@author: Johannes Appel
'''

import tkinter as tk
import binascii
import time

from canlib import canlib
from canlib.canlib import ChannelData
from tkinter import *
from tkinter.ttk import *

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

def desQuit():
    root.destroy()

def sortRun():
    for j in range(len(dispListRun1)-1):
        if dispListRun1[j] > dispListRun1[j+1]:
            temp = dispListRun1[j];
            dispListRun1[j] = dispListRun1[j+1];
            dispListRun1[j+1] = temp;
    
            temp = dispListRun2[j];
            dispListRun2[j] = dispListRun2[j+1];
            dispListRun2[j+1] = temp;
            
def sortSec():
    for j in range(len(dispListSec1)-1):
        if dispListSec1[j] > dispListSec1[j+1]:
            temp = dispListSec1[j];
            dispListSec1[j] = dispListSec1[j+1];
            dispListSec1[j+1] = temp;
    
            temp = dispListSec2[j];
            dispListSec2[j] = dispListSec2[j+1];
            dispListSec2[j+1] = temp;
    
def text(t):
    tx = binascii.hexlify(t).decode('utf-8')
    n = 2
    temp = [tx[i:i+n] for i in range(0, len(tx), n)]
    txt = ','.join(temp)
    return txt

def returning(indx, txt):
    spl = text(txt).split(",")
    disp2 = dispListRun2[indx].split(",")
    for i in range (len(spl)):
        if spl[i] != disp2[i]:
            spl[i] = 'XX'
    listRun2 = ','.join(spl)
    return listRun2

def find(con):
    id_index = 0
    byte_index = 0
    first_byte = ""
    second_byte = ""
    for j in range (len(dispListRun1)):
        dispR = dispListRun2[j].split(",")
        dispS = dispListSec2[j].split(",")
        for x in range (len(dispR)): 
            if dispR[x] != dispS[x] and dispR[x] != 'XX':
                id_index = dispListRun1[j]
                byte_index = x+1
                first_byte = dispR[x]
                second_byte = dispS[x]
                if dispS[x] == 'OO':
                    dispList.append('Control unit: {}, ID: {}, Byte: {}, {} -> {}'.format(con, id_index, byte_index, blink1, blink2))
                    dataList.append('Control unit: {}, ID: {}, Byte: {}, {} -> {}'.format(con, id_index, byte_index, blink1, blink2))
                else:
                    dispList.append('Control unit: {}, ID: {}, Byte: {}, {} -> {}'.format(con, id_index, byte_index, first_byte, second_byte))
                    dataList.append('Control unit: {}, ID: {}, Byte: {}, {} -> {}'.format(con, id_index, byte_index, first_byte, second_byte))
    return dispList

def test(indx, txt):
    spl = text(txt).split(",")
    dispSec2 = dispListSec2[indx].split(",")
    dispRun2 = dispListRun2[indx].split(",")
    for i in range (len(spl)):
        if spl[i] != dispSec2[i] and dispRun2[i] != 'XX':
            if dispSec2[i] == 'OO':
                spl[i] = 'OO'
            else:
                global count
                global blink1
                global blink2
                if count < 1:
                    blink1 = dispSec2[i]
                    blink2 = spl[i]
                    spl[i] = 'OO'
                    count += 1
    listSec2 = ','.join(spl)
    return listSec2

def resetData():
    del dispListRun1[:]
    del dispListRun2[:]
    del dispListSec1[:]
    del dispListSec2[:]
    del dispList[:]
    global blink1
    blink1 = ""
    global blink2
    blink2 = ""
    global count
    count = 0

def calibrate():
    entBike.delete(0, 'end')
    entBike.pack_forget()
    bikeName.pack_forget()
    resetData()
    var.set('Calibrating...')
    ch0 = setUpChannel(channel=0)
    cnt = 0
    while cnt < 5000:
        try:
            frame = ch0.read()
            cnt += 1
        except (canlib.canNoMsg):
            pass
            #print('Error')
        if frame.id in dispListRun1:
            inx = dispListRun1.index(frame.id)
            dispListRun1[inx] = frame.id
            dispListRun2[inx] = returning(inx, frame.data)
        else:
            dispListRun1.extend([frame.id])
            dispListRun2.extend([text(frame.data)])
        sortRun()
        val = cnt/50
        progress['value'] = val
        root.update()
        
    tearDownChannel(ch0)
    var.set('Turn on desired control unit and press done.')
    lab.pack(side=tk.LEFT, padx=3, pady=3)
    entControl.pack(side=tk.LEFT, padx=3, pady=3)
    done.pack(side=tk.RIGHT, padx=3, pady=3)
    
def done():
    var.set('Running...')
    ch0 = setUpChannel(channel=0)
    cnt = 0
    while cnt < 5000:
        try:
            frame = ch0.read()
            cnt += 1
        except (canlib.canNoMsg):
            pass
            #print('Error')
        if frame.id in dispListSec1:
            inx = dispListSec1.index(frame.id)
            dispListSec1[inx] = frame.id
            dispListSec2[inx] = test(inx, frame.data)
        else:
            dispListSec1.extend([frame.id])
            dispListSec2.extend([text(frame.data)])
        sortSec()
        val = cnt/50
        progress['value'] = val
        root.update()
        
    tearDownChannel(ch0)
    
    cu = entControl.get()
    indexFind = find(cu)
    if len(indexFind) == 1:
        disp = indexFind
    else:
        disp = '\n'.join(indexFind)
    var.set(disp)
    
    export.pack(side=tk.BOTTOM, padx=3, pady=3)
    entControl.delete(0, 'end')
    lab.pack_forget()
    entControl.pack_forget()
    done.pack_forget()
    bikeName.pack(side=tk.LEFT, padx=3, pady=3)
    entBike.pack(side=tk.RIGHT, padx=3, pady=3)
    
def export():
    name = entBike.get()
    with open('{}.txt'.format(name), 'w') as filehandle:
        filehandle.writelines("%s\n" % listItem for listItem in dataList)
    export.pack_forget()

root = tk.Tk()
root.title('Data Logger')
var = StringVar()
var.set('Select an option.')
L = Label(root, textvariable = var)
L.pack()

progress = Progressbar(root, orient = HORIZONTAL, length = 100, mode = 'determinate')
progress.pack(pady = 8)

frame = tk.Frame(root)
frame.pack(fill=None, expand=False)

quitButton = tk.Button(frame, text="Quit", fg="red", command=desQuit)
quitButton.pack(side=tk.RIGHT, padx=3, pady=3)

calibrateButton = tk.Button(frame, text="Calibrate", command=calibrate)
calibrateButton.pack(side=tk.LEFT, padx=3, pady=3)

done = tk.Button(root, text="Done", command=done)

export = tk.Button(frame, text="Export", command=export)

lab = tk.Label(root, text="Control Unit")
entControl = tk.Entry(root)

bikeName = tk.Label(root, text="Bike Name")
entBike = tk.Entry(root)

dispListRun1 = []
dispListRun2 = []
dispListSec1 = []
dispListSec2 = []

cu = ""
dataList = []
dispList = []
blink = ""
count = 0

root.mainloop()