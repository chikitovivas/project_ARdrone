##### Suggested clean drone startup sequence #####
import time, sys
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron')
import ps_drone                                    # Import PS-Drone-API

drone = ps_drone.Drone()                           # Start using drone
drone.startup()                                    # Connects to drone and starts subprocesses

drone.reset()                                      # Sets drone's status to good
while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1]) # Battery-status
drone.useDemoMode(True)                            # Set 15 basic dataset/sec
drone.getNDpackage(["demo","vision_detect"])       # Packets, which shall be decoded
time.sleep(0.5)                                    # Give it some time to awake fully
drone.startVideo()                                          # Empezar la funcion de video
drone.showVideo()
##### Mainprogram begin #####
# Setting up detection...
# Shell=1|Roundel=2|BlackRoundel=4|Stripe=8|Cap=16|ShellV2=32|TowerSide=64|OrientedRoundel=128
#drone.setConfig("detect:detect_type","10")            # Enable detection in universal mode
drone.setConfig("detect:detections_select_h","130") # Detect "Oriented Roundel" in front
#drone.setConfig("detect:detections_select_v","0")   # No detection on ground cam
CDC = drone.ConfigDataCount
while CDC==drone.ConfigDataCount: time.sleep(0.001) # Wait until it is done (resync is done)

# Get detections
stop = False
while not stop:
    NDC = drone.NavDataCount
    while NDC == drone.NavDataCount:  time.sleep(0.01)
    if drone.getKey():              stop = True
    tagNum = drone.NavData["vision_detect"][0]      # Number of found tags
    tagX = drone.NavData["vision_detect"][2]        # Horizontal position(s)
    tagY = drone.NavData["vision_detect"][3]        # Vertical position(s)
    tagZ = drone.NavData["vision_detect"][6]        # Distance(s)
    tagRot = drone.NavData["vision_detect"][7]      # Orientation(s)

# Show detections
    print(str(drone.NavData["vision_detect"]))
    #if tagNum:
    #    for i in range (0,tagNum):
    #        print "Tag no "+str(i)+" : X= "+str(tagX[i])+" Y= "+str(tagY[i])\
    #                              +" Dist= "+str(tagZ[i])+" Orientation= "+str(tagRot[i])
    #else:   print "No tag detected"
