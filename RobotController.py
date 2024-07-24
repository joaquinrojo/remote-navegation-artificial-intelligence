import socket
import time


class RobotController:

    # Numero total de estrellas
    socketConnection = 0
    lastAction=""


    def __init__(self,host,port,simulacion):
        print("inicio constructor")
        self.simulacion = simulacion
        if self.simulacion == 0:
            self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketConnection.connect((host, int(port)))
            #self.socketConnection.settimeout(100)
        print("termino constructor")

    def hearthBeat(self):
        s="{Heartbeat}"
        print(s)
        if self.simulacion == 0:
            self.socketConnection.sendall(s.encode())

    def action(self, actionCode, intesity,duration):
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
        # Forward, // (1)
        # Backward, // (2)
        # Left, // (3)
        # Right, // (4)
        # LeftForward, // (5)
        # LeftBackward, // (6)
        # RightForward, // (7)
        # RightBackward, // (8)
        # stop_it // (9)

        if(actionCode!=self.lastAction):
        #if (1):
            #print(self.lastAction,actionCode)

            self.lastAction=actionCode
            contentDef = '{"N":102,"D1":'+str(numCode)+',"D2":'+str(intesity)+'}'
            contentStop = '{"N":102,"D1":9,"D2":' + str(intesity) + '}'
            print(actionCode,contentDef)
            if self.simulacion == 0:
                self.socketConnection.sendall(contentDef.encode())
                #time.sleep(0.5)
                #self.socketConnection.sendall(contentStop.encode())


            for x in range(0, duration):
                pass
                #time.sleep(1)
                #self.hearthBeat()
            # s.shutdown(socket.SHUT_WR)

            #while True:
            #    data = self.socketConnection.recv(4096)
            #    if not data:
            #        break
            #    print(repr(data))

            #self.socketConnection.shutdown(socket.SHUT_WR)
        else:
            pass


