import compas
import os 
import Beam as b

from Joint_90lap import Joint_90lap
from compas.geometry import subtract_vectors
from compas.geometry import Translation
from compas.geometry import Frame
from compas.geometry import Transformation

class Model(object):
    """This class is an assembly model
    """
    
    def __init__(self):
   
        self.uncut_beam=[]
        self.beams=[] # <- only one list should stay
        self.beam_match=[]
        # self.vertices=[]

    def create_beam(self, frame, depth, width, height,name):
        self.new_beam = b.Beam(frame, depth, width, height,name)
        self.uncut_beam.append(self.new_beam)
        return self.new_beam
   
    def utilities_vertices(self,beam,face_id):
        self.vertices = []
        vertices_id = beam.face_vertices(face_id)
        for key in vertices_id:
            a = beam.vertex_coordinates(key)
            self.vertices.append(a)
        return self.vertices      
        
    def rule_90lap(self,beam_to_match,face_id,distance):
        #calculations for frame ideal should be in joint class
        v = self.utilities_vertices(beam_to_match,face_id)

        x_axis = subtract_vectors(v[0], v[1])
        y_axis = subtract_vectors(v[1], v[2])
        centroid = beam_to_match.face_centroid(face_id)
        face_frame = Frame(centroid, x_axis, y_axis)
        dist = face_frame.transformed(Translation([distance,0,0]))#transformation for distance
        joint_frame = dist.transformed(Translation([0,-50,50]))
    
        self.joints = Joint_90lap(joint_frame,face_id,50,100,100) 
        #TRIMESH proxy function
        self.mesh_90lap = b.Beam.trimesh_proxy_subtract(self.new_beam,self.joints)#this is not ideal
        self.beams.append(self.mesh_90lap)
        #self.beams.append(self.joints.mesh)
    
    # def create_beam_match(self,beam_to_match,face_id,extension,distance):       
       
    #     v_1 = self.utilities_vertices(beam_to_match.mesh,face_id)
    #     v1_xaxis = subtract_vectors(v_1[0], v_1[1])
    #     v1_yaxis = subtract_vectors(v_1[1], v_1[2])  
    #     v1_centroid = beam_to_match.mesh.centroid()
    #     beam_frame_c = Frame(v1_centroid, v1_xaxis, v1_yaxis)
        
    #     y = -(beam_to_match.width/2)
    #     z = ((beam_to_match.length+extension)/2)
    #     join_frame = beam_frame_c.transformed(Translation([distance,-50,50]))
    #     beam_frame = beam_frame_c.transformed(Translation([distance,y,z]))#transformation for distance
    #     self.test = b.Beam(beam_frame, (beam_to_match.length+extension), beam_to_match.width, beam_to_match.height)

    #     self.match_joint = Joint_90lap(join_frame,face_id,50,100,100) 
    #     #TRIMESH proxy function
    #     self.match_90lap = b.Beam.trimesh_proxy_subtract(self.test ,self.match_joint)#this is not idea
    #     #self.beam_match.append(self.beam_match_mesh)

    #     return self.match_90lap 

    

#    Make a function for joint_frame
#    beam_to_match.joints.append(Joint_90(beam_to_match,face_id,distance))

#    #Compute input_beam_face_frame, based on beam_frame and face_id
#    #Translate input_beam_face_frame to new beam frame, based on distance and new beam length

#    new_beam = Beams(new_beam_frame, depth, width, height)

#    new_beam.joint.append(Joint_90(new_beam,3,distance))
#    beams.append(new_beam)

#    pass
  
    def load_beams(self, foostring):
        
        HERE = os.path.dirname(__file__)
        DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
        FILE_I = os.path.join(DATA, foostring)
        return FILE_I
             
 
if __name__ == '__main__':
    import compas
    from compas.datastructures import Mesh
    from compas.geometry import Frame
    from compas_rhino.artists import MeshArtist
    from compas_rhino.artists import Artist
    from id_generator import create_id


    m = Model()
    test = m.create_beam(Frame.worldXY(),10,20,30,create_id())
    # m.create_beam(Frame.worldXY(),100,200,300)
    # m.create_beam(Frame.worldXY(),1000,200,3000)
    # test2 = m.create_beam_match(test,0,300,100)
    #test3 = m.utilities_vertices(test.mesh,0)



    #print(m.beams)
    # for beam in m.beam_match:
    #     print(type(beam))




    for beam in m.beams:
        m.rule_90lap(beam,1,200)


    # artist = Artist(layer='Beams_out')
    # artist.clear_layer()
    # for beam in m.beams:
    #     artist = MeshArtist(beam.mesh, layer='Beams_out')
    #     artist.draw_faces(join_faces=False)

        
    
#    
#        print(type(beam))
#        print(beam.width)
#        print(beam.height)
#        artist = MeshArtist(beam, layer='Beams_out')
#        artist.clear_layer()
#        artist.draw_faces(join_faces=False)