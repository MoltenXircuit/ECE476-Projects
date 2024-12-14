from machine import Pin, ADC, PWM
from micropython import const
import usb.device
from usb.device.midi import MIDIInterface
import time
from collections import deque

delta_key_stack = deque([[1,250]],200)
"""
delta_key_stack.append([1,250])
delta_key_stack.append([3,200])
delta_key_stack.append([1,0])
delta_key_stack.append([0,0])
delta_key_stack.append([3,0])
delta_key_stack.append([1,250])
delta_key_stack.append([3,200])
delta_key_stack.append([1,0])
delta_key_stack.append([0,0])
delta_key_stack.append([3,0])
delta_key_stack.append([3,200])
delta_key_stack.append([1,0])
delta_key_stack.append([0,0])
delta_key_stack.append([3,0])
"""
#---------------------IO Definitions------------------------------
a2d2 = ADC(2)
led = Pin(25, Pin.OUT)
Spkr = PWM(Pin(11))

midi = MIDIInterface()

#---------------------Definitions------------------------------

_MIDI_POLY_KEYPRESS = const(0xA0)
_CIN_POLY_KEYPRESS = const(0xA)

N = const(7)
last_state = ([0]*N)
previous_state = ([0]*N)

    
#---------------------Midi Update-------------------------
def make_stack(key_scaled_state):
    i = len(key_scaled_state)
    while i>0:
        i = i-1
        if (key_scaled_state[i] < 0):
            key_scaled_state[i] = 0
        if ( (previous_state[i] != 1) and (key_scaled_state[i] > (120)) ):     #add key_on to queue if not already on
            previous_state[i] = 1
            delta_key_stack.append([i,key_scaled_state[i]])
            
        elif( (previous_state[i] != 0) and (key_scaled_state[i] < (120)) ):     #add key_off to queue if not already off
            previous_state[i] = 0
            delta_key_stack.append([i,0])



def UpdateMIDI():

    if ( len(delta_key_stack) > 0 ):
        CHANNEL = 0
        key = delta_key_stack.popleft()
        i = key[0]
        key_volume = int(key[1])    #using a list as a queue
        if (i<0):
            pass
        elif ((last_state[i] == 0) and (key_volume != 0)):
            last_state[i] = 1
            print("on", key)
            midi.note_on(CHANNEL, i, (a2d2.read_u16() >> 9))
            led.value(1)

            
        elif ((last_state[i] == 1) and (key_volume == 0)):
            last_state[i] = 0
            print("off", key)
            midi.note_off(CHANNEL, i)
            led.value(0)
        #else:
            #midi.send_event(_CIN_POLY_KEYPRESS, _MIDI_POLY_KEYPRESS| CHANNEL, i, vel)

#---------------------Code Start-------------------------


# Remove builtin_driver=True if you don't want the MicroPython serial REPL available.
usb.device.get().init(midi, builtin_driver=True)

# TX constants
CHANNEL = 0
PITCH = 60
CONTROLLER = 64

control_val = 0
print("init")

def main(key_scaled_state):
#    while not midi.is_open():
    while not midi.is_open():
        try:
            i = max(key_scaled_state)
            print("key is ",key_scaled_state.index(i))
            if (i < 110):
                print("no keys")
                Spkr.duty_u16(0)
            else:
                freq = 200+(40*key_scaled_state.index(i))
                Spkr.freq(freq)
                Spkr.duty_u16(32768)
            time.sleep_ms(100)
        except:
            pass

    #print("Starting MIDI loop...")
    while midi.is_open():
        Spkr.duty_u16(0)
        #print("scaled_key", key_scaled_state, previous_state)
        make_stack(key_scaled_state)
        UpdateMIDI()
        time.sleep(0.1)


