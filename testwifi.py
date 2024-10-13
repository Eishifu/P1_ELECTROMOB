"""
Programm to test the connection to the ESP32s.

A value of -1, is a timeout
"""

import pc2esp32 as c

#IP ADRESSES
TCP_IP_1 = '192.168.164.67' #box esp32
TCP_IP_2 = '192.168.164.181'  #table esp32
#TCP_IP_3 = '192.168.164.xx'  #injection esp32
TCP_PORT = 10000

s1,process1=c.begin_one_connection(TCP_IP_1,TCP_PORT)
s2,process2=c.begin_one_connection(TCP_IP_2,TCP_PORT)

if process1 and process2:
    print("Asking for the informations of the box and the table")
    print(c.get_all_from_box(s1))
    print(c.get_all_from_table(s2))
    
c.end_one_connection(s1)
c.end_one_connection(s2)

