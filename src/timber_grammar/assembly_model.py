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
        match_beam_origin = face_frame.represent_point_in_global_coordinates([(joint_distance_from_start-50) , 0, beam.height + ext_start]) 
        match_beam_frame = Frame(match_beam_origin, face_frame.normal * -1.0, face_frame.yaxis)
        #length of match beam 
        length = ext_end + ext_start + beam.height #height is picked instead of heard coding 100 since the frame is always created on the face(XZPlane)
        #name of match beam 
        name = create_id()
  
        match_beam = self.rule_create_beam(match_beam_frame,length,100,100,name)

        #Add joint90Lap to Beam 2
        #Update mesh of 2 new joints and 2 beams
        match_beam_joint = Joint_90lap((ext_start+50),3,100,50,100)
        match_beam.joints.append(match_beam_joint)
        match_beam_joint.update_joint_mesh(match_beam)
        match_beam.update_mesh()

        return [match_beam_origin]
    
    def rule_Connect_90lap(self,selected_beams,projected_point_list,face_ids,beam_length,ext_start,name):

        #create joints on selected beams 
        joint_distance_to_selectedBeams = []
        for i in range (len(selected_beams)):
            print("Adding Joint to Beam: ", i)
            #Prepare information
            selected_beam =  selected_beams[i]
            projected_point = projected_point_list[i]
            face_id = face_ids[i]
            print(face_id)
            joint_distance = selected_beam.Get_distancefromBeamYZFrame(projected_point)
            joint_distance_to_selectedBeams.append(joint_distance)
            #Create Joint
            new_joint = Joint_90lap(joint_distance,face_id,100,50,100)
            #Add new Joint to Beam and update beam mesh
            selected_beam.joints.append(new_joint)
            new_joint.update_joint_mesh(selected_beam)
            selected_beam.update_mesh()

            
        #Add match beam 
        #####get beam frame 
        #construct a frame similar to face frame with max point as origin 
        
        face_frame = selected_beams[0].face_frame(face_ids[0])
        max_point_frame = Frame(face_frame.point,face_frame.xaxis,face_frame.yaxis)
        connection_beam_origin = max_point_frame.represent_point_in_global_coordinates([(joint_distance_to_selectedBeams[0]-50),0, ext_start])
        connection_beam_frame = Frame(connection_beam_origin, face_frame.normal * -1.0, face_frame.yaxis)

        match_beam = self.rule_create_beam(connection_beam_frame,beam_length,100,100,name)

        #calculate distance from projected points to match_beam[0]plane
        for i in range(len(projected_point_list)):
            print("Adding Joint " , i)
            pt = projected_point_list[i]
            match_beam_joint_distance = match_beam.Get_distancefromBeamYZFrame(pt)
            joint = Joint_90lap(match_beam_joint_distance,3,100,50,100) #match_beam joint face is always 3 
            match_beam.joints.append(joint)
            joint.update_joint_mesh(match_beam)

        #performs multiple booleans in 1 call   
        match_beam.update_mesh()

 
if __name__ == '__main__':
    pass
    # import compas
    # from compas.datastructures import Mesh
    # from compas.geometry import Frame
    # from compas_rhino.artists import MeshArtist
    # from compas_rhino.artists import Artist
    # from Joint_90lap import Joint_90lap
    # from id_generator import create_id


    # beam = Beam(Frame.worldXY(),1000,100,150,create_id())


    # beam.joints.append(Joint_90lap(Frame.worldXY(),1,50,100,100)) #Note that the position of the joint is dummy data.
    # from compas.geometry import Translation
    # joint_frame = beam.frame.transformed(Translation([200,0,0]))
    # beam.joints.append(Joint_90lap(joint_frame,3,50,100,100)) #Note that the position of the joint is dummy data.

    # beam.update_mesh()


    # model = Model()
    # model.beams.append(beam)


    # model.to_json("model.json")
    # loaded_model = Model.from_json("model.json")
    # loaded_model.to_json("model2.json")

    # print ("Comparing two data dictionary:")
    # assert (model.data == loaded_model.data)
    # if (model.data == loaded_model.data) :
    #     print("Correct") 
    # else:
    #     print("Incorrect")


    # m = Model()
    # m.create_beam(Frame.worldXY(),10,20,30,name)
    # t.joints.append(Joint_90lap(Frame.worldXY(),1,50,100,100))

    # m.to_json("august.json",pretty=True)

    # loaded_beam = m.from_json("august.json")
    # print(loaded_beam)
    # print(loaded_beam.data)

        
