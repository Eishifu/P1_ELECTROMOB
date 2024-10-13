
#TP ELECTROMOB - SOLUTION
"""This TP aim to programm the KUKA robot in order to recreate a part of a production line.

For this you have:

pykuka.py
    kuka.move_to_pose(Pose)       //PTP movement
    kuka.move_lin_to_pose(Pose)   //LIN movement
    kuka.close_tool()
    kuka.open_tool()

pc2esp32.py
    s=begin_one_connection(TCP_IP,TCP_PORT)
    end_one_connection(s:socket.socket)
    pin_value=get_pin_try(pin:int,s:socket.socket,nb_try:int,pr=True)
    open_gate_try(s:socket.socket,nb_try:int)
    close_gate_try(s:socket.socket,nb_try:int)

To send information to the KUKA robot, the program PC2KUKA_ELECTROMOB needs to be active on the KUKA KRL Lauer

To send information to the ESP32s, they need to be connected to the same WiFi hotspot than the pc, and you need to have their IP adresses.

"""

import time
from pykuka import Pose
import pykuka as kuka
import pc2esp32 as c

#KUKA Robot connection
kuka.initialize("/dev/ttyS0")

#ESP32 TCP Connection 
TCP_IP1 = '192.168.164.67'      #IP of the BOX
TCP_IP2 = '192.168.164.181'     #IP of the TABLE
#TCP_IP3 = '192.168.164.181'     #IP of the INJECTION PART
TCP_PORT = 10000

##########
#Points
##########

Exemple_point=Pose(1,1,1,2,2,2)



###########
#Functions
###########
def get_cell_conv():  #Process of taking the cell from the conveyor belt
    achieved=False
    #::::FILL THIS PROGRAMM
    print("Going to the conveyor belt")

    print("Starting to take the cell")

    print("Cell taken")

    print("Going to the injection support")

    print("Cell placed on injection support")

    achieved=True
    return(achieved)

def inject(): # Process of injecting electrolyte in the cell
    achieved=False
    #::::FILL THIS PROGRAMM

    #Step 1: Take the injection tool
    print("Starting to take the injection tool")

    print("Injection tool taken")

    print("Starting the injection")

    print("Injection initiated for 10s")
    time.sleep(10)
    print("Injection done")

    #Step 3: Put back the injection tool
    print("Returning the injection tool")

    print("Injection tool placed in his support")
   
    print("Injection process done")
    achieved=True

    return(achieved)

def place_into_box(n: int): #Process of taking the cell from the injection support and put it in the "n" position of the box
    achieved = False
    #::::FILL THIS PROGRAMM
    
    print("Starting to take the cell from the injection support")

    print("Cell taken")

    print("Going to cell space i")

    print("Cell dropped in cell space i")

    print("Return to home")

    achieved = True
    return(achieved)

def trigger_gate():
    """
    Open and then close the gate
    """
    success=False
    print("Asking to open the gate")
    opened=c.open_gate_try(s2,20)
    if opened:
        print("Gate opened")
        print("Asking to close the gate")
        closed=c.close_gate_try(s2,20)
    if closed:
        print("Gate closed")
        success=True
    return(success)

#Initial condition
"""
TO CHANGE according to initial condition
"""
nb_cell_conv=1                                                  #Number of cell coming on the conveyor
nb_cell_box=2                                                   #Number of cell already in the box
nb_cell_total=3                                                 #Total number of cell in the production chain
cell_pos_inject=False                                           #True if a cell is already on the injection support
pin_inj=2                                                       #PIN of the injection support trigger
cell_injected=False                                             #True if a cell is already injected and on the injection support 
pin_conv=22
cell_conv=False
pin_nb=[2,4,21,22,23]                                           #PINs of the triggers in the battery box
nb_boucle=0                                                     #Number of production loop done at the start

err=False                                                       #At the start we don't have any error, put it to True to not execute the loop

#________________________________Programme________________________________#

###Connection
s1,s1_bool=c.begin_one_connection(TCP_IP1,TCP_PORT)
s2,s2_bool=c.begin_one_connection(TCP_IP2,TCP_PORT)

###Production process###
#Initial state of pins
print("Initial state of the box pins")
box_pos=c.get_all_from_box(s1)
print(box_pos)
print("Initial state of the table's pins")
print(c.get_all_from_table(s2))

#Execution loop
"""Execute while the number of cell in the box is less than 5 and the max number of cell is not in the box.
Stops when the number of cell in the box is 5 or when the total number of cells are in the box.
"""
while  nb_cell_box<5 and nb_cell_box!=nb_cell_total and not err: 
    nb_boucle+=1
    print('Loop n°',nb_boucle)
    ###Update all parameters
    print("Check 1")
    #Check if there is a cell in the injection slot

    #If yes, write True in the cell_pos_inject variable

    #If no, write False in the cell_pos_inject variable
   
    #Check if there is a cell waiting on the conveyor belt
                                                 
    #If yes, write True in the cell_convt variable

    #If no, write False in the cell_convt variable

    ####Procédure 1 : Takes the cell from the conveyor and bring it to the injection slot####
    print("--------Procedure 1-------")
    #If there is no cell on the injection slot and a cell waiting on the conveyor

    #Go take the cell on the conveyor belt and bring it to the injection slot
                                            
    #If the operation wasa sucess, reduce by 1 the number of cell coming by the conveyor

    #and indicates that this cell was not yet injected
                                                      
    #If error

    #err variable at true

    ####Procédure 2 : Inject the electrolyte in the cell###
    print("--------Procedure 2-------")
    #If the cell is in place and not already injected

    #Start the injection procedure  
    #                                                                   
    #If the procedure does not finish                                               
     
    #variable err at True

    ####Procédure 3 : Takes the cell from the injection slot and put it in the box####
    print("--------Procedure 3-------")
    #If the cell in injected on the injection slot
    #she is not already placed in the box
    #We check every position of the box
    #If it is not already placed
    
    #Ask for the state of the slot i
    #Save it
    #If it is free
    #Choose it
    #Start the procedure to place it in slot i

    #After, verify if the trigger in the slot is triggered
    #If yes save it
    #The cell is placed
    #Add 1 to the number of cell in the box
    #If the trigger was not triggered

    #We have an error
    

#Go to initial position

print("End of process : deconnexion")

#End of connexions
c.end_one_connection(s1)
c.end_one_connection(s2)