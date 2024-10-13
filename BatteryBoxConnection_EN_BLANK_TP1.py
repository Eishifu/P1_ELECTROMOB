
#TP1 ELECTROMOB - EXERCICE
"""This TP aim to programm the KUKA robot in order to recreate a part of a production line.

For this you have:

pykuka.py
    kuka.move_to_pose(Pose)       //PTP movement
    kuka.move_lin_to_pose(Pose)   //LIN movement
    kuka.close_tool()
    kuka.open_tool()

To send information to the KUKA robot, the program PC2KUKA_ELECTROMOB needs to be active on the KUKA KRL Lauer


"""

import time
from pykuka import Pose
import pykuka as kuka

#KUKA Robot connection
kuka.initialize("/dev/ttyS0")

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

    achieved = True
    return(achieved)


#________________________________Programme________________________________#
n=1
get_cell_conv()
inject()
place_into_box(n)
