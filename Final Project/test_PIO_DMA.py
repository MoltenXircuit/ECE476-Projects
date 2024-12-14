import array

from micropython import const
from rp2 import PIO, DMA, asm_pio, StateMachine
import time
from machine import Pin

#make a custom data type array for key states

#─────[ IO Definitions ]────────────────────────────────────

key1 = Pin(15,Pin.IN,Pin.PULL_UP)
key2 = Pin(14,Pin.IN,Pin.PULL_UP)

wave_start = Pin(18,Pin.OUT)
wave1 = Pin(19,Pin.IN)
wave2 = Pin(20,Pin.IN)
wave3 = Pin(21,Pin.IN)

wave_start.value(1)

#─────[ Register Definitions ]────────────────────────────────────
    #DREQ's gotten from rp2040 datasheet 2.5.3
SIZE_BYTE       = const(0)
DREQ_PIO0_TX0   = const(0)
DREQ_PIO0_TX1   = const(1)
DREQ_PIO0_TX2   = const(2)
DREQ_PIO0_TX3   = const(3)
DREQ_PIO0_RX0   = const(4)
DREQ_PIO0_RX1   = const(5)
DREQ_PIO0_RX2   = const(6)
DREQ_PIO0_RX3   = const(7)

    #PIO Register List for DMA pointer gotten from rp2040 datasheet 3.7 (not needed with new DMA library)
PIO0_BASE   = const(0x50200000)
PIO1_BASE   = const(0x50300000)
RXF0        = const(0x010)
RXF1        = const(0x014)
RXF2        = const(0x018)
RXF3        = const(0x01c)
TXF0        = const(0x020)
TXF1        = const(0x024)
TXF2        = const(0x028)
TXF3        = const(0x02c)

#─────[ Variable Definitions ]────────────────────────────────────


#─────[ PIO Code ]────────────────────────────────────

@asm_pio()
#@asm_pio(sideset_init=PIO.OUT_LOW)
def keys_in():
    wrap_target()
    pull()
    mov(y, osr)                 # y = Number of keys
    wait(0,pin,0)               # skip first pulse

    label("loop_not_zero")      # 
    mov(x, 0b10111)                 # reset x = 0b0000_0000_0000_0000
    mov(x, 0xffffffff)                 # reset x = 0b0000_0000_0000_0000
    wait(0,pin,0)               # wait for wave_start to go low
    
    label("loop")               # 
    jmp(pin,"loop_high")        # when wave pin is high, stop counting 
    jmp(x_dec,"loop")           # else count down and loop
    jmp("loop_high")            # loop again 
    
    label("loop_high")          # 
    in_(y, 32)                  # Copy 8 bits of counter into ISR
    push()                      # push isr to pio_rx
    jmp(y_dec,"loop_not_zero")  # if y is not 0, decrease key count
    wrap()

#─────[ Prepare state machine and start it ]────────────────────────────────────
sm0 = StateMachine(0,keys_in, freq=1_000_000, set_base=wave_start, in_base=wave_start, jmp_pin=wave1)
#sm0.active(1)

#─────[ Allocate array to store data ]──────────────────────────────────────────

N = const(7)
dst = bytearray(N)
key_time = bytearray([0] * N)
key_time_min = ([255] * N)
key_time_max = ([0] * N)
key_scale_array = ([1] * N)

key_scaled_state = ([0] * N)
previous_state = ([0] * N)

delta_key_stack = ([0,0])



#─────[ Prepare DMA for PIO to memory transfer ]────────────────────────────────
#startDMA
dma = DMA()
control = dma.pack_ctrl(inc_read=False, inc_write=True, size=SIZE_BYTE, bswap=1, treq_sel=DREQ_PIO0_RX0)
dma.config(read=sm0,
           write=dst,
           ctrl=control)


#─────[ Start DMA and start PIO ]──────────────────────────────────────
def ReadKeyboard():
    print("starting PIO")
    sm0.restart()
    i = sm0.rx_fifo()
    while(i>0):             #throw out last pio fifo data
        #print(i)
        sm0.get()
        i = i-1
    sm0.put(N)
    time.sleep(0.01) #needs delay for put to work
    sm0.active(True)
    print("starting DMA")
    dma.config(write=dst,count=N)
    time.sleep(0.01)
    dma.active(True)
    time.sleep(0.01)
    wave_start.value(0)
#    time.sleep(0.01)
#    if(dma.active() == 0):
#        dma.close

#─────[ Main ]────────────────────────────────────

while True:
    ReadKeyboard()
    time.sleep(0.5)
    print(sm0.rx_fifo())
    print([x for x in dst], sm0.active(), dma.active())
    #print(dst, sm0.active(), dma.active())
    wave_start.value(1)
    time.sleep(0.01)

