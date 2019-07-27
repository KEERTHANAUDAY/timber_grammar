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

class Beam(object):
    """ Beam class containing its size and connecting dowels
    """

    def __init__(self, frame, length, width, height, face_id, dist, new_beam_ht):
        """ initialization

            :frame:  base plane where the beam is along with
            :length:          the length along the local x-axis (= the length of this beam)
            :width:          the length along the local y-axis
            :height:          the length along the local z-axis  
            :face_id:         key of the selected face through UI 
            :dist:            distance of joint position 
            :new_beam_ht:     height of the new beam 
        """
        self.frame = frame
        self.length = length
        self.width = width
        self.height = height
        self.face_id = face_id
        self.dist = dist 
        self.new_beam_ht = new_beam_ht
        self.update_mesh()
        self.joint_mesh_pos = []
        self.booleaned_beam = []
        self.booleaned_newbeam = []
        self.joints = []
        
    def update_mesh(self):
        self.draw_uncut_mesh()
        self.get_bool_pos()
        # for joint in joints:
        # mesh_for_subtraction = boolean_subtract(mesh_for_subtraction,joint.mesh_geometry)
        #self.mesh_geometry = uncut_mesh
        
    def draw_uncut_mesh(self):
        box = Box(self.frame, self.length,self.height,self.width)
        self.beam_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces) 
        return self.beam_mesh

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
        xaxis_viz = add_vectors(f_v1, scale_vector(xaxis_vec, 0.1)) #visualization for vector 

        f_c = self.beam_mesh.face_centroid(self.face_id)
        yaxis_vec = self.beam_mesh.face_normal(self.face_id)
        yaxis_viz = add_vectors(f_c, scale_vector(yaxis_vec,100)) #visualization for vector 

        #frame at self.dist
        dist_point = get_point_coordinates(self.dist)
        self.f_frame = Frame(dist_point[0], xaxis_vec, yaxis_vec)

        #get join_90lap mesh
        joint_in = j.joint(Frame.worldXY, 100, 100, -50)
        joint = joint_in.update_joint()
        joint_mesh = Mesh.from_vertices_and_faces(joint.vertices, joint.faces)
        bool_frame = Frame([0, 0, 0], [1, 0, 0], [0, 0, 1]) #world frame values hard coded, needs to be fixed

        #Transformation
        T = Transformation.from_frame_to_frame(bool_frame,self.f_frame)
        joint_mesh_pos = mesh_transform(joint_mesh, T) #mesh of translated mesh
        self.joint_mesh_pos.append(joint_mesh_pos)  

        #beamboolean
        boolean_list = []
        beam_1 = self.draw_uncut_mesh()
        boolean_list.append(beam_1)
        boolean_list.append(joint_mesh_pos)
        _engin = 'auto'

        beam_boolean = self.boolean_subtract(boolean_list, _engin)

        return beam_boolean

    def boolean_subtract(self, B_list, _engin):
        with Proxy('trimesh') as t:
            boolean_out = t.boolean.difference(B_list, _engin)
        # with Proxy('trimesh') as t:
        # bool_mesh = t.boolean_subtract(T1, T2)
        return  boolean_out

    def new_beam(self):
        #new_beam geometry
        box = Box(Frame.worldXY(),self.new_beam_ht,100,100)
        box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

        #attriutes of box_mesh
        face_id = 5
        vertices_id = box_mesh.face_vertices(face_id)
        vertices = []
        for key in vertices_id:
            v = box_mesh.vertex_coordinates(key)
            vertices.append(v)
        #xaxis
        x_1 = vertices[0]
        x_2 = vertices[1]
        x_3 = subtract_vectors(x_1, x_2)
        x_4 = add_vectors(x_1, scale_vector(x_3,0.1))#visualization of vectors
        #yaxis
        y_1 = vertices[1]
        y_2 = vertices[2]
        y_3 = subtract_vectors(y_1, y_2)
        y_4 = add_vectors(y_1, scale_vector(y_2, 2.5))#visualization of vectors
        #centroid
        c_1 = box_mesh.face_centroid(face_id)
        c_2 = box_mesh.face_normal(face_id)
        #newframe for new_beam
        new_beam_frame = Frame(c_1, y_3, x_3)
        #Transformation 
        T = Transformation.from_frame_to_frame(new_beam_frame,self.f_frame)
        bool_newbeam_mesh = mesh_transform(box_mesh, T)

        #neam_beam boolean
        newbeam_boolean_list = []
        beam_1 = self.get_bool_pos()
        boolean_list.append(beam_1)
        boolean_list.append(bool_newbeam_mesh)
        _engin = 'auto'

        return bool_newbeam_mesh


if __name__ == '__main__':

    # from compas.geometry import Box
    # from compas.datastructures import Mesh

    # box = Box(Frame.worldXY(),3000,100,100)
    # mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)
    # face_id = 1
    # pt = (0,0,0)

    # beam_in = Beam(mesh, face_id, pt)
    
    print("ok")