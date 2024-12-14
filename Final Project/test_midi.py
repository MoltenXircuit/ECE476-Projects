from machine import Pin
from micropython import const
import usb.device
from usb.device.midi import MIDIInterface
import time
from collections import deque


#---------------------IO Definitions------------------------------
spkr = Pin(13,Pin.OUT)
led = Pin(25, Pin.OUT)


#---------------------Definitions------------------------------

_MIDI_POLY_KEYPRESS = const(0xA0)
_CIN_POLY_KEYPRESS = const(0xA)

N = const(7)

global delta_key_stack

#delta_key_stack.popleft()
previous_state = ([0] * N)

#---------------------Midi Update-------------------------

def UpdateMIDI():
    if ( len(delta_key_stack) > 0 ):
        key = delta_key_stack.popleft()
        i = key[0]
        key_volume = key[1]    #using a list as a queue
        print(key)
        
        if (i<0):
            pass
        elif ((previous_state[i] == 0) and (key_volume != 0)):
            previous_state[i] = 1
            print("on", i, key_volume)
        elif (key_volume == 0):
            previous_state[i] = 0
            print("off", i, key_volume)

        #else:
            #midi.send_event(_CIN_POLY_KEYPRESS, _MIDI_POLY_KEYPRESS| CHANNEL, i, vel)

#---------------------Code Start-------------------------

# Remove builtin_driver=True if you don't want the MicroPython serial REPL available.
# TX constants
CHANNEL = 0
PITCH = 60
CONTROLLER = 64

control_val = 0

while True:
    UpdateMIDI()
    time.sleep(2)

