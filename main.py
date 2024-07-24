import cv2
from process.main import FrameProcessing
from RobotController import RobotController
hostDef = "192.168.4.1"
portDef = "100"
intensity = 40
import datetime
import time
from datetime import datetime
simulacion=0


frame_processing = FrameProcessing()

if simulacion==1:
    cap = cv2.VideoCapture(0)
else:
    URL = "http://192.168.4.1"
    cap = cv2.VideoCapture(URL + ":81/stream")


cap.set(3, 1280)
cap.set(4, 720)
milisegundosDesdeUltimoPalpito=datetime.now()



if __name__ == "__main__":
    objRobot = RobotController(hostDef, portDef, simulacion)
    objRobot.hearthBeat()
    contFramesProcesados=0
    while True:
        ret, frame = cap.read()
        #time.sleep(0.3)
        #print(contFramesProcesados)
        if contFramesProcesados%10==0: #solo pares
            contFramesProcesados=0
            t1=milisegundosDesdeUltimoPalpito
            t2 = datetime.now()
            delta = t2 - t1
            if(delta.total_seconds()>0.85):
                #objRobot.action("S", intensity, 1)
                objRobot.hearthBeat()
                milisegundosDesdeUltimoPalpito = datetime.now()
            #print(f"Time difference is {delta.total_seconds()} seconds")

            #timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            #print(ts)

            frame = cv2.resize(frame, (1280, 720))
            frame = cv2.flip(frame, 1)

            clase,vectorError = frame_processing.process(frame)
            distanciaRequiereMovimiento=0

            errorX=vectorError[0]

            cercaniaActual = abs(vectorError[1])
            print(errorX,cercaniaActual)
            if(abs(errorX)>120):
                distanciaRequiereMovimiento=1



            if distanciaRequiereMovimiento==0:
                #hacer una pulso para que no se apague el motor

                maxCercania=550000
                minCercania=300000
                #para valores mas lejanos el errorY es menor

                if(cercaniaActual>maxCercania): #si está muy cerca, debe alejarse
                    objRobot.action("D", intensity, 1);

                if (cercaniaActual < minCercania and cercaniaActual>0):  # si está muy lejos
                    objRobot.action("U", intensity, 1);

                if (cercaniaActual==0 or (cercaniaActual<=maxCercania and  cercaniaActual >= minCercania)):  # si está en rango permitido
                    objRobot.action("S",intensity,1)


            else:

                if errorX < 0:
                    #debe girar a la derecha
                    objRobot.action("L",intensity,1)
                    #objRobot.hearthBeat()
                if errorX > 0:
                    # debe girar a la izquierda
                    objRobot.action("R",intensity,1)




            cv2.imshow('object tracking robot', frame)
            t = cv2.waitKey(5)
            if t == 27:
                break
        contFramesProcesados = contFramesProcesados + 1;
    cap.release()
    cv2.destroyAllWindows()
