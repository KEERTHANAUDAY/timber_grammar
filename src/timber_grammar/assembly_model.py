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

    def create_beam(self, frame, length, width, height,name):
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
    
    def get_joint_frame(self,BeamRef,joint_dist,face_id):
        """
        Computes the frame of selected face and translates it to the picked point location

        Parameters
        ----------
        BeamRef:  Beam Object 
        joint_dist:  double
        face_id:  int

        Return
        ------
        compas Frame

        """
        joint_face = BeamRef.get_face_frame(face_id)
        if face_id == 3:     
            y_trans = (joint_face.yaxis*(joint_dist))
            z_trans = (joint_face.normal*-100)
            joint_frame = joint_face.transformed(Translation([(y_trans)[0],(y_trans)[1],(y_trans)[2]]))
            joint_frame = joint_frame.transformed(Translation([(z_trans)[0],(z_trans)[1],(z_trans)[2]]))
        elif face_id == 4:
            y_trans = (joint_face.yaxis*joint_dist)
            joint_frame = joint_face.transformed(Translation([(y_trans)[0],(y_trans)[1],(y_trans)[2]]))
        elif face_id == 2:
            y_trans = (joint_face.yaxis*-joint_dist)
            z_trans = (joint_face.normal*50)
            x_trans = (joint_face.xaxis*-100)
            joint_frame = joint_face.transformed(Translation([(y_trans)[0],(y_trans)[1],(y_trans)[2]]))
            joint_frame = joint_frame.transformed(Translation([(z_trans)[0],(z_trans)[1],(z_trans)[2]]))
            joint_frame = joint_frame.transformed(Translation([(x_trans)[0],(x_trans)[1],(x_trans)[2]]))
        elif face_id == 1:
            y_trans = (joint_face.yaxis*joint_dist)
            z_trans = (joint_face.zaxis*-50)
            joint_frame = joint_face.transformed(Translation([(y_trans)[0],(y_trans)[1],(y_trans)[2]]))
            joint_frame = joint_frame.transformed(Translation([(z_trans)[0],(z_trans)[1],(z_trans)[2]]))

        else:
            pass

        return joint_frame

    def get_match_beam_frame(self,BeamRef,ext_b,joint_dist,face_id):
        
        """Translates the location of the match Beam frame
            works in conjunction with get_joint_frame
        Parameters:
        ----------
        BeamRef: Beam Object
        ext_b:  Beam extension (distance used for translation)
        joint_dist: (double) distance of the frame 
        face_id: (int) ID of the selected face 

        Return:
        ------
        compas Frame
        """
        face_frame = self.get_joint_frame(BeamRef,joint_dist,face_id)
        if face_id == 4:
            x_trans = (face_frame.xaxis*-ext_b)
            match_beam_frame = face_frame.transformed(Translation([(x_trans)[0],(x_trans)[1],(x_trans)[2]]))

        elif face_id == 3:
            x_trans = (face_frame.xaxis*-ext_b)
            match_beam_frame = face_frame.transformed(Translation([(x_trans)[0],(x_trans)[1],(x_trans)[2]]))

        elif face_id == 2:
            z_trans = (face_frame.normal*-50)
            x_trans = (face_frame.xaxis*-ext_b)
            match_beam_frame = face_frame.transformed(Translation([(z_trans)[0],(z_trans)[1],(z_trans)[2]]))
            match_beam_frame = match_beam_frame.transformed(Translation([(x_trans)[0],(x_trans)[1],(x_trans)[2]]))

        elif face_id == 1:
            x_trans = (face_frame.xaxis*-ext_b)
            z_trans = (face_frame.zaxis*-50)
            match_beam_frame = face_frame.transformed(Translation([(x_trans)[0],(x_trans)[1],(x_trans)[2]]))
            match_beam_frame = match_beam_frame.transformed(Translation([(z_trans)[0],(z_trans)[1],(z_trans)[2]]))

        return match_beam_frame

    def Get_distancefromBeamYZFrame(self,BeamRef,placed_point):
        """Computes the distance from selected point to Beam YZ_Plane(face_id = 0)
        Parameters:
        ----------
        BeamRef: Beam Object
        placed_point: Point3d
        Return:
        ------
        distance (double)
        """
        YZ_Plane = BeamRef.get_face_frame(0)
        dist = distance_point_plane(placed_point,YZ_Plane)
        return dist
 
    def rule_90lap(self,BeamRef,placed_point,face_id):
        """Performs 90Lap joint boolean operation to beam object:
        ----------
        BeamRef: Beam Object
        placed_point: Point3d
        face_id: (int) ID of selected face of Beam

        Return:
        ------
        No return 
        """
        dist = self.Get_distancefromBeamYZFrame(BeamRef,placed_point)
        joint_dist = self.get_joint_frame(BeamRef,dist,face_id)
        BeamRef.joints.append(Joint_90lap(joint_dist,face_id,100,100,50))
        BeamRef.update_mesh()

    def match_beam(self,BeamRef,ext_a,ext_b,name,placed_point,face_id,match_face_id):
        """Creates a 90 Lap joint match beam to selected Beam
        ----------
        BeamRef: Beam Object
        ext_a: Beam Offset up or right
        ext_b: Beam Offset down or left
        name: UUID 
        placed_point: Point3D
        face_id: (int) ID of selected face of Beam
        match_face_id: face_id to place joint for match beam 
        
        Return:
        ------
        Beam Object 
        """   
        dist = self.Get_distancefromBeamYZFrame(BeamRef,placed_point)
        match_beam_frame = self.get_match_beam_frame(BeamRef,ext_b,dist,face_id)
        match_beam = Beam(match_beam_frame,(ext_a+100+ext_b),100,100,name)

        joint_dist = self.get_joint_frame(match_beam,ext_b,match_face_id)
        match_beam.joints.append(Joint_90lap(joint_dist,match_face_id,100,100,50))
        match_beam.update_mesh()

        self.beams.append(match_beam)
        return match_beam


     
   
#if __name__ == '__main__':
#    import compas
#    from compas.datastructures import Mesh
#    from compas.geometry import Frame
#    from compas_rhino.artists import MeshArtist
#    from compas_rhino.artists import Artist
#    from Joint_90lap import Joint_90lap
#    from id_generator import create_id
#    
#    #Create Beam object
#    beam = Beam(Frame.worldXY(),1000,100,150,create_id())
#
#    #Create some joints on the beam
#    beam.joints.append(Joint_90lap(Frame.worldXY(),1,50,100,100)) #Note that the position of the joint is dummy data.
#    from compas.geometry import Translation
#    joint_frame = beam.frame.transformed(Translation([200,0,0]))
#    beam.joints.append(Joint_90lap(joint_frame,3,50,100,100)) #Note that the position of the joint is dummy data.
#    
#    #Update mesh - Boolean the joints from Mesh
#    beam.update_mesh()
#
#    #Add beam into model
#    model = Model()
#    model.beams.append(beam)
#
#    #Save and load the model
#    model.to_json("model.json")
#    loaded_model = Model.from_json("model.json")
#    loaded_model.to_json("model2.json")
#
#    print ("Comparing two data dictionary:")
#    assert (model.data == loaded_model.data)
#    if (model.data == loaded_model.data) :
#        print("Correct") 
#    else:
#        print("Incorrect")
#    

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