from machine import Pin, bitstream
import _thread
import network
from time import sleep
import socket

#-----------------NeoPixel Code--------------------
tree_status = float(0)
gNeoCommand = 0
def runNeopixel():
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
        global tree_status
        timing = [300, 900, 700, 500]
        np = Pin(12, Pin.OUT)
        tree_status = 0
        X = bytearray([0,0,0]*N)
        bitstream(np, 0, timing, X)
        
    def starter_tree(N):
        global tree_status
        timing = [300, 900, 700, 500]
        np = Pin(12, Pin.OUT)
        timing = [300, 900, 700, 500]
        X = bytearray([20,20,0])
        tree_status = (1/N)
        sleep(1)
        bitstream(np, 0, timing, X)
        print("a")
        for neo in range(1,N-1):
            tree_status = ( (neo+1) /N)
            sleep(0.2)
            addLight(X,'Y')
            bitstream(np, 0, timing, X)
            print("b")
        sleep(1)
        addLight(X,'G')
        tree_status = 1
        bitstream(np, 0, timing, X)
        print("c")
        
    global gNeoCommand
    #global starter_tree_reset, starter_tree
    N = 8
    starter_tree_reset(N)
    reset = 1
    while(1):
        if ((gNeoCommand == 1) and (reset == 1)):
            starter_tree(N)
            gNeoCommand = 0
            reset = 0
        elif ((gNeoCommand == 2) and (reset == 0)):
            starter_tree_reset(N)
            gNeoCommand = 0
            reset = 1
        else:
            sleep(0.2)


#-----------------Webpage Code--------------------

def web_page(ip_address, LED):
    global tree_status
    f = open("Input.html")

    x = f.read()
    x = x.replace('\r\n',' ')
    x = x.replace('aaaaa',ip_address)
    x = x.replace('bbbbb', str(LED))
    x = x.replace('vStatus', str(tree_status))
    
    return(x)
Button14 = Pin(14, Pin.IN, Pin.PULL_UP)
Button15 = Pin(15, Pin.IN, Pin.PULL_UP)
LED1 = Pin(16, Pin.OUT)
OnOff = ['OFF', 'ON']


ssid = 'Pico-Network'
password = 'PASSWORD'

ap = network.WLAN(network.AP_IF)
ap.config(ssid=ssid, password=password)
ap.active(True)

while ap.active() == False:
    pass
print('AP Mode Is Active, You can Now Connect')
IP_Address = ap.ifconfig()[0]
print('IP Address To Connect to:: ' + IP_Address)

print('Channel',  ap.config('channel'))
      
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
_thread.start_new_thread(runNeopixel,())
reset = 1

while(1):
    flag = 0
    while(flag == 0):
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = request.decode('utf-8')
        if(request.find('favicon') > 0):
            print('--------------------')
            print('Got a connection from %s' % str(addr))
            flag = 1
        else:
            response = web_page(IP_Address, OnOff[LED1.value()] )
            conn.send(response)
            conn.close()

    n = request.find('Referer:')+9
    request = request[n:]
    n = request.find('\r\n')
    request = request[0:n]
    for i in range(0,10):
        n = request.find('/')+1
        if(n>0):
            request = request[n:]
    if ((Button15.value() == 0) and (reset == 1)):
        gNeoCommand = 1
        reset = 0
    elif ((Button14.value() == 0) and (reset == 0)):
        gNeoCommand = 2
        reset = 1
    else:
        sleep(0.1)

    response = web_page(IP_Address, LED1.value() )
    conn.send(response)
    conn.close()




