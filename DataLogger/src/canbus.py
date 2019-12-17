# '''
# Created on Dec 13, 2019
# 
# @author: Hex
# '''
import binascii
from canlib import canlib, Frame
from canlib.canlib import ChannelData 

class CanBus:
    def __init__(self, channel):
        self.ch = canlib.openChannel(channel, canlib.canOPEN_ACCEPT_VIRTUAL)
        print("Using channel: %s, EAN: %s" % (ChannelData(channel).channel_name,
                                              ChannelData(channel).card_upc_no)
                                                )
        self.ch.setBusOutputControl(canlib.canDRIVER_NORMAL)
        self.ch.setBusParams(canlib.canBITRATE_500K)
        self.ch.busOn()
    
def tearDownChannel(ch):
    ch.busOff()
    ch.close()

def text(t):
    tx = binascii.hexlify(t).decode('utf-8')
    n = 2
    txt = [tx[i:i+n] for i in range(0, len(tx), n)]
    return txt

def counter(ch):
    try:
        cnt = 1
        frame = ch.read()
        firstID = frame.id
        while True:
            frame = ch.read()
            cnt += 1
            if frame.id == firstID:
                break
        pass    
    except (canlib.canNoMsg):
        pass
    except (canlib.canError):
        print("Rerun")
    return cnt


print("canlib version:", canlib.dllversion())

cnt = counter()
print("Counter: %d" %(cnt))  

tearDownChannel(ch0)
 
if __name__ == "__main__":
    cbus = CanBus(channel=0)
    # Read from the canbus
    i = 0
    show = ""
    while i <= 4:
        show = ""
        frame = cbus.read()
        show = show + ("%s\t%s\n" %(frame.id, text(frame.data)))
        print(show)
        i += 1