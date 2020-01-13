# '''
# Created on Dec 13, 2019
# 
# @author: Hex
# '''
import binascii
from canlib import canlib
from canlib.canlib import ChannelData 
import threading, queue
import time

class CanBus(threading.Thread):
    def __init__(self, channel, cnt=9):
        super().__init__()
        
        #self.cnt = cnt
        self.ch = canlib.openChannel(channel, canlib.canOPEN_ACCEPT_VIRTUAL)
        print("Using channel: %s, EAN: %s" % (ChannelData(channel).channel_name,
                                              ChannelData(channel).card_upc_no))
        self.ch.setBusOutputControl(canlib.canDRIVER_NORMAL)
        self.ch.setBusParams(canlib.canBITRATE_500K)
        self.ch.busOn()
        #self.cnt = self.counter()
        self.queue = queue.Queue()
        self._is_alive = threading.Event()
        self._is_alive.set()
        self.frame_count = None
        
    def get(self):
        # None blocking get
        try:
            data = self.queue.get(False)
        except queue.Empty:
            return None
        return data
        
    def stop(self):
        print('CanBus.stop()')
        self._is_alive.clear()
        time.sleep(0.01)
        self.trashed_count = self.queue.qsize()
        #print('Trashed frames:{}'.format(self.queue.qsize()))
        while not self.queue.empty():
            self.queue.get()
    

    def run(self):
        while self._is_alive.is_set():
            item = None
            try:
                item = self.ch.read()
                self.queue.put(item)
                self.frame_count += 1
                time.sleep(0.05)
            except (canlib.canNoMsg):
                #self.queue.put('except canlib.canNoMsg')
                pass
            except Exception as e:  # Break at unknow error
                self.queue.put(e)
                self.stop()
                continue
    
#             if item is not None:
#             # Possible to decode data before
#             # item.data = text(item.data)
#                 #print('\tqueue.put({})'.format(item))
#                 self.queue.put(item)
#             else:
#                 #self.queue.put('item is None')
#                 pass
    
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

    def text(self, t):
        tx = binascii.hexlify(t).decode('utf-8')
        n = 2
        txt = [tx[i:i+n] for i in range(0, len(tx), n)]
        return txt  

# def read4(cbus):
#     j = 0
#     while j < 4:
#         frame = None
#         try:
#             frame = cbus.ch.read()
#         except (canlib.canNoMsg):
#             pass
#         
#         print(j)
#         if frame is not None:
#             print("%s\t%s\n" %(frame.id, text(frame.data)))
#         j += 1
#        show = show + ("%s\t%s\n" %(frame.id, text(frame.data)))
#        print(show)

if __name__ == "__main__":
    print("canlib version:", canlib.dllversion())
    
    # Read from the canbus    
    cbus = CanBus(channel=0)

#     print("Counter: %d" %(cbus.cnt)) 

    cbus.start()
    # For testing we need to terminate the `Thread`
    none_count = 0
    max_frames = 1000
    for _ in range(max_frames):
        time.sleep(0.005)
        frame = cbus.get()
        if frame is None:
            none_count +=1
        else:
            #print(frame.data)
            pass
        
    cbus.stop()
    print('EXIT, frame_count:{}'.format(cbus.frame_count))
        
        
    cbus.tearDownChannel()