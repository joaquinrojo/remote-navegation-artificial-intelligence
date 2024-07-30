import socket
import time


class RobotController:

    # Numero total de estrellas
    socketConnection = 0
    lastAction=""

    def __init__(self,host,port,simulacion):
        self.simulacion = simulacion
        if self.simulacion == 0:
            self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketConnection.connect((host, int(port)))


    def hearthBeat(self):
        s="{Heartbeat}"
        print(s)
        if self.simulacion == 0:
            self.socketConnection.sendall(s.encode())

    def action(self, actionCode, intesity,duration):

        # Forward, // (1)
        # Backward, // (2)
        # Left, // (3)
        # Right, // (4)
        # LeftForward, // (5)
        # LeftBackward, // (6)
        # RightForward, // (7)
        # RightBackward, // (8)
        # stop_it // (9)

        numCode=0
        if(actionCode=="S"):
            numCode=9
        if(actionCode=="L"):
            numCode=3
        if(actionCode=="R"):
            numCode=4
        if(actionCode=="U"):
            numCode=1
        if(actionCode=="D"):
            numCode=2


        if(actionCode!=self.lastAction):
            self.lastAction=actionCode
            contentDef = '{"N":102,"D1":'+str(numCode)+',"D2":'+str(intesity)+'}'
            print(contentDef)
            if self.simulacion == 0:
                self.socketConnection.sendall(contentDef.encode())
                self.hearthBeat()
                time.sleep(duration)

        else:
            pass


