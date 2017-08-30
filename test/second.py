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
print "Battery " + str(drone.getBattery()[0]) + " " + str(drone.getBattery()[1])
if drone.getBattery()[1]== "empty" : sys.exit()
drone.useDemoMode(True)
drone.getNDpackage(["demo"])
time.sleep(0.5)
#15 basic datasets per second (default)
#Packets, which shall be decoded
#Give it some time to fully awake
drone.takeoff()
#Fly, drone, fly !
while drone.NavData["demo"][0][2]: time.sleep(0.1) #Still in landed-mode?
##### Mainprogram #####
print "Drone is flying now, land it with any key but <space>"
gliding = False
print "Drone is holding its position, toggle to glide with <space>-key."
end = False
while not end:
    key = drone.getKey()
    #Get a pressed key
    if key == " ":
        if gliding:
            gliding = False
            drone.stop()
            #Stop and hold position
            print "Drone is holding its position"
        else:
            gliding = True
            drone.moveForward(0)
            #Do not fly actively in any direction
            print "Drone is gliding"
    elif key: end = True
    #End this loop
    else: time.sleep(0.1)
    #Wait until next looping
