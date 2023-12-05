#! /usr/bin/env python
import rospy
import sys
import copy
import moveit_msgs.msg
import geometry_msgs.msg
import moveit_commander
from std_msgs.msg import Empty
import math
import actionlib
from geometry_msgs.msg import Pose


import tf2_ros
import tf2_geometry_msgs

rospy.init_node('test')

tf_buffer = tf2_ros.Buffer(rospy.Duration(100.0))  # tf buffer length
tf_listener = tf2_ros.TransformListener(tf_buffer)


moveit_commander.roscpp_initialize(sys.argv)
robot=moveit_commander.RobotCommander()
scene=moveit_commander.PlanningSceneInterface()
group=moveit_commander.MoveGroupCommander('arm')
display_trajectory_publisher=rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory)

print("== go to home ==")
target_values= group.get_named_target_values("home")
group.go(target_values, wait = True)

print("== go to left ==")
target_values= group.get_named_target_values("left")
group.go(target_values, wait = True)

print("== move down, 50 mm ==")

pose=group.get_current_pose()
posetarget = pose
posetarget.pose.position.z-=0.05
group.set_pose_target(posetarget)
plan=group.plan()
group.go(wait=True)


print("== go to test IK ==")
transform = tf_buffer.lookup_transform('world', 'ik_testpoint', rospy.Time())

destination_pose = Pose()
destination_pose.position = transform.transform.translation
destination_pose.orientation = transform.transform.rotation

group.set_pose_target(destination_pose)
plan=group.plan()
group.go(wait=True)

print("== go to right ==")
target_values= group.get_named_target_values("right")
group.go(target_values, wait = True)

print("== go to home ==")
target_values= group.get_named_target_values("home")
group.go(target_values, wait = True)

print("== go to resting ==")
target_values= group.get_named_target_values("resting")
group.go(target_values, wait = True)




print("== ready ==")

