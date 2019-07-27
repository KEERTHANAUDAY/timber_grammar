import math
import compas
from compas.geometry import Box
from compas.datastructures import Mesh

class Beam(object):
    """ Beam class containing its size and connecting dowels
    """

    def __init__(self, frame, depth, width, height):
        """ initialization

            :frame:           base plane for the beam 
            :depth:           the length along the local x-axis
            :width:           the length along the local z-axis
            :height:          the length along the local y-axis  
            
        """
        self.frame = frame
        self.depth = depth 
        self.width = width
        self.height = height 
        self.beam_mesh = None
        self.draw_uncut_mesh()

    def update_mesh(self):
        pass
     
    def draw_uncut_mesh(self):
        box = Box(self.frame, self.depth,self.width,self.height)
        box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces) 
        self.beam_mesh = box_mesh
        