import serial
#s = serial.Serial() # TODO
s=serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0)

# characters used to communicate
DLE = 16
STX = 2
ETX = 3
EOT = 4
DONE = 35        # '#' sent by the KUKA when it reaches the required location
GO = 72          # 'G' means 'GO' GO = 71   
HOME = 71        # 'H' means 'HOME' 
POS = 80         # 'P' means current 'POSITION'
EXIT = 88        # 'X' means 'EXIT'
GRAB = 25
DROP = 27
YES = 89         # 'Y' means yes
NO = 78          # 'N' means no
REL=73
LIN = 74         # 'L' means go linear = 74

class Pose:
    """Represents a pose (position x, y, z, and orientation a, b, c) of the robot."""
    def __init__(self, x, y, z, a, b, c):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c
    
    @classmethod
    def from_string(cls, string):
        """Build a pose object from a string. The string must consist of 6 double values separated by spaces."""
        s = string.split(' ')
        return cls(float(s[0]), float(s[1]), float(s[2]), float(s[3]), float(s[4]), float(s[5]))
    
    def to_string(self):
        """Convert the pose object into a string. 6 doubles values separated by spaces are returned."""
        return f"{format(self.x, '010.6f')} {format(self.y, '010.6f')} {format(self.z, '010.6f')} {format(self.a, '010.6f')} {format(self.b, '010.6f')} {format(self.c, '010.6f')}"
    
    def copy(self):
        """Return a copy of the pose"""
        return Pose(self.x, self.y, self.z, self.a, self.b, self.c)

    def __repr__(self):
        return f"X = {self.x}; Y = {self.y}; Z = {self.z}; A = {self.a}; B = {self.b}; C = {self.c}"

def calculate_bcc(input, init_value):
    """Calculate the BCC of a byte array to check for transmission errors."""
    bcc = init_value
    for i in input:
        bcc ^= i
    return bcc

def read_3964R_data_buffer():
    """Read a byte buffer from the robot using the 3964R protocol. Block until the buffer is received."""
    s.read_until(bytes([STX]))                    # wait for STX
    s.write(bytes([DLE]))                         # then send DLE
    payload = s.read_until(bytes([DLE, ETX]))     # read the payload until DLE ETX
    bcc = s.read()[0]                             # read the BCC
    s.write(bytes([DLE]))                         # write DLE
    if bcc != calculate_bcc(payload, 0):
        print(payload)
        raise Exception("Transmission error")     # throw error if received BCC does not match calculated BCC
    return payload[:-2]                           # strip DLE and ETX and return the payload

def read_3964R_string():
    """Read a buffer from the robot using the 3964R protocol, and convert it to a string. Block until the string is received."""
    return read_3964R_data_buffer().decode('utf-8')

def read_3964R_pose():
    """Read a buffer from the robot using the 3964R protocol, and convert it to a pose. Block until the pose is received. The conversion is done by the from_string method of the Pose class: the buffer must consist of six double values separated by spaces. This function must be used when the SEND function is called in the robot program."""
    return Pose.from_string(read_3964R_data_buffer().decode('utf-8'))

def read_3964R_single_char():
    """Read a buffer from the robot using the 3964R protocol, and return the first char sent. Block until the char is received. This function must be used when the SEND_CHAR function is called in the robot program."""
    return read_3964R_data_buffer()[0]

def send_3964R_data_buffer(input_bytes):
    """Send a byte buffer to the robot using the 3964R protocol."""
    s.write(bytes([STX]))                         # send STX until we get DLE
    while(s.read()[0] != DLE):
        s.write(bytes([STX]))
    payload = input_bytes + bytes([DLE, ETX])     # add BLE ETX to the payload
    bbc = calculate_bcc(payload, 0)               # calculate BCC to be added to the payload
    s.write(payload + bytes([bbc]))               # send payload DLE ETX BCC
    s.read_until(bytes([DLE]))                    # wait for DLE

def send_3964R_string(string):
    """Send a string to the robot using the 3964R protocol. The string is converted to a byte buffer and is then sent."""
    send_3964R_data_buffer(bytes(string, 'utf-8'))

def send_3964R_single_char(byte):
    """Send a single character to the robot using the 3964R protocol. The character is converted to a size 1 byte buffer and is then sent. This function must be used when the READ_CHAR function is called in the robot program."""
    send_3964R_data_buffer(bytes([byte]))

def send_3964R_single_double(double):
    """Send a double value to the robot using the 3964R protocol. The value converted to a byte buffer formated as 000.000000 and is then sent. This function must be used when the READ_DOUBLE is called is the robot program."""
    send_3964R_data_buffer(bytes(format(double, '010.6f'), 'utf-8'))

def go_to_pose(pose, movement_type=72):
    """Ask the robot to reach a specific pose using a specific movement type, return the pose that the robot actually reached. This function is only used when the PC2KUKA program is running on the robot, which can read and execute this order."""
    send_3964R_single_char(movement_type)         # send GO signal
    send_3964R_single_double(pose.x)              # send the 6 double values the robot is waiting for
    send_3964R_single_double(pose.y)
    send_3964R_single_double(pose.z)
    send_3964R_single_double(pose.a)
    send_3964R_single_double(pose.b)
    send_3964R_single_double(pose.c)
    recv = read_3964R_data_buffer()
    while recv[0] != DONE:                        # wait DONE signal
        recv = read_3964R_data_buffer()
    return read_3964R_pose()                      # read and return pose

def move_to_pose(pose, movement_type=72):
    """Ask the robot to reach a specific pose using a specific movement type, return the pose that the robot actually reached. This function is only used when the PC2KUKA program is running on the robot, which can read and execute this order."""
    send_3964R_single_char(movement_type)         # send GO signal
    send_3964R_single_double(pose.x)              # send the 6 double values the robot is waiting for
    send_3964R_single_double(pose.y)
    send_3964R_single_double(pose.z)
    send_3964R_single_double(pose.a)
    send_3964R_single_double(pose.b)
    send_3964R_single_double(pose.c)
    recv = read_3964R_data_buffer()
    while recv[0] != DONE:                        # wait DONE signal
        recv = read_3964R_data_buffer()
    return read_3964R_pose()                      # read and return pose

def move_lin_to_pose(pose, movement_type=74):
    """Ask the robot to reach a specific pose using a linear movement type, return the pose that the robot actually reached. This function is only used when the PC2KUKA program is running on the robot, which can read and execute this order."""
    send_3964R_single_char(movement_type)         # send LIN signal
    send_3964R_single_double(pose.x)              # send the 6 double values the robot is waiting for
    send_3964R_single_double(pose.y)
    send_3964R_single_double(pose.z)
    send_3964R_single_double(pose.a)
    send_3964R_single_double(pose.b)
    send_3964R_single_double(pose.c)
    recv = read_3964R_data_buffer()
    while recv[0] != DONE:                        # wait DONE signal
        recv = read_3964R_data_buffer()
    return read_3964R_pose()                      # read and return pose

def move_linRel(dx=0.0,dy=0.0,dz=0.0,da=0.0,db=0.0,dc=0.0,movement_type=73):
    """Ask the robot to reach a specific pose using a specific movement type, return the pose that the robot actually reached. This function is only used when the PC2KUKA program is running on the robot, which can read and execute this order."""
    send_3964R_single_char(movement_type)         # send GO signal
    send_3964R_single_double(dx)              # send the 6 double values the robot is waiting for
    send_3964R_single_double(dy)
    send_3964R_single_double(dz)
    send_3964R_single_double(da)
    send_3964R_single_double(db)
    send_3964R_single_double(dc)
    recv = read_3964R_data_buffer()
    while recv[0] != DONE:                        # wait DONE signal
        recv = read_3964R_data_buffer()
    return read_3964R_pose()                      # read and return pose
def get_pose():
    """Ask the robot to send back its pose, return the pose. This function is only used when the PC2KUKA program is running on the robot, which can read and execute this order."""
    send_3964R_single_char(POS)                   # send POS signal
    return read_3964R_pose()                      # read and return pose

def get_poses():
    bPose = get_pose()
    # il faut transformer le tableau d'octets recus en chaine : 
    szPose = str(format(bPose))
    # on peut passer la chaine la fonction de decodage qui retourne une
    # liste (ici rPos) au format [x,y,z,a,b,c] : 
    rPos = decodePos(szPose)
    print(format(rPos))
    return format(rPos)


def close_tool(movement_type=76):
    try:
        print("close..............")
        send_3964R_single_char(movement_type) 
        recv = read_3964R_data_buffer()
        szRecv = str(format(recv))
        print("close : recu = " + szRecv)
        
        while recv[0] != DONE:                        # wait DONE signal
            print("calling read_3964R_data_buffer()")
            recv = read_3964R_data_buffer()
            print("OK")
            szRecv = str(format(recv))
            print("close : recu = " + szRecv)
        #return read_3964R_pose()  
    except:
        print() 

def open_tool(movement_type=77):
    try:
        print("open..............")
        send_3964R_single_char(movement_type) 
        recv = read_3964R_data_buffer()
        szRecv = str(format(recv))
        print("open : recu = " + szRecv)
        while recv[0] != DONE:                        # wait DONE signal
             print("calling read_3964R_data_buffer()")
             recv = read_3964R_data_buffer()
             print("OK")
             szRecv = str(format(recv))
             print("open : recu = " + szRecv)
        #return read_3964R_pose()  
    except:
        print()

def initialize(port):
    global s
    s = serial.Serial(port=port, baudrate=9600, bytesize=8, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE) # TODO s=serial.Serial() et créer une fonction initilize(port)

def finalize():
    s.close()



#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# fonction de decodage de la trame position
# IN : 
#       szIN : chaine de recherche, issue de getPos()
#       cKey : 'X','Y','Z','A','B','C' suivant ce qui
#              est recherche. 
#---------------------------------------------------
# Jacques BOONAERT-LEPERS 01/03/24
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def decodeOneCoordinate( szIn, cKey):
    szResult=[]
    i=0
    iMax = len(szIn)
    # on recherche le caractere correspondant a la coordonnee
    while (szIn[i] != cKey) and (i < iMax):
        i+=1
    # on a quitte la boucle precedente parce qu'on a trouve le caractere : 
    if i < iMax:
        if cKey != 'C':
            # on cherche maintenant le caractere ';' : 
            j = 0
            while( szIn[i+j] != ';') and ((i+j) < iMax):
                j+=1
            # on a trouve ';' : 
            if( (i+j) < iMax ):
                szResult = szIn[(i+4):(i+j)]
                return szResult
            # souci de format :
            else :
                return []
        else:
            # on s'arrete a la fin de la ligne
            szResult = szIn[(i+4):iMax]
            return szResult
    # on n'a pas trouve le caractere correspondant a la coordonnee dans la ligne
    else:
        return []
#____________________________________________________________________________
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# decode de la trame de position renvoyee par le robot
# IN 
#       szIn  : trame de position retournee par getPos()
# OUT
#       [x,y,z,a,b,c] : coordonnees cartesiennes et orientation 
#---------------------------------------------------------------
# Jacques BOONAERT-LEPERS   01/03/24
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def decodePos( szIn ):
    szX = decodeOneCoordinate( szIn, 'X')
    szY = decodeOneCoordinate( szIn, 'Y')
    szZ = decodeOneCoordinate( szIn, 'Z')
    szA = decodeOneCoordinate( szIn, 'A')
    szB = decodeOneCoordinate( szIn, 'B')
    szC = decodeOneCoordinate( szIn, 'C')
    if (szX == []) or (szY == []) or (szZ == []) or (szA == []) or (szB == []) or (szC == []):
        return None
    else:
        x = eval(szX)
        y = eval(szY)
        z = eval(szZ)
        a = eval(szA)
        b = eval(szB)
        c = eval(szC)
        return [x,y,z,a,b,c]
#____________________________________________________________________________________________