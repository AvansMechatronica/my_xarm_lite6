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

rospy.init_node('test')

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

