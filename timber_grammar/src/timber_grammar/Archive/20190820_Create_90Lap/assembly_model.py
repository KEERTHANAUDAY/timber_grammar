import compas
import os 
import json
from Beam import Beam

from Joint_90lap import Joint_90lap
from compas.geometry import subtract_vectors
from compas.geometry import Translation
from compas.geometry import Frame
from compas.geometry import Transformation

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
        with open(filepath, 'w+') as fp:
            if pretty:
                json.dump(self.data, fp, sort_keys=True, indent=4)
            else:
                json.dump(self.data, fp)

    def create_beam(self, frame, depth, width, height,name):
        self.new_beam = Beam(frame, depth, width, height,name)
        self.beams.append(self.new_beam)
        return self.new_beam#.mesh was removed
        
    # def rule_90lap(self,beam_to_match,face_id,distance):
    def rule_90lap(self,beam,position_pt,face_id):

        if face_id == 1:
            joint_frame = Frame(position_pt,beam.frame.xaxis,beam.frame.yaxis)
            beam.joints.append(Joint_90lap(joint_frame,face_id,100,50,100))
            beam.update_mesh()
        elif face_id == 3:
            joint_frame = Frame(position_pt,beam.frame.xaxis,beam.frame.yaxis)
            joint_frame_T = joint_frame.transformed(Translation([0,50,0]))
            beam.joints.append(Joint_90lap(joint_frame_T,face_id,100,50,100))
            beam.update_mesh()
        else:
            pass

        #implement if or assert checks to make sure the face is right
        # beam_object.joints.append(Joint_90lap(joint_frame,face_id,100,100,50))
        # beam_object.update_mesh()
        # self.beams.append(beam_object)
        # return beam_90lap_mesh

  
    def create_beam_match(self,beam_to_match,face_id,extension,distance):  
        pass   

        #input beam + extension length(may be call create_beam)
        #create joint
        #update mesh

    def joint_frame(self):
        #this will perform the frame calculations
        pass

    

#    Make a function for joint_frame
#    beam_to_match.joints.append(Joint_90(beam_to_match,face_id,distance))

#    #Compute input_beam_face_frame, based on beam_frame and face_id
#    #Translate input_beam_face_frame to new beam frame, based on distance and new beam length

#    new_beam = Beams(new_beam_frame, depth, width, height)

#    new_beam.joint.append(Joint_90(new_beam,3,distance))
#    beams.append(new_beam)

#    pass
  

 
if __name__ == '__main__':
    import compas
    from compas.datastructures import Mesh
    from compas.geometry import Frame
    from compas_rhino.artists import MeshArtist
    from compas_rhino.artists import Artist
    from Joint_90lap import Joint_90lap
    from id_generator import create_id
    
    #Create Beam object
    beam = Beam(Frame.worldXY(),1000,100,150,create_id())

    #Create some joints on the beam
    beam.joints.append(Joint_90lap(Frame.worldXY(),1,50,100,100)) #Note that the position of the joint is dummy data.
    from compas.geometry import Translation
    joint_frame = beam.frame.transformed(Translation([200,0,0]))
    beam.joints.append(Joint_90lap(joint_frame,3,50,100,100)) #Note that the position of the joint is dummy data.
    
    #Update mesh - Boolean the joints from Mesh
    beam.update_mesh()

    #Add beam into model
    model = Model()
    model.beams.append(beam)

    #Save and load the model
    model.to_json("model.json")
    loaded_model = Model.from_json("model.json")
    loaded_model.to_json("model2.json")

    print ("Comparing two data dictionary:")
    assert (model.data == loaded_model.data)
    if (model.data == loaded_model.data) :
        print("Correct") 
    else:
        print("Incorrect")
    

    # m = Model()
    # m.create_beam(Frame.worldXY(),10,20,30,name)
    # #t.joints.append(Joint_90lap(Frame.worldXY(),1,50,100,100))

    # m.to_json("august.json",pretty=True)
    
    # loaded_beam = m.from_json("august.json")
    # print(loaded_beam)
    # print(loaded_beam.data)

        
    
#    
#        print(type(beam))
#        print(beam.width)
#        print(beam.height)
#        artist = MeshArtist(beam, layer='Beams_out')
#        artist.clear_layer()
#        artist.draw_faces(join_faces=False)