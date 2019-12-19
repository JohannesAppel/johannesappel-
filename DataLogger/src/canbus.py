# '''
# Created on Dec 13, 2019
# 
# @author: Hex
# '''
import binascii
from canlib import canlib, Frame
from canlib.canlib import ChannelData 

class CanBus:
    def __init__(self, channel, cnt=4):
        self.cnt = cnt
        self.ch = canlib.openChannel(channel, canlib.canOPEN_ACCEPT_VIRTUAL)
        print("Using channel: %s, EAN: %s" % (ChannelData(channel).channel_name,
                                              ChannelData(channel).card_upc_no)
                                                )
        self.ch.setBusOutputControl(canlib.canDRIVER_NORMAL)
        self.ch.setBusParams(canlib.canBITRATE_500K)
        self.ch.busOn()
    
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

if __name__ == "__main__":
    print("canlib version:", canlib.dllversion())
    
    # Read from the canbus    
    cbus = CanBus(channel=0)
#     cbus.cnt = cbus.counter()
#     print("Counter: %d" %(cbus.cnt)) 
    
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
#             show = show + ("%s\t%s\n" %(frame.id, text(frame.data)))
#             print(show)
        
        
    cbus.tearDownChannel()