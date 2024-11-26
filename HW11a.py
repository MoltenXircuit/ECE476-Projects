from machine import Pin, bitstream
from time import sleep


def addLight(A,color):
    if (color == 'Y'):
        A.extend(bytearray([20,20,0]))
    elif (color == 'G'):
        A.extend(bytearray([20,0,0]))
    elif (color == 'R'):
        A.extend(bytearray([0,20,0]))
        
def starter_tree_reset(N):
    timing = [300, 900, 700, 500]
    np = Pin(12, Pin.OUT)
    X = bytearray([0,0,0]*N)
    bitstream(np, 0, timing, X)
    
def starter_tree(N):
    timing = [300, 900, 700, 500]
    np = Pin(12, Pin.OUT)
    timing = [300, 900, 700, 500]
    X = bytearray([20,20,0])
    sleep(0.75)
    bitstream(np, 0, timing, X)
    for neo in range(1,N-1):
        tree_status = ( (neo+1) /N)
        sleep(0.75)
        addLight(X,'Y')
        bitstream(np, 0, timing, X)
    sleep(0.75)
    addLight(X,'G')
    bitstream(np, 0, timing, X)
    
#global starter_tree_reset, starter_tree
Button14 = Pin(14, Pin.IN, Pin.PULL_UP)
Button15 = Pin(15, Pin.IN, Pin.PULL_UP)

N = 8
starter_tree_reset(N)
reset = 1
while(1):
    if ((Button15.value() == 0) and (reset == 1)):
        starter_tree(N)
        reset = 0
    elif ((Button14.value() == 0) and (reset == 0)):
        starter_tree_reset(N)
        reset = 1
    else:
        sleep(0.1)



