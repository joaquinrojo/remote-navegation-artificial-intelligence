import time
from RobotController import RobotController

hostDef = "192.168.4.1"
portDef = "100"
contentDef = '{"N":102,"D1":1,"D2":44}'
simulacion=0
objRobot=RobotController(hostDef,portDef,simulacion)
intensity=44
objRobot.action("L",intensity,1)
time.sleep(0.5)
objRobot.hearthBeat()
time.sleep(0.5)
objRobot.hearthBeat()
time.sleep(0.5)
objRobot.hearthBeat()
time.sleep(0.5)
