import sys

from numpy import ndarray

sys.path.append("..\src")

import cv2
from junduo_gripper.src.interface import JunDuoGripper

# 伪代码，实例化睿尔曼机械臂对象
arm = Arm()

# 实例化钧舵夹爪
junduo_gripper = JunDuoGripper(arm)

# 打开夹爪
junduo_gripper.gripper_open()

# 关闭夹爪
junduo_gripper.gripper_close()
