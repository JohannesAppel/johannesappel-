# '''
# Created on Dec 13, 2019
# 
# @author: Hex
# '''
import binascii
from canlib import canlib, Frame
from canlib.canlib import ChannelData 
import threading, queue

class CanBus(threading.Thread):
    def __init__(self, channel, cnt=4):
        super().__init__()
        
        self.cnt = cnt
        self.ch = canlib.openChannel(channel, canlib.canOPEN_ACCEPT_VIRTUAL)
        print("Using channel: %s, EAN: %s" % (ChannelData(channel).channel_name,
                                              ChannelData(channel).card_upc_no))
        self.ch.setBusOutputControl(canlib.canDRIVER_NORMAL)
        self.ch.setBusParams(canlib.canBITRATE_500K)
        self.ch.busOn()
        
        self.queue = queue.Queue()
        self._is_alive = threading.Event()
        self._is_alive.set()
        
    def get(self):
        # None blocking get
        try:
           data = self.queue.get(False)
        except ???.QueueEmpty:
           return None
        return data
        
    def stop(self):
        print('CanBus.stop()')
        self._is_alive.clear()
        while not self.queue.is_empty():
            self.queue.get()
    

    def run(self):
        # copy my sceleton
    
    def tearDownChannel(self):
        self.ch.busOff()
        self.ch.close()
        
    def counter(self):
        try:
            cnt = 0
            frame = self.ch.read()
            firstID = frame.id
            while True:
                frame = self.ch.read()
                cnt += 1
                if frame.id == firstID:
                    break                    
        except (canlib.canNoMsg):
            pass
        except (canlib.canError):
            pass
        return cnt
    
    def read_frame(self):
        frame = []
        for _ in range(self.cnt):
            frame.append(self.ch.read())
        return frame

def text(t):
    tx = binascii.hexlify(t).decode('utf-8')
    n = 2
    txt = [tx[i:i+n] for i in range(0, len(tx), n)]
    return txt  

def read4(cbus):
    j = 0
    show = ""
    while j < 4:
        frame = None
        try:
            frame = cbus.ch.read()
        except (canlib.canNoMsg):
            pass
        
        print(j)
        if frame is not None:
            print("%s\t%s\n" %(frame.id, text(frame.data)))
        j += 1
#        show = show + ("%s\t%s\n" %(frame.id, text(frame.data)))
#        print(show)

if __name__ == "__main__":
    print("canlib version:", canlib.dllversion())
    
    # Read from the canbus    
    cbus = CanBus(channel=0)
#     cbus.cnt = cbus.counter()
#     print("Counter: %d" %(cbus.cnt)) 

    cbus.start()
    # For testing we need to terminate the `Thread`
    max_frames = 100
    for _ in range(max_frames):
        frame = cbus.get()
        print(frame)
    cbus.stop()
    print('EXIT')
        
        
    cbus.tearDownChannel()