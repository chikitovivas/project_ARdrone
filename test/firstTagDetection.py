##### Suggested clean drone startup sequence #####
import time, sys
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron')
#Imports the PS-Drone-API
import ps_drone
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
#Setting up detection...
drone.setConfig("detect:detect_type", "3")
#Universal detection
drone.setConfig("detect:detections_select_h", "128") #Front: Oriented Roundel
drone.setConfig("detect:detections_select_v", "0") #Ground: None
CDC = drone.ConfigDataCount
while CDC==drone.ConfigDataCount: time.sleep(0.001) #Wait until it is done
#Get detections
end = False
while not end:
    while drone.NavDataCount==CDC: time.sleep(0.001) #Wait for NavData
    if drone.getKey():    end = True
    tagNum = drone.NavData["vision_detect"][0]
    #No of found tags
    tagX = drone.NavData["vision_detect"][2]
    #Horizontal position(s)
    tagY = drone.NavData["vision_detect"][3]
    #Vertical position(s)
    tagZ = drone.NavData["vision_detect"][6]
    #Distance(s)
    #Orientation(s)
    tagRot = drone.NavData["vision_detect"][7]
#Show detections
    if tagNum:
        for i in range (0,tagNum):
                print "Tag no" +str(i)+ ": X="+str(tagX[i])+ "Y="+str(tagY[i])\
                + "Dist=" +str(tagZ[i])+ "Orientation=" +str(tagRot[i])
    else: print "No tag detected"
