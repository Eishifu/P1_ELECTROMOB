"""
Programm to test the connection to the ESP32s and the functionality of the motor gate.
"""

import pc2esp32 as c

#IP ADRESSES
TCP_IP_2 = '192.168.164.181'  #table esp32
#TCP_IP_3 = '192.168.164.xx'  #injection esp32
TCP_PORT = 10000


s2,process2=c.begin_one_connection(TCP_IP_2,TCP_PORT)

if process2:
    success=False
    opened=c.open_gate_try(s2,20)
    if opened:
        print("Gate opened")
        #sleep(1)
        closed=c.close_gate_try(s2,20)
        print("Asking to close the gate")
    if closed:
        print("Gate closed")
        success=True
    

c.end_one_connection(s2)

