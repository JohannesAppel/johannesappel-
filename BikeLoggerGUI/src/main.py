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

def find():
    id_index = 0
    byte_index = 0
    first_byte = 0
    second_byte = 0
    for j in range (len(dispListRun1)):
        dispR = dispListRun2[j].split(",")
        dispS = dispListSec2[j].split(",")
        for x in range (len(dispR)):
            if dispR[x] != dispS[x] and dispR[x] != 'XX':
                id_index = dispListRun1[j]
                byte_index = x
                first_byte = dispR[x]
                second_byte = dispS[x]
    return id_index, byte_index, first_byte, second_byte

def test(indx, txt):
    spl = text(txt).split(",")
    dispSec2 = dispListSec2[indx].split(",")
    for i in range (len(spl)):
        if spl[i] != dispSec2[i]:
            spl[i] = 'OO'
    listSec2 = ','.join(spl)
    return listSec2

def resetData():
    del dispListRun1[:]
    del dispListRun2[:]
    del dispListSec1[:]
    del dispListSec2[:]

def calibrate():
    resetData()
    var.set('Calibrating...')
    ch0 = setUpChannel(channel=0)
    cnt = 0
    while cnt < 1000:
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
        val = cnt/10
        progress['value'] = val
        root.update()
        
    tearDownChannel(ch0)
    var.set('Turn on desired control unit and press done.')
    lab.pack(side=LEFT)
    ent.pack(side=LEFT)
    done.pack(side=RIGHT)
    
def done():
    var.set('Running...')
    ch0 = setUpChannel(channel=0)
    cnt = 0
    while cnt < 1000:
        try:
            frame = ch0.read()
            cnt += 1
        except (canlib.canNoMsg):
            pass
            #print('Error')
        if frame.id in dispListSec1:
            inx = dispListSec1.index(frame.id)
            dispListSec1[inx] = frame.id
            dispListSec2[inx] = text(frame.data)
        else:
            dispListSec1.extend([frame.id])
            dispListSec2.extend([text(frame.data)])
        sortSec()
        val = cnt/10
        progress['value'] = val
        root.update()
        
    tearDownChannel(ch0)
    indexFind = find()
    var.set("Done.\nThe ID of the control unit is: %d\nThe position of the byte is: %d\nThe byte changed from %s to %s" 
            % (indexFind[0], indexFind[1]+1, indexFind[2], indexFind[3]))
    cu = ent.get()
    dataList.append('Control unit: {}, ID: {}, Byte: {}, {} -> {}'.format(cu, indexFind[0], indexFind[1]+1, indexFind[2], indexFind[3]))
    
    export.pack(side=tk.BOTTOM)
    ent.delete(0, 'end')
    lab.pack_forget()
    ent.pack_forget()
    done.pack_forget()

def export():
    with open('listfile.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % listItem for listItem in dataList)
    export.pack_forget()

root = tk.Tk()
root.title('Data Logger')
var = StringVar()
var.set('Select an option.')
L = Label(root, textvariable = var)
L.pack()

progress = Progressbar(root, orient = HORIZONTAL, length = 100, mode = 'determinate')
progress.pack(pady = 10)

frame = tk.Frame(root)
frame.pack(fill=None, expand=False)

button = tk.Button(frame, text="Quit", fg="red", command=desQuit)
button.pack(side=tk.RIGHT)

slogan = tk.Button(frame, text="Calibrate", command=calibrate)
slogan.pack(side=tk.LEFT)

done = tk.Button(root, text="Done", command=done)

export = tk.Button(frame, text="Export", command=export)

lab = tk.Label(root, text="Control Unit")
ent = tk.Entry(root)

dispListRun1 = []
dispListRun2 = []
dispListSec1 = []
dispListSec2 = []

cu = ""
dataList = []

root.mainloop()