import compas
import os 
import json
from Beam import Beam

from Joint_90lap import Joint_90lap
from compas.geometry import subtract_vectors
from compas.geometry import Translation
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Vector
from compas.geometry import add_vectors
from compas.geometry import distance_point_plane
from compas.geometry import subtract_vectors
from id_generator import create_id

class Model(object):
    """This class is an assembly model
    it will not call the proxy, all boolean operations happen in the beam class
    """
    
    def __init__(self):

        self.beams=[] # <- only one list should stay

    @property
    def data(self):
        """dict : A data dict representing all internal persistant data for serialisation.
        The dict has the following structure:
        * 'type'            => string (name of the class)
        * 'beams'           => list of dict of Beam.to_data()
        """
        data = {
            'type'      : self.__class__.__name__,
            'beams'     : [beam.to_data() for beam in self.beams]
            }
        return data
    

    @data.setter
    def data(self, data):
        for beam_data in data.get('beams'):
            self.beams.append(Beam.from_data(beam_data))

    @classmethod
    def from_data(cls,data):
        """Construct an assembled Beam object from structured data.
        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        object
            An object of the type Model

        Note
        ____
        This constructor method is meant to be used in conjuction with
        the corresponding *to_data* method.
        """
        new_object = cls()
        new_object.data = data

        return new_object

      
    def to_data(self):
        """Returns a dict of structured data representing the data structure.
        Actual implementation is in @property def data(self)

        Returns
        _______
        dict
            The structued data.

        Note
        ____
        This method produces the data that can be used in conjuction with the
        corresponding *from_data* class method.

        """
        return self.data

    @classmethod
    def from_json(cls, filepath):
        """Construct a datastructure from structured data contained in a json file.

            Parameters
            ---------
            filepath : str
            The path to the json file.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_json* method.

        """
        
        # PATH = os.path.abspath(os.path.join(filepath, '..', 'data'))
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        return cls.from_data(data)

    def to_json(self, filepath, pretty=False):
        """Serialise the structured data representing the data structure to json.

        Parameters
        ----------
        filepath : str
            The path to the json file.

        """
        # PATH = os.path.abspath(os.path.join(filepath, '..', 'data'))
        with open(filepath, 'w+') as fp:
            if pretty:
                json.dump(self.data, fp, sort_keys=True, indent=4)
            else:
                json.dump(self.data, fp)

    def rule_create_beam(self, frame, length, width, height,name):
        """Creates a Beam Object.

        Parameters
        ----------
        frame:  Compas Frame 
        length:  double
        width:  double
        height: double
        name:   UUID
        """
        self.new_beam = Beam(frame, length, width, height,name)
        self.beams.append(self.new_beam)
        return self.new_beam 
    
    def rule_90lap(self, beam, joint_distance_from_start, face_id, ext_start, ext_end, name):
        """Performs 90Lap joint boolean operation to beam object:
        ----------
        BeamRef: Beam Object
        placed_point: Point3d
        face_id: (int) ID of selected face of Beam

        Return:
        ------
        No return 
        """
        #Add joint90Lap to Beam 1
        #selected Beam and its boolean
        joint = Joint_90lap(joint_distance_from_start,face_id,100,50,100)
        beam.joints.append(joint)
        joint.update_joint_mesh(beam)
        beam.update_mesh()

        #Add Beam 2 to model

        #get match_beam_frame
        face_frame = beam.face_frame(face_id)
        match_beam_origin = face_frame.represent_point_in_global_coordinates([(joint_distance_from_start-50) , 0, beam.height + ext_end]) 
        match_beam_frame = Frame(match_beam_origin, face_frame.normal * -1.0, face_frame.yaxis)
        #length of match beam 
        length = ext_end + ext_start + beam.height #height is picked instead of heard coding 100 since the frame is always created on the face(XZPlane)
        #name of match beam 
        name = create_id()
  
        match_beam = self.rule_create_beam(match_beam_frame,length,100,100,name)

        #Add joint90Lap to Beam 2
        #Update mesh of 2 new joints and 2 beams
        match_beam_joint = Joint_90lap((ext_end+50),3,100,50,100)
        match_beam.joints.append(match_beam_joint)
        match_beam_joint.update_joint_mesh(match_beam)
        match_beam.update_mesh()
 

    
    # def match_Beam_to_Beams(self,BeamRefs,length,ext,name,joint_points,face_id,match_face_id):
    #     """Creates a 90 Lap joint match beam to selected Beam
    #     ----------
    #     BeamRefs:        list of Beam Object
    #     length:         length of match Beam
    #     ext:            Beam Offset from selected point
    #     name:           UUID 
    #     joint_points:   list of points of origin got joint
    #     face_id:        (int) ID of selected face of Beam
    #     match_face_id:  face_id to place joint for match beam 
        
    #     Return:
    #     ------
    #     Match beam with booleaned joints  
    #     """   
        
    #     dist = self.Get_distancefromBeamYZFrame(BeamRefs[0],joint_points[0])  
       
    #     match_beam_frame = self.get_match_beam_frame(BeamRefs[0],ext,dist,face_id)
    #     #make a singlebeam
    #     match_beam = Beam(match_beam_frame,length,100,100,name)

    #     #append joints to match_beam 
    #     joint_dist = [] 
    #     joint_frames = []
    #     for joint_point in joint_points:
    #         dist = self.Get_distancefromBeamYZFrame(match_beam,joint_point)
    #         joint_dist.append(dist)
    #     #     joint_frame = self.get_joint_frame(match_beam,dist,match_face_id)
    #     #     joint_frames.append(joint_frame)
    #     #     match_beam.joints.append(Joint_90lap(joint_frame,match_face_id,100,100,50))
    #     # match_beam.update_mesh()

    #     # self.beams.append(match_beam)
    #     return joint_dist
 


     
   
if __name__ == '__main__':

    pass
#    import compas
#    from compas.datastructures import Mesh
#    from compas.geometry import Frame
#    from compas_rhino.artists import MeshArtist
#    from compas_rhino.artists import Artist
#    from Joint_90lap import Joint_90lap
#    from id_generator import create_id
   
#    Create Beam object
#    beam = Beam(Frame.worldXY(),1000,100,150,create_id())

#    Create some joints on the beam
#    beam.joints.append(Joint_90lap(Frame.worldXY(),1,50,100,100)) #Note that the position of the joint is dummy data.
#    from compas.geometry import Translation
#    joint_frame = beam.frame.transformed(Translation([200,0,0]))
#    beam.joints.append(Joint_90lap(joint_frame,3,50,100,100)) #Note that the position of the joint is dummy data.
   
#    Update mesh - Boolean the joints from Mesh
#    beam.update_mesh()

#    Add beam into model
#    model = Model()
#    model.beams.append(beam)

#    Save and load the model
#    model.to_json("model.json")
#    loaded_model = Model.from_json("model.json")
#    loaded_model.to_json("model2.json")

#    print ("Comparing two data dictionary:")
#    assert (model.data == loaded_model.data)
#    if (model.data == loaded_model.data) :
#        print("Correct") 
#    else:
#        print("Incorrect")
   

#     m = Model()
#     m.create_beam(Frame.worldXY(),10,20,30,name)
#     t.joints.append(Joint_90lap(Frame.worldXY(),1,50,100,100))

#     m.to_json("august.json",pretty=True)
    
#     loaded_beam = m.from_json("august.json")
#     print(loaded_beam)
#     print(loaded_beam.data)

        
    
   
#        print(type(beam))
#        print(beam.width)
#        print(beam.height)
#        artist = MeshArtist(beam, layer='Beams_out')
#        artist.clear_layer()
#        artist.draw_faces(join_faces=False)