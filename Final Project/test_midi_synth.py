from machine import Pin
from micropython import const
import usb.device
from usb.device.midi import MIDIInterface
import time

#---------------------IO Definitions------------------------------
spkr = Pin(13,Pin.OUT)
led = Pin(25, Pin.OUT)

midi = MIDIInterface()

#---------------------Definitions------------------------------

_MIDI_POLY_KEYPRESS = const(0xA0)
_CIN_POLY_KEYPRESS = const(0xA)

N = const(7)
delta_key_stack = ([1,250], [3,200], [1,0], [0,0], [3,0], [1,250], [3,200], [1,0], [0,0], [3,0], [1,250], [3,200], [1,0], [0,0], [3,0], [1,250], [3,200], [1,0], [0,0], [3,0], [1,250], [3,200], [1,0], [0,0], [3,0], [1,250], [3,200], [1,0], [0,0], [3,0], [1,250], [3,200], [1,0], [0,0], [3,0], [1,250], [3,200], [1,0], [0,0], [3,0], [1,250], [3,200], [1,0], [0,0], [3,0])
previous_state = ([0] * N)

#---------------------Midi Update-------------------------

def UpdateMIDI():
    if ( sizeof(delta_key_stack) > 1 ):
        key = delta_key_stack.popleft()
        i = key[0]
        key_volume = key[1]    #using a list as a queue
        if (i<0):
            pass
        elif (previous_state[i] == 0):
            previous_state[i] = 1
            midi.note_on(CHANNEL, 60, (key_volume-1)/2)
            
        elif (key_volume == 0):
            previous_state[i] = 0
            midi.note_off(CHANNEL, 60)
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

while True:
    while not midi.is_open():
        time.sleep_ms(100)

    #print("Starting MIDI loop...")
    while midi.is_open():
        UpdateMIDI()
        time.sleep(2)









        """
        time.sleep(5)
        #print(f"TX Note On channel {CHANNEL} pitch {PITCH}")
        midi.note_on(CHANNEL, PITCH, 120)  # Velocity is an optional third argument
        time.sleep(0.1)
        #print(f"TX Note Off channel {CHANNEL} pitch {PITCH}")
        midi.note_off(CHANNEL, PITCH, 120)
        time.sleep(1)
        #print(f"TX Control channel {CHANNEL} controller {CONTROLLER} value {control_val}")
        midi.control_change(CHANNEL, CONTROLLER, control_val)
        control_val += 1
        if control_val == 0x7F:
            control_val = 0
        time.sleep(1)
        """
    #print("USB host has reset device, example done.")

