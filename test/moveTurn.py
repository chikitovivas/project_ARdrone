##### Suggested clean drone startup sequence #####
import time, sys
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron')
import ps_drone
#Imports the PS-Drone-API
drone = ps_drone.Drone()
drone.startup()
#Initials the PS-Drone-API

#Connects to the drone and starts subprocesses
drone.reset()
#Sets drones LEDs to green when red
while (drone.getBattery()[0]==-1): time.sleep(0.1)
#Reset completed ?
print "Battery:" + str(drone.getBattery()[0]) + "%" + str(drone.getBattery()[1])
if drone.getBattery()[1]== "empty" : sys.exit()
drone.useDemoMode(True)#15 basic datasets per second (default)
drone.getNDpackage([ "demo" ])#Packets, which shall be decoded
time.sleep(0.5)#Give it some time to fully awake
drone.trim()#Recalibrate sensors
drone.getSelfRotation(5)#Auto-alteration-value of gyroscope-sensor
print  "Auto-alternation:" + str(drone.selfRotation) + "deg/sec"
drone.takeoff()
while drone.NavData[ "demo" ][0][2]: time.sleep(0.1)

##### Mainprogram #####
print "Drone is flying now"
leftRight = -0.02 #Move with 2% speed to the left

backwardForward = -0.1 #Move with 10% speed backwards

downUp = 0.3 #Move with 30% speed upward

turnLeftRight = 1 #Turn full speed right

drone.move(leftRight, backwardForward, downUp, turnLeftRight) #Do movement
timeToFlight = 1 #Time to move at all

refTime = time.time() #Start-time
end = False
while not end:
    if drone.getKey(): end = True
    if time.time()-refTime>=timeToFlight: end = True
print "Drone stopped movement"
drone.stop()
time.sleep(2)
print "Drone turns 120 degree to the left"
drone.turnAngle(-120,1,1) #Turn 120 to the left, full speed, 1 accuracy
