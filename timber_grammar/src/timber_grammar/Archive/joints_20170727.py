import math

import compas
from compas.geometry import Box

class joint(object):
    """
    joint class containing varied joints
    """
    def __init__(self, frame, depth, width, height):

        """
        :param fame:      plane of boolean geometry
        :param depth:   depth of boolean geometry
        :param width:     width of boolean geometry
        :param height:     height of boolean geometry
        """
        self.frame = frame
        self.depth = depth
        self.width = width 
        self.height = height
        self.update_joint() #method
        self.joints = []

    def update_joint(self):
        return self.joint_90lap()

    def joint_90lap(self):
        bool_joint = Box(self.frame, self.depth, self.width, self.height)
        return bool_joint 

#======================================
#Input geometry for test
#======================================

#recreate face just as in created geometry
#

#test = joints(100,face_id,50, 100)
        




