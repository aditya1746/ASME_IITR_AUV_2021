#! /usr/bin/env python

# ============ Importing necessary libraries ===============

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from std_msgs.msg import String
from sauvc_qualification.msg import distance_and_center

# ============= defining callback function for reading the image published on camera_input topic ====================

def callback(msgs):

    # ============== reading the image from camera_input topic =================

    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(msgs, desired_encoding="passthrough")

    #cv2.imshow('frame_sub', img)
    #cv2.waitKey(5000)
    #cv2.destroyAllWindows()

    # =============== processing the image  ===================================



    # ============== publishing the necessary data on gate_pos topic ===========

    pub = rospy.Publisher('gate_pos',distance_and_center,queue_size=10)

    msg_dist = distance_and_center()

    if(depth_reached=="no"):
        
        msg_dist.distance = -100
        msg_dist.centerx = -100
        msg_dist.centery = -100

    else:

        msg_dist.distance = 20
        msg_dist.centerx = 30
        msg_dist.centery = 10

    pub.publish(msg_dist)


# ==================== Naming the node ========================

rospy.init_node('detecting_gate') 

# ==================== calling the callback function to read the image published on camera_input topic ==============

sub = rospy.Subscriber('camera_input', Image, callback)

sub_depth = rospy.Subscriber('depth',String, callback_depth)

rospy.spin()
