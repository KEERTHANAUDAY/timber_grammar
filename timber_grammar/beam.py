import math
import compas
import joints as j
from compas.geometry import Frame
from compas.datastructures import Mesh
from compas.geometry import subtract_vectors
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import Transformation
from compas.datastructures import mesh_transform
from compas_rhino import get_point_coordinates
from compas.geometry import Box
from compas.rpc import Proxy
import trimesh
from compas.rpc import Proxy
import trimesh

class Beam(object):
    """ Beam class containing its size and connecting dowels
    """

    def __init__(self, beam_mesh, face_id, dist):
        """ initialization

            :frame:  base plane where the beam is along with
            :length:          the length along the local x-axis (= the length of this beam)
            :width:          the length along the local y-axis
            :height:          the length along the local z-axis  
            :face_id:         key of the selected face through UI 
            :dist:            distance of joint position  
        """

        # self.frame = frame
        # self.length = length
        # self.width = width
        # self.height = height
        self.beam_mesh = beam_mesh
        self.face_id = face_id
        self.dist = dist 

        #self.mesh_geometry = mesh_geometry #output mesh
        self.update_mesh()
        self.joints = []
        
    def update_mesh(self):
        #return self.draw_uncut_mesh()
        return self.get_bool_pos()
        # for joint in joints:
        # mesh_for_subtraction = boolean_subtract(mesh_for_subtraction,joint.mesh_geometry)
        #self.mesh_geometry = uncut_mesh
        
    # def draw_uncut_mesh(self):
    #     box = Box(self.frame, self.length,self.height,self.width)
    #     self.beam_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces) 
    #     return self.beam_mesh

    def get_bool_pos(self):
        """
        gets the face_id 
            calls the attributes of the face 
            gets the vector and the normal of the face
        creats a frame on the input point position 
        translates the boolean geometry to the desired position
        """
        #get face attributes 
        vertices_id = self.beam_mesh.face_vertices(self.face_id)

        f_vertices = [] #vertices of the selected face
        for key in vertices_id:
            f_vertex = self.beam_mesh.vertex_coordinates(key)
            f_vertices.append(f_vertex)

        #vectors of face
        f_v1 = f_vertices[0]
        f_v2 = f_vertices[1]
        xaxis_vec = subtract_vectors(f_v1, f_v2)
        xaxis_viz = add_vectors(f_v1, scale_vector(xaxis_vec, 0.1)) #svisualizationcaled vectors for 

        f_c = self.beam_mesh.face_centroid(self.face_id)
        yaxis_vec = self.beam_mesh.face_normal(self.face_id)
        yaxis_viz = add_vectors(f_c, scale_vector(yaxis_vec,100)) #svisualizationcaled vectors for

        #frame at self.dist
        dist_point = get_point_coordinates(self.dist)
        f_frame = Frame(dist_point[0], xaxis_vec, yaxis_vec)

        #get join_90lap mesh
        joint_in = j.joint(Frame.worldXY, 100, 100, -50)
        joint = joint_in.update_joint()
        joint_mesh = Mesh.from_vertices_and_faces(joint.vertices, joint.faces)
        bool_frame = Frame([0, 0, 0], [1, 0, 0], [0, 0, 1]) #world frame values hard coded, needs to be fixed

        #Transformation
        T = Transformation.from_frame_to_frame(bool_frame,f_frame)
        self.joint_mesh_pos = mesh_transform(joint_mesh, T)

        #boolean 
        with Proxy('trimesh') as t:
            bool_beam = t.boolean_subtract(self.beam_mesh, joint_mesh_pos)
            

        return self.joint_mesh_pos 
        
        

    def boolean_subtract(self, T1, T2):
        with Proxy('trimesh') as t:
            self.bool_geo = t.boolean_subtract(T1, T2)
        return 


if __name__ == '__main__':

    # from compas.geometry import Box
    # from compas.datastructures import Mesh

    # box = Box(Frame.worldXY(),3000,100,100)
    # mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)
    # face_id = 1
    # pt = (0,0,0)

    # beam_in = Beam(mesh, face_id, pt)
    



    print("ok")