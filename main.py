import cv2
from process.main import FrameProcessing
from RobotController import RobotController
from robot_controller.src.main import PIDControl

hostDef = "192.168.4.1"
portDef = "100"
intensity = 40

from datetime import datetime
simulation=1 #1  works with webcam (solo con webcam), 0 works with robot camera (funciona con robot)


frame_processing = FrameProcessing()
pid = PIDControl()
if simulation==1:
    cap = cv2.VideoCapture(0)
else:
    URL = "http://"+hostDef
    cap = cv2.VideoCapture(URL + ":81/stream")

lastHearthBeat = datetime.now()
minSecondsBeforeHearthBeat=0.7
maxCloseness = 550000 #maximo de cercanía, mientras mayor mas cerca
minCloseness = 300000  #mínimo de cercanía, mientras mayor mas cerca
classForDetection = "person"
maxErrorX = 120  #maximo de error de forma horizontal

maxTimeTurningX = 0.9  # max time turning (tiempo maximo de giro)
allowedErrorinX = 50  # si el error en X está dentro de ese valor entonces está ok

maxTimeMovingInY = 0.5


resolutionInX = 1280
resolutionInY = 720

if __name__ == "__main__":
    objRobot = RobotController(hostDef, portDef, simulation)
    objRobot.hearthBeat()
    contFramesProcessed=0
    while True:
        ret, frame = cap.read()
        if contFramesProcessed%10==0: #just 1 of 10 frames are processed (solo 1 cada 10 frames son procesados)
            contFramesProcessed=0
            t1=lastHearthBeat
            t2 = datetime.now()
            delta = t2 - t1
            if(delta.total_seconds()>minSecondsBeforeHearthBeat): #hay que darle un pulso al robot y no se apague
                objRobot.hearthBeat()
                lastHearthBeat = datetime.now()

            frame = cv2.resize(frame, (resolutionInX, resolutionInY))
            frame = cv2.flip(frame, 1)

            clase,vectorError = frame_processing.process(frame,classForDetection)



            errorX=vectorError[0]
            errorY=vectorError[1]
            actualCloseness = abs(vectorError[1])  #cercanía actual en valor absoluto

            distanciaRequiereMovimiento=0
            if(abs(errorX)>maxErrorX):
                distanciaRequiereMovimiento=1

            if distanciaRequiereMovimiento==0:
                performMovement=0 #si realiza movimiento
                direccion=""
                if(actualCloseness>maxCloseness): #si está muy cerca, debe alejarse
                    performMovement=1
                    direccion="D" #ir hacia atrás

                if (actualCloseness < minCloseness and actualCloseness>0):  # si está muy lejos
                    performMovement=1
                    direccion="U" #ir hacia adelante

                if performMovement==1:
                    objRobot.action(direccion, intensity, maxTimeMovingInY);

                if (actualCloseness==0 or (actualCloseness<=maxCloseness and  actualCloseness >= minCloseness)):  # si está en rango permitido
                    objRobot.action("S",intensity,0) #stop


            else:
                control_x = pid.pid_control(errorX, 'x')
                # saco regla de 3 para calcular
                duracionMov = (maxTimeTurningX*abs(control_x))/allowedErrorinX;
                duracionMov = min(duracionMov, maxTimeTurningX)
                if errorX < 0:
                    #Turn right (debe girar a la derecha)
                    objRobot.action("L",intensity,duracionMov)
                if errorX > 0:
                    #Turn left (debe girar a la izquierda)
                    objRobot.action("R",intensity,duracionMov)

            cv2.imshow('object tracking robot (ESC to close)', frame)
            t = cv2.waitKey(5)
            if t == 27:
                break
        contFramesProcessed = contFramesProcessed + 1
    cap.release()
    cv2.destroyAllWindows()
