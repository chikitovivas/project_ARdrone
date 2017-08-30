#########
# useVideo.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows the usage of the video-function of a Parrot AR.Drone 2.0 using the PS-Drone-API.
# The drone will stay on the ground.
# Dependencies: a POSIX OS, openCV2, PS-Drone-API 2.0 beta or higher.
# (w) J. Philipp de Graaff, www.playsheep.de, 2016
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

##### Suggested clean drone startup sequence #####
import time, sys
sys.path.append('/home/chikitovivas/Descargas/Python-control-dron')
import ps_drone													# Import PS-Drone-API
import cv2
import numpy
from matplotlib import pyplot as plt														# Import OpenCV

drone = ps_drone.Drone()										# Start using drone
drone.startup()													# Connects to drone and starts subprocesses
kernel = numpy.ones((5,5),numpy.uint8)
drone.reset()													# Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0]==-1):	time.sleep(0.1)				# Waits until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])	# Gives a battery-status
drone.useDemoMode(True)											# Just give me 15 basic dataset per second (is default anyway)

##### Mainprogram begin #####
drone.setConfigAllID()				# Go to multiconfiguration-mode
drone.sdVideo()						# Choose lower resolution (hdVideo() for...well, guess it)
drone.frontCam()					# Choose front view
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:	time.sleep(0.0001)	# Wait until it is done (after resync is done)
drone.startVideo()					# Start video-function

##### And action !
IMC = 	 drone.VideoImageCount		# Number of encoded videoframes
stop =	 False
while not stop:
	while drone.VideoImageCount==IMC: time.sleep(0.01)	# Wait until the next video-frame
	IMC = drone.VideoImageCount
	key = drone.getKey()
	if key:		stop = True
	img  = drone.VideoImage					# Copy video-image
	"""pImg = cv2.resize(img,(700,400))		# Process video-image
	while(True):
	    #ret,frame = img
	    rangomax = numpy.array([50,255,50])
	    rangomin = numpy.array([0,51,0])
	    mascara = cv2.inRange(pImg,rangomin,rangomax)
	    opening = cv2.morphologyEx(mascara,cv2.MORPH_OPEN,kernel)
	cv2.imshow('ventana2',opening)
	x,y,w,h = cv2.boundingRect(opening)
	cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
	cv2.circle(frame,(x+w/2,y+h/2),5,(0,0,255),-1)
	cv2.imshow('ventana',frame)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
	    break"""

	#pImg = cv2.resize(img,(700,400))		# Process video-image
	##END##
	#cv2.imshow('Drones video',pImg)			# Show processed video-image
	#cv2.waitKey(1)							# OpenCV for Linux has a bug and needs this line
