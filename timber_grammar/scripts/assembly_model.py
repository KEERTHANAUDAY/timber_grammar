import compas
import os 
import Beam


class Model(object):
    """This class is an assembly model
    """
    
    def __init__(self):
    
        self.beams=[]

    def create_beam(self,frame, depth, width, height):
        new_beam = Beam.Beam(frame, depth, width, height)
        #new_beam.draw_uncut_mesh()
        self.beams.append(new_beam)
        
        
   
#def rule_90lap(beam_to_match,face_id,distance):
#    beam_to_match.joints.append(Joint_90(beam_to_match,face_id,distance))
#    #Compute input_beam_face_frame, based on beam_frame and face_id
#    #Translate input_beam_face_frame to new beam frame, based on distance and new beam length
#    new_beam = Beams(new_beam_frame, depth, width, height)
#    new_beam.joint.append(Joint_90(new_beam,3,distance))
#    beams.append(new_beam)
#    pass
#    
    def load_beams(self, foostring):
        
        HERE = os.path.dirname(__file__)
        DATA = os.pathsep.abspath(os.pathsep.join(HERE, '..', 'data'))
        FILE_I = os.path.join(DATA, foostring)
        return FILE_I
        
        
        
        #beams = load_from_json("beam.json")
#
#def save_beams():
#    save_to_json(beams, "beam.json")
#    
if __name__ == '__main__':
    from compas.geometry import Frame
    from compas_rhino.artists import MeshArtist
    from compas_rhino.artists import Artist

    
    m = Model()
    m.create_beam(Frame.worldXY(),10,20,30)
    m.create_beam(Frame.worldXY(),100,200,300)
    m.create_beam(Frame.worldXY(),1000,200,3000)
    print(m.beams)
    
    for beam in m.beams:
        print(type(beam))
        print(beam.width)
        print(beam.height)
        artist = MeshArtist(beam, layer='Beams_out_2')
        artist.clear_layer()
        artist.draw_faces(join_faces=False)