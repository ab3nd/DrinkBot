#!/usr/bin/python

# Controls the 5 liquid dispensing pumps on the drinkbot 
# Subscribes to face tracker to detect faces, and object detector to 
# determine which soda the person wants

# From attention_tracker
# /actual_focus_of_attention
# /attention_tracker/faces/image
# /attention_tracker/faces/image/compressed
# /attention_tracker/faces/image/compressed/parameter_descriptions
# /attention_tracker/faces/image/compressed/parameter_updates
# /attention_tracker/faces/image/compressedDepth
# /attention_tracker/faces/image/compressedDepth/parameter_descriptions
# /attention_tracker/faces/image/compressedDepth/parameter_updates
# /attention_tracker/faces/image/theora
# /attention_tracker/faces/image/theora/parameter_descriptions
# /attention_tracker/faces/image/theora/parameter_updates

# From gscam
# /camera/camera_info
# /camera/image_raw
# /camera/image_raw/compressed
# /camera/image_raw/compressed/parameter_descriptions
# /camera/image_raw/compressed/parameter_updates
# /camera/image_raw/compressedDepth
# /camera/image_raw/compressedDepth/parameter_descriptions
# /camera/image_raw/compressedDepth/parameter_updates
# /camera/image_raw/theora
# /camera/image_raw/theora/parameter_descriptions
# /camera/image_raw/theora/parameter_updates
# /estimate_focus
# /face_0_field_of_view
# /nb_detected_faces
# /objects
# /objectsStamped
# /rosout
# /rosout_agg
# /tf
# /tf_static

from pyfirmata import Arduino, util
import rospy
from sensor_msgs.msg import Range
from std_msgs.msg import Float32MultiArray
from find_object_2d.msg import ObjectsStamped
from visualization_msgs.msg import Marker

#Indexed by pump number, which is written on the pump
pinMap = [8, 9, 5, 4, 6]

#Object numbers to names
#Use GFTT detector, ORB descriptor
detector_from_soda = {"dr_pepper":[69, 70, 71, 72],
					  "monster":[76,77,79,80,81],
					  "sunkist":[82,83,84],
					  "sprite":[85, 86, 87, 88, 89],
					  "coke":[90, 91, 92, 93, 94, 95, 96, 97, 98, 99]}

#Turns the above map inside out, to map image IDs to soda names. 
#Look, it just does, OK, relax and go with it. 
soda_from_detector =  {imgId:key for key in soda_from_detector for imgId in soda_from_detector[key]}

# Make sure you set the pumps up like this
pump_from_soda = {"dr_pepper":0, 
                  "monster":1, 
                  "sunkist":2,
                  "sprite":3,
                  "coke":4}

class DrinkDriver:
	def __init__(self):
		#self.board = Arduino('/dev/ttyUSB0')
		
		#Keep a list of the soda cans the robot can see
		self.visibleCans = []
		self.lastSawCans = None
		#Set to the time if a user is looking at the robot
		self.lastLookedAt = None
		#Set to true if robot is serving a drink
		self.isServing = False

		self.fovSub = rospy.Subscriber("/estimate_focus", Marker, self.getFoV)
		self.canIDSub = rospy.Subscriber("/objects", Float32MultiArray, self.getCanIDs)

		print "init ended"

	def pumpDrink(self, pumpNumber, duration):
		#If robot has been looked at in the last 5 seconds
		if (rospy.Time.now() - self.lastLookedAt) < rospy.Duration(5, 0):
			#And if there has been a soda seen 
			if len(self.visibleCans) > 0:
				print "***SAW BOTH!***"
				#Get the last seen soda
				# 46-48 Dr Pepper

				#Translate that to a pump number

				#Translate that to a pin number

				#Turn the pin high

				#Delay for a while

				#Turn pin low

				#Clear the timers		
				pass

	def getFoV(self, message):
		self.lastLookedAt = message.header.stamp
		print "."
		
	def getCanIDs(self, message):
		#Throw away everything except the IDs
		self.visibleCans = message.data[0::11]
		self.lastSawCans = rospy.Time.now()
		if len(self.visibleCans) > 0:
			print self.visibleCans
			self.pumpDrink

if __name__ == "__main__":
	dd = DrinkDriver()
	rospy.init_node("dispenser_control")
	rospy.spin()
	
