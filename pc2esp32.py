# PC to ESP32 - TCP connection
# Receive and Transmit a float in binary to ESP32 server
"""Here you can find the function to connect this PC to ESP32 with a WiFi hotspot.

1 - The ESP32s and the PC need to be connected to the same WiFi connection with the same open port.

2 - You need to get the IP adress of each ESP32 with a PC. It depends of the WiFi network used.

3 - Used function for the Electromob TP are:

begin_one_connection(TCP_IP,TCP_PORT)
end_one_connection(s:socket.socket)
get_pin_try(pin:int,s:socket.socket,nb_try:int,pr=True)
open_gate_try(s:socket.socket,nb_try:int)
close_gate_try(s:socket.socket,nb_try:int)

You can use the variation of these functions depending of the case, but with these function all can be done.

"""

#Importations
import socket
import struct
import multiprocessing.pool
import functools
from time import sleep

###FUNCTION DECLARATION
def timeout(max_timeout: float):
    """ timeout
    DEF: Timeout decorator function that can be applied to a function at the declaration. If the function process time exceed the timeout value, rise a timeout error.
    to apply the timeout, follow this model: 
                                                @timeout(max_timeout)
                                                def function():
                                                    .....
    INPUTS: max_timeout(float value in second) 
    """
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator

#connection functions
@timeout(50)
def connect2esp32(TCP_IP:str,TCP_PORT:int):
    """connect2esp32
    DEF: Base function to start a connexion. Return the socket of the connection.
    the timeout function is attached: if the connexion takes more than 20s rises an error.
    INPUTS: TCP_IP(string of the IP ADRESS of the ESP32 to reach); TCP_PORT(int value of the PORT).
    OUTPUTS: s(socket of the connection)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a socket
    print("Connextion attempt to :",TCP_IP, "on the port :", TCP_PORT)
    s.connect((TCP_IP, TCP_PORT)) #connect the socket
    print("connected")
    return(s)                     #return the socket

def begin_one_connection(TCP_IP_1,TCP_PORT):
    """begin_one_connection
    DEF: connects to the IP and PORT specified and return the socket. 
    INPUTS: TCP_IP_1(IP to connect to it);TCP_PORT(PORT to connect to it).
    OUTUTS:s(socket of the connection);succesful(bool to confirm the succes of the connection).
    ERROR: If a timeout occur, return two False booleans.
    """
    succesful=True
    try:
        s=connect2esp32(TCP_IP_1, TCP_PORT)
    except OSError or multiprocessing.context.TimeoutError: 
        print('timeout, could not connect')
        succesful=False
        s=False
    return(s,succesful)
def begin_all_connections(TCP_IP_1,TCP_IP_2,TCP_IP_3,TCP_PORT):
    """begin_all_connections
    DEF: connects to all ESP32 specified with the IPs and the PORT
    INPUTS: TCP_IP_1(IP 1 to connect to it);TCP_IP_1(IP 2 to connect to it);TCP_IP_1(IP 3 to connect to it);TCP_PORT(PORT to connect to it).
    OUTUTS: s1(socket of the connection 1); s2(socket of the connection 2); s3(socket of the connection 3);succesful(bool to confirm the succes of the connection).
    ERROR: If a timeout occurs, return False booleans.
    """
    succesful=True
    try:
        s1=connect2esp32(TCP_IP_1, TCP_PORT)
    except OSError or multiprocessing.context.TimeoutError: 
        print('timeout,could not connect to s1')
        succesful=False
        s1=False
    try:
        s2=connect2esp32(TCP_IP_2, TCP_PORT)
    except OSError or multiprocessing.context.TimeoutError:
        print('timeout,could not connect to s2')
        succesful=False
        s2=False
    try:
        s3=connect2esp32(TCP_IP_3, TCP_PORT)
    except OSError or multiprocessing.context.TimeoutError:
        print('timeout,could not connect to s3')
        succesful=False
        s3=False
    return(s1,s2,s3,succesful)
def end_one_connection(s):
    """end_one_connection
    DEF: end the specified socket connection; if a given input is not socket.socket, ignore it.
    INPUTS: s(socket to close)
    """
    if isinstance(s,socket.socket):
        try :
            s.close()
            print("socket closed")
        except NameError or OSError or AttributeError:
            print("socket already closed") 
def end_all_connections(s1,s2,s3):
    """end_all_connections
    DEF: end the three specified sockets connections; if a given input is not socket.socket, ignore it.
    INPUTS:s1(socket to close);s1(socket to close);s1(socket to close)
    """
    if isinstance(s1,socket.socket):
        try :
            s1.close()
            print("s1 closed")
        except NameError or OSError or AttributeError:
            print("s1 already closed")
    if isinstance(s2,socket.socket):
        try :
            s2.close()
            print("s2 closed")
        except NameError or OSError or AttributeError:
            print("s2 already closed")
    if isinstance(s3,socket.socket):
        try :
            s3.close()
            print("s3 closed")
        except NameError or OSError or AttributeError:
            print("s3 already closed")

#get and receive functions
@timeout(20)
def get_pin(pin:int,s:socket.socket,pr=True):
    """get_pin
    DEF: Get the float value of a pin from a connected ESP32
    the timeout function is attached: if the function takes more than 5s rises an error.
    INPUT:pin(int value of the pin);s(socket from which we ask the pin);pr(bool condition to print the steps in the terminal)
    OUTPUT:received_value(float value received from the ESP32)
    ERROR: if received -1, the value that was received was not a proper float
    """
    value=pin
    ba = bytearray(struct.pack("f", value)) 
    s.send(ba)
    if pr:print(f"Requested pin value: {value}")
    # Receive data from the server (expecting a float)
    data = s.recv(4)  # float is 4 bytes
    if len(data) == 4:
        received_value = struct.unpack("f", data)[0]
        if pr: print(f"Received value from server: {received_value}")
        
    else:
        if pr: print("Did not receive proper float data.")
        received_value=-1
    return(received_value)
def get_pin_to(pin:int,s:socket.socket,pr=True):
    """get_pin_to
    DEF: adds a expections handler for the timeout. This is for preventing for stopping the code when asking for a pin.
    INPUTS:pin(int value of the pin);s(socket from which we ask the pin);pr(bool condition to print the steps in the terminal).
    OUTPUT:received_value(float value received from the ESP32).
    ERROR: if received -1, timeout of not proper float received.
    """
    try :result=get_pin(pin,s,pr)
    except multiprocessing.context.TimeoutError:
        print("timeout")
        result=-1
    return(result)
def get_pin_try(pin:int,s:socket.socket,nb_try:int,pr=True):
    while (nb_try>0): 
        r=get_pin_to(pin,s,pr)
        nb_try-=1
        if r!=-1:
            nb_try=0
    return(r)
  
def get_all_from_box(s:socket.socket): 
    """get_all_from_box 
    DEF: get the pin value of all the slots in the box
    INPUTS: s(socket of the ESP32 inside the box)
    OUTPUTS: t(vector containing all the pin values)
    """
    p1=get_pin_to(2,s,False)
    p2=get_pin_to(4,s,False)
    p3=get_pin_to(21,s,False)
    p4=get_pin_to(22,s,False)
    p5=get_pin_to(23,s,False)
    t=[p1,p2,p3,p4,p5]
    return(t)
def get_all_from_table(s:socket.socket): 
    """get_all_from_box 
    DEF: get the pin value of all the slots in the box
    INPUTS: s(socket of the ESP32 inside the box)
    OUTPUTS: t(vector containing all the pin values)
    """
    p1=get_pin_to(4,s,False)
    p2=get_pin_to(21,s,False)
    p3=get_pin_to(22,s,False)
    p4=get_pin_to(23,s,False)
    t=[p1,p2,p3,p4]
    return(t)
#Gate movements 
def move_motor(code:int,s:socket.socket):
    """move_motor
    DEF: Base function that send a float code to the ESP32 on the socket s, this code can be 50 to close the barrier, 51 to open it. Receive a value depending of the succes of the operation.
    The rotation direction can be exchanged depending on the wires connection of the motor and the pins.
    the timeout function is attached: if the function takes more than 10s rises an error.
    INPUTS: code(int value corresponding to an action); s(socket to reach).
    OUTPUT: received_value(int value, 2=succes,-1=failure).
    """
    success1=False
    while not success1:
        try: 
            success1=mm1(code,s)
            print("command received by ESP32")
        except  multiprocessing.context.TimeoutError:
            print("timeout,sending again")
    print("Waiting for the end of the command")
    try: 
        success2=mm2(s)
        print("Command succesfully done by ESP32")
    except  multiprocessing.context.TimeoutError:
        success2=False
        print("timeout")
    return(success2)
@timeout(20)
def mm1(code,s:socket.socket):
    '''mm1
    DEF: Part of motor move function
    '''
    success=False
    value=code
    ba = bytearray(struct.pack("f", value)) 
    s.send(ba)
    # Receive data from the server (expecting a float)
    data = s.recv(4)  # float is 4 bytes
    if len(data) == 4:
        confirmation_value = struct.unpack("f", data)[0]
    else:
        confirmation_value=-1
    if confirmation_value==2:
        success=True
    return(success)
@timeout(30)
def mm2(s:socket.socket):
    '''mm2
    DEF:Part of motor move function
    '''
    success=False
    data2 = s.recv(4)  # float is 4 bytes
    if len(data2) == 4:
        received_value = struct.unpack("f", data2)[0]
    else:
        received_value=-1
    if received_value==3:
        success=True
    return(success)

def open_gate(s:socket.socket):
    """open_gate
    DEF: command to open the gate on the conveyor belt
    INPUT: s(socket to reach)
    OUTPUT: succesful(bool that give the succes information)
    """
    succesful=False
    print(f"Requested opening of barrier")
    succesful=move_motor(51,s)
    return(succesful)
def open_gate_try(s:socket.socket,nb_try:int):
    """open_gate_try
    DEF: open_gate until nb_try is achieved or succes of command
    INPUT: s(socket to reach);nb_try(maximum try of the command)
    OUTPUT: closed(bool that confirms the succes of the command)
    """
    opened=False
    while not opened and nb_try>0:
        opened=open_gate(s)
        sleep(2)
        nb_try-=1
    return(opened)
def close_gate(s:socket.socket):
    """close_gate
    DEF: command to close the gate on the conveyor belt
    INPUT: s(socket to reach)
    OUTPUT: succesful(bool that give the succes information)
    """
    succesful=False
    print(f"Requested closing of barrier")  
    succesful=move_motor(50,s)
    return(succesful)
def close_gate_try(s:socket.socket,nb_try:int):
    """close_gate_try
    DEF: close_gate until nb_try is achieved or succes of command
    INPUT: s(socket to reach);nb_try(maximum try of the command)
    OUTPUT: closed(bool that confirms the succes of the command)
    """
    closed=False
    while not closed and nb_try>0:
        closed=close_gate(s)
        sleep(2)
        nb_try-=1
    return(closed)


# if this is the main file, executes. Used for debugging
if __name__=="__main__": 
    #IP ADRESS of the three ESP32s
    TCP_IP_1 = '192.168.164.181'    #ESP32 inside the box
    TCP_IP_2 = '192.168.164.67'     #ESP32 for the barrier and the injection slot
    TCP_IP_3 = '192.168.164.67'     #ESP32 inside the injection TOOL
    TCP_PORT = 10000                #Port of communication
    #BUFFER_SIZE = 1024              #Size 
    #used to test and debug
    s1,s2,s3,process=begin_all_connections(TCP_IP_1,TCP_IP_2,TCP_IP_3,TCP_PORT)
    while process:
        #print("Valeurs recu",get_all())
        #get_pin_to(2,s1)
        sleep(3)
    end_all_connections(s1,s2,s3)






