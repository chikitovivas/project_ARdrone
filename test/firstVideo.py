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
drone.useDemoMode(True)
#15 basic datasets per second
drone.getNDpackage(["demo","vision_detect"]) #Packets to decoded
time.sleep(0.5)
#Gives time to fully awake
##### Mainprogram #####
CDC = drone.ConfigDataCount
drone.setConfigAllID() #Go to multiconfiguration-mode
drone.sdVideo() #Choose lower resolution
drone.groundCam() #Choose ground view
#drone.frontCam() #Choose front view
while CDC==drone.ConfigDataCount: time.sleep(0.001) #Wait until it is done
drone.startVideo() #Start video-function
drone.showVideo() #Display the video
print"<space> to toggle front- and groundcamera, any other key to stop"
IMC = drone.VideoImageCount #Number of encoded videoframes
stop = False
ground = False #To toggle front- and groundcamera
#drone.groundVideo(True)
while not stop:
    while drone.VideoImageCount==IMC: time.sleep(0.01) #Wait for next image
    IMC = drone.VideoImageCount #Number of encoded videoframes
    key = drone.getKey()
    print "esperando key.."
    print "Key presionada:" + key + "--"
    if key == "g":
        if ground:
            ground = False
            drone.frontCam()
        else:
            ground = True
            drone.groundCam()
    elif key: stop = True
print("chao")
