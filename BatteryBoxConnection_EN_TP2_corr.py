
#TP ELECTROMOB - SOLUTION
"""This TP aim to programm the KUKA robot in order to recreate a part of a production line.

For this you have:

pykuka.py
    kuka.move_to_pose(POSE)       //PTP movement
    kuka.move_lin_to_pose(POSE)   //LIN movement
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
#!!!!!!WARNING!!!!!!! The points are invalid if the position of the installation are modified.
#Take
take1=Pose(-206.83,-295.25,353.54,-127.43,-87.42,-142.19)              #approximate first point in order to take the cell (p2)
take2=Pose(-206.83,-455.31,353.56,-127.36,-87.43,-142.26)              #second more precise point to take the cell (p3)
take3=Pose(-206.83,-496.27,353.56,-127.31,-87.43,-142.30)              #third point that start to place the tool around the cell (p9)
take4=Pose(-206.83,-504.80,353.55,-127.29,-87.42,-142.33)              #fourth point that puts the tool to the exact position (p10)
take_up1=Pose(-206.83,-504.80,460.43,-127.28,-87.42,-142.34)           #lift the cell when it is taken to this point (p4)
take_up2=Pose(-206.82,-238.3,460.43,-127.5,-87.42,-142.11)             #for a nicer trajectory (p5)
inter_traj=Pose(379.29,-43.91,655.75,-4.34,0.26,179.43)                #additionnal point for nicer trajectory (p11)
#Put for injection
inj_home=Pose(-60.58,419.15,659.58,89.58,-2.37,179.78)
put_inj1=Pose(-64.39,392.23,715.74,86.76,-2.97,178.66)
put_inj2=Pose(-63.96,422,619.25,87,-1.16,179.55)
put_inj3=Pose(-63.96,422,478.29,87,-1.16,179.55)
put_inj4=Pose(-63.96,422,530.63,87,-1.15,179.55)

#Take the injection piece
#inj_home as P1
injPc_take1 = Pose(-56.14, 331.88, 520.45, 85.74, -2.13, 179.71)       #Position above the injection piece support (P2)
injPc_take2 = Pose(-56.14, 331.88, 456.90, 85.74, -2.13, 179.71)       #Position of the "pince" right above the injection piece (P3)
injPc_take3 = Pose(-56.14, 331.88, 408.81, 85.74, -2.13, 179.70)       #Position of the "pince" to pick the injection piece (P4)
injPc_take_up=Pose(-56.13, 331.88, 559.26, 85.74, -2.13, 179.70)       #Position above the injection piece support and with the lowest part above the cell (P5)

#Injection
injPc_inject1 = Pose(-56.13, 430.82, 560.14, 85.74, -0.72, 179.60)     #Position above the cell (P6)
injPc_inject2 = Pose(-56.13, 430.81, 530.66, 85.74, -0.73, 179.60)     #Position of injection (P7) 

#Take from injection
#inj_home as P1
inj_take2 = Pose(-60.57, 420, 524.12, 88.79, -2.34, 179.45)         #Position of the "pince" passing the upper limit of the cell (P2)
inj_take3 = Pose(-60.58, 420, 473.66, 88.79, -2.35, 179.45)         #Position of the "pince" to pick the cell (P4)
inj_take_up = Pose(-60.57, 420, 622.89, 88.79, -2.35, 179.45)        #Position to take the cell out of the side supports (P5)

#Put in cell N
box1_home = Pose(-281.75, 126.81,  659.55, 179.17, -2.04, 178.78)       #Position of the cell above the box for the cell espace 1 (P6)
box1_b4enter = Pose(-281.75, 126.81, 635.94, 179.16, -2.04, 178.78)    #Position of the cell right above entering in the cell espace 1 (P7)
box1_inside = Pose(-281.75, 126.81,  519.96, 179.16, -2.04, 178.78)     #Position of the cell for dropping in cell espace 1 (P8)
box2_home = Pose(-329.2, 125, 659.52, 179.18, -2.06, 178.78)          #Position of the cell above the box for the cell espace 2 (P6)
box2_b4enter = Pose(-329.2, 125.4, 634.36, 179.17, -2.06, 178.78)       #Position of the cell right above entering in the cell espace 2 (P7)
box2_inside = Pose(-329.2, 125.4, 501.28, 179.17, -2.06, 178.78)        #Position of the cell for dropping in cell espace 2 (P8)
box3_home = Pose(-375.7, 126.81, 659.51, 179.17, -2.05, 178.78)       #Position of the cell above the box for the cell espace 3 (P6)
box3_b4enter = Pose(-375.7, 127, 632.77, 179.17, -2.05, 178.78)    #Position of the cell right above entering in the cell espace 3 (P7)
box3_inside = Pose(-375.7, 127, 496.96, 179.17, -2.05, 178.78)     #Position of the cell for dropping in cell espace 3 (P8)
box4_home = Pose(-423, 127, 659.51, 179.17, -2.05, 178.78)       #Position of the cell above the box for the cell espace 4 (P6)
box4_b4enter = Pose(-423, 127, 630.52, 179.17, -2.05, 178.78)    #Position of the cell right above entering in the cell espace 4 (P7)
box4_inside = Pose(-423, 127, 502.20, 179.17, -2.05, 178.78)     #Position of the cell for dropping in cell espace 4 (P8)
#box5_home = box4_home | To prevent hitting the upper suport of the battery box
box5_b4enter = Pose(-469, 127, 630.58, 179.18, -2.06, 178.78)    #Position of the cell right above entering in the cell espace 5 (P7)
box5_inside = Pose(-469, 127, 515.98, 179.18, -2.05, 178.78)     #Position of the cell for dropping in cell espace 5 (P8)

###########
#Functions
###########
def get_cell_conv():  #Process of taking the cell from the conveyor belt
    achieved=False
    print("Going to the conveyor belt")
    kuka.move_to_pose(inj_home)
    kuka.move_to_pose(inter_traj)
    kuka.move_to_pose(take1)
    print("Starting to take the cell")
    kuka.open_tool()
    kuka.move_to_pose(take2)
    kuka.move_to_pose(take3)
    kuka.move_to_pose(take4)
    kuka.close_tool()
    print("Cell taken")
    time.sleep(1)
    kuka.move_to_pose(take_up1)
    kuka.move_to_pose(take_up2)
    trigger_gate()
    print("Going to the injection support")
    kuka.move_to_pose(inter_traj)
    kuka.move_to_pose(put_inj1)
    kuka.move_to_pose(put_inj2)
    kuka.move_to_pose(put_inj3)
    kuka.open_tool()
    print("Cell placed on injection support")
    time.sleep(1)
    kuka.move_to_pose(put_inj4)
    kuka.move_to_pose(inj_home)
    achieved=True
    return(achieved)

def inject(): # Process of injecting electrolyte in the cell
    achieved=False
    #t_start = time.time()
    kuka.move_to_pose(inj_home)

    #Step 1: Take the injection tool
    print("Starting to take the injection tool")
    kuka.move_to_pose(injPc_take1)
    kuka.move_lin_to_pose(injPc_take2)
    kuka.move_lin_to_pose(injPc_take3)
    kuka.close_tool()
    print("Injection tool taken")
    time.sleep(1)
    kuka.move_lin_to_pose(injPc_take_up)
    #t_step1 = time.time() - t_start

    #Step 2: Simulate the injection process
    print("Starting the injection")
    kuka.move_to_pose(injPc_inject1)
    kuka.move_lin_to_pose(injPc_inject2)
    print("Injection initiated for 10s")
    time.sleep(10)
    print("Injection done")
    kuka.move_lin_to_pose(injPc_inject1)
    #t_step2 = time.time() - t_start

    #Step 3: Put back the injection tool
    print("Returning the injection tool")
    kuka.move_to_pose(injPc_take_up)
    kuka.move_lin_to_pose(injPc_take2)
    kuka.move_lin_to_pose(injPc_take3)
    kuka.open_tool()
    print("Injection tool placed in his support")
    time.sleep(1)
    kuka.move_lin_to_pose(injPc_take_up)
    #t_step3 = time.time() - t_start

    #End of process
    kuka.move_to_pose(inj_home)
    print("Injection process done")
    achieved=True
    #t_injProcess = time.time() - t_start

    return(achieved)

def place_into_box(n: int): #Process of taking the cell from the injection support and put it in the "n" position of the box
    achieved = False

    if type(n) != int:
        print("Input is not valid, must be an integer")
        return(achieved)
    elif n < 1 or n > 5:
        print("Input is not valid, must be an integer in the interval [1,5]")
        return(achieved)
    else:
        #Step 1: Pick the cell from inject pos
        kuka.move_to_pose(inj_home)
        print("Starting to take the cell from the injection support")
        kuka.move_lin_to_pose(inj_take2)
        kuka.move_lin_to_pose(inj_take3)
        kuka.close_tool()
        print("Cell taken")
        time.sleep(1)
        kuka.move_lin_to_pose(inj_take_up)
        kuka.move_to_pose(inj_home)

        #Step 2: Place it in the espace of cell N
        if n == 1:
            print("Going to cell space 1")
            kuka.move_to_pose(box1_home)
            kuka.move_to_pose(box1_b4enter)
            kuka.move_lin_to_pose(box1_inside)
            kuka.open_tool()
            print("Cell dropped in cell space 1")
            time.sleep(1)
            kuka.move_lin_to_pose(box1_b4enter)
            kuka.move_to_pose(box1_home)
        elif n == 2:
            print("Going to cell space 2")
            kuka.move_to_pose(box2_home)
            kuka.move_to_pose(box2_b4enter)
            kuka.move_lin_to_pose(box2_inside)
            kuka.open_tool()
            print("Cell dropped in cell space 2")
            time.sleep(1)
            kuka.move_lin_to_pose(box2_b4enter)
            kuka.move_to_pose(box2_home)
        elif n == 3:
            print("Going to cell space 3")
            kuka.move_to_pose(box3_home)
            kuka.move_to_pose(box3_b4enter)
            kuka.move_lin_to_pose(box3_inside)
            kuka.open_tool()
            print("Cell dropped in cell space 3")
            time.sleep(1)
            kuka.move_lin_to_pose(box3_b4enter)
            kuka.move_to_pose(box3_home)
        elif n == 4:
            print("Going to cell space 4")
            kuka.move_to_pose(box4_home)
            kuka.move_to_pose(box4_b4enter)
            kuka.move_lin_to_pose(box4_inside)
            kuka.open_tool()
            print("Cell dropped in cell space 4")
            time.sleep(1)
            kuka.move_lin_to_pose(box4_b4enter)
            kuka.move_to_pose(box4_home)
        elif n == 5:
            print("Going to cell space 5")
            kuka.move_to_pose(box4_home)
            kuka.move_to_pose(box5_b4enter)
            kuka.move_lin_to_pose(box5_inside)
            kuka.open_tool()
            print("Cell dropped in cell space 5")
            time.sleep(1)
            kuka.move_lin_to_pose(box5_b4enter)
            kuka.move_to_pose(box4_home)
        
        #Step 3: Return to Home Position (inj_home)
        kuka.move_to_pose(inj_home)
        achieved = True
        return(achieved)

def trigger_gate():
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

###
'''
print("Checking functionnalities")
kuka.move_to_pose(inj_home)
kuka.close_tool()
kuka.open_tool()
'''
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
    inj=c.get_pin_try(pin_inj,s2,10)                                    #Check if there is a cell in the injection slot
    if inj==1: 
        cell_pos_inject==True                                           #If yes, write True in the cell_pos_inject variable
        print("Cell detected in injection support")
    else: 
        cell_pos_inject == False                                        #If no, write False in the cell_pos_inject variable
        print("No  cell detected in injection support")
    print("Check 2")
    convt=c.get_pin_try(22,s2,10)
    if convt==1:                                                        #Check if there is a cell waiting on the conveyor belt
        cell_conv=True                                                  #If yes, write True in the cell_convt variable
        print("Cell detected on the conveyor")
    else:
        cell_conv=False                                                 #If no, write False in the cell_convt variable
        print("No cell detected on the conveyor")

    ####Procédure 1 : Takes the cell from the conveyor and bring it to the injection slot####
    print("--------Procedure 1-------")
    if not cell_pos_inject and cell_conv:                               #If there is no cell on the injection slot and a cell waiting on the conveyor
        cell_pos_inject= get_cell_conv()                                #Go take the cell on the conveyor belt and bring it to the injection slot
        if cell_pos_inject:                                             
            nb_cell_conv -= 1                                           #If the operation wasa sucess, reduce by 1 the number of cell coming by the conveyor
            cell_injected = False                                       #and indicates that this cell was not yet injected
        else:                                                           
            print("error on procedure 1")                               #If error
            err=True                                                    #err variable at true, stops the process

    ####Procédure 2 : Inject the electrolyte in the cell###
    print("--------Procedure 2-------")
    if not cell_injected and not err and cell_pos_inject:               #If the cell is in place and not already injected
        cell_injected = inject()                                        #Start the injection procedure                                                                    
        if not cell_injected:                                           #If the procedure does not finish                                               
            print ("error while injecting")                             
            err=not cell_injected                                       #variable err at True

    ####Procédure 3 : Takes the cell from the injection slot and put it in the box####
    print("--------Procedure 3-------")
    if cell_injected and not err and cell_pos_inject:                   #If the cell in injected on the injection slot
        placed = False                                                  #she is not already placed in the box
        for i in range (5):                                             #We check every position of the box
            if not placed and not err:                                  #If it is not already placed
                print("Asking for the cell slot :",i+1)
                res=c.get_pin_try(pin_nb[i],s1,20)                      #Ask for the state of the slot i
                box_pos[i]=res                                          #Save it
                if box_pos[i]== 0.0:                                    #If it is free
                    print("Slot ",i+1," choosed")                       #Choose it
                    err = not place_into_box(i+1)                       #Start the procedure to place it in slot i
                    res = c.get_pin_try(pin_nb[i],s1,20)
                    if res==1:                                          #After, verify if the trigger in the slot is triggered
                        box_pos[i]=res                                  #If yes save it
                        placed = True                                   #The cell is placed
                        nb_cell_box+=1                                  #Add 1 to the number of cell in the box
                    else:                                               #If the trigger was not triggered
                        print("Error while putting the cell on the box/trigger not triggered")
                        err=True                                        #We have an error
    

#Go to initial position

kuka.move_to_pose(inj_home)
print("End of process : deconnexion")

#End of connexions
c.end_one_connection(s1)
c.end_one_connection(s2)