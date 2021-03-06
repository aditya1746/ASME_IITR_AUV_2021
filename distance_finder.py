#! /usr/bin/env python

# ============ Importing necessary libraries ===============

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from std_msgs.msg import String
from sauvc_qualification.msg import distance_and_center

def nothing(x):
	pass

def findDistanceFromArea(ar):
	# will be define once we have actual hardware

# ============= defining callback function for reading the image published on camera_input topic ====================

def callback(msgs):

    # ============== reading the image from camera_input topic =================

    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(msgs, desired_encoding="passthrough")
	
	frame_cx,frame_cy,ch = img.shpae
	
	frame_cx = frame_cx/2
	frame_cy = frame_cy/2

    #cv2.imshow('frame_sub', img)
    #cv2.waitKey(5000)
    #cv2.destroyAllWindows()

    # =============== processing the image  ===================================

    #image=cv2.imread("test.jpeg")
    image = img
	b, g, r = cv2.split(image)

#while(1):

	b1 = b-135
	g1 = g-144
	r1 = r + 164

	image= cv2.merge((b1,g1,r1))
	
	gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	image=cv2.GaussianBlur(image,(5,5),0)
	edged=cv2.Canny(image,50,250,apertureSize=3)
	temp = cv2.dilate(edged, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

	cnts,_ = cv2.findContours(temp,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	
	area = -1

	if(len(cnts)>0):

		areas = [cv2.contourArea(c) for c in cnts]
		max_index = np.argmax(areas)
		cnt=cnts[max_index]
		rect = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(rect) # cv2.boxPoints(rect) for OpenCV 3.x
		box = np.int0(box)
		area = cv2.contourArea(cnt)
		print(area)
		M = cv.moments(cnt)
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		cv2.drawContours(image,[box],0,(0,0,255),1)

	cv2.imshow("final",edged)
	cv2.imshow("image", image)
	if cv2.waitKey(30) & 0xFF == 27:
		break

	cv2.waitKey(0)

	cv2.destroyAllWindows()


    # ============== publishing the necessary data on gate_pos topic ===========

    pub = rospy.Publisher('gate_pos',distance_and_center,queue_size=10)

    msg_dist = distance_and_center()

    msg_distance.distance = findDistanceFromArea(area)
	msg_distance.centerx = frame_cx - cx
	msg_distance.centery = framecy - cy

    pub.publish(msg_dist)


# ==================== Naming the node ========================

rospy.init_node('detecting_gate') 

# ==================== calling the callback function to read the image published on camera_input topic ==============

sub = rospy.Subscriber('camera_input', Image, callback)

sub_depth = rospy.Subscriber('depth',String, callback_depth)

rospy.spin()
