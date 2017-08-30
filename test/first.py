import time
import sys
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron')
import ps_drone #Imports the PS-Drone-API


drone = ps_drone.Drone()

drone.startup() #Initials the PS-Drone-API
#Connects to the drone and starts subprocesses

drone.takeoff()
time.sleep(7.5) #Drone starts
#Gives the drone time to start
drone.moveForward()
time.sleep(1)
drone.stop()
time.sleep(2) #Drone flies forward...
#... for two seconds
#Drone stops...
#... needs, like a car, time to stop
drone.moveBackward(0.25)
time.sleep(1)
drone.stop()
time.sleep(2) #Drone flies backward with a quarter speed...
#... for one and a half seconds
#Drone stops
drone.setSpeed(1.0)
print drone.setSpeed() #Sets default moving speed to 1.0 (=100%)
#Shows the default moving speed
drone.turnLeft()
time.sleep(2)
drone.stop()
time.sleep(2) #Drone moves full speed to the left...
#... for two seconds
#Drone stops
drone.land() #Drone lands
