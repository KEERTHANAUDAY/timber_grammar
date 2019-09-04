import math
import compas
from compas.geometry import Box
from compas.datastructures import Mesh
from compas.datastructures import mesh_bounding_box
from id_generator import create_id
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Translation

from Joint import Joint
import json

from compas.rpc import Proxy
import sys
python_exe_path = sys.executable

class Beam(object):
    """ Beam class creates beams and performs booleans(called through tri
    mesh proxy)
    """

    def __init__(self, frame, length, width, height, name ):
        """ initialization

            :frame:           base plane for the beam 
            :length:          the length along the local x-axis (Typically the long side)
            :width:           the length along the local z-axis (Short Side of Side 1 and Side 3)
            :height:          the length along the local y-axis (Short Side of Side 2 and Side 4)
            :name(optional):  UUID generated frim id_generator as name for each mesh
            
        """
        self.frame = frame
        self.length = length 
        self.width = width
        self.height = height 
        self.name = name
        # self.face_frame = None
        self.mesh = None
        self.joints = []
        
        #Perform initial calculation of the mesh if this object is not empty
        if frame is not None:  
            self.update_mesh()


    @property   
    def data(self):
        """dict : A data dict representing all internal persistant data for serialisation.
        The dict has the following structure:
        * 'type'            => string (name of the class)
        * 'frame'           => dict of compas.frame.to_data()
        * 'length'          => double
        * 'width'           => double
        * 'height'          => double
        * 'mesh'            => dict of compas.mesh.to_data()
        * 'joints'          => list of dict of Joint.to_data()
        * 'name'            => string
        """
        data = {
            'type'      : self.__class__.__name__, #Keep this line for deserialization
            'frame'     : None,   
            'length'    : self.length,
            'width'     : self.width,
            'height'    : self.height,
            'name'      : self.name,
            'mesh'      : None,
            'joints'    : [joint.to_data() for joint in self.joints],
            }
        if (self.frame is not None) : 
            data['frame'] = self.frame.to_data()
        if (self.mesh is not None) :
            data['mesh'] = self.mesh.to_data()
        return data
    
    @data.setter
    def data(self, data):
        self.frame      = None
        if (data.get('frame') is not None): self.frame = compas.geometry.Frame.from_data(data.get('frame'))
        self.length      = data.get('length') or None
        self.width      = data.get('width') or None
        self.height     = data.get('height') or None
        self.name       = data.get('name') or None
        self.mesh       = None
        if (data.get('mesh') is not None): self.mesh = compas.datastructures.Mesh.from_data(data.get('mesh'))
        for joint_data in data.get('joints') :
            self.joints.append(Joint.from_data(joint_data))
    
    @classmethod
    def from_data(cls,data):
        """Construct a Beam object from structured data.
        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        object
            An object of the type Beam

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_data* method.

        """

        new_object = cls(None,None,None,None,None) # Only this line needs to be updated
        new_object.data = data
        if new_object.mesh is None:
            new_object.update_mesh()
        return new_object
   

    def to_data(self):
        """Returns a dictionary of structured data representing the data structure.
        Actual implementation is in @property def data(self)

        Returns
        -------
        dict
            The structured data.

        Note
        ----
        This method produces the data that can be used in conjuction with the
        corresponding *from_data* class method.

        """
        return self.data

    @classmethod
    def from_json(cls, filepath):
        """Construct a datastructure from structured data contained in a json file.

        Parameters
        ----------
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
        print('type: ', data['type'])

        assert data['type'] ==  cls.__name__ , "Deserialized object type: %s is not equal to %s." % (data['type'] , cls.__name__)
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

    #Here is where the functions of the class begins
    def update_mesh(self):
        '''Computes the beam geometry with boolean difference of all joints.

        Returns
        -------
        compas.datastructures.Mesh
        The beam mesh with joint geoemtry removed

        Note
        ----------
        self.mesh is updated.
        '''
        self.mesh = self.draw_uncut_mesh()
        for joint in self.joints:
            self.mesh = self.trimesh_proxy_subtract(self.mesh,joint.mesh) #why am i giving joint.mesh and not joint, isn't trimesh_proxy_subtract a classmethod?
        self.mesh.name = self.name
        return self.mesh
    
   
    # Here we compute the face_frame of the beam
    def face_frame(self,face_id):
        """Computes the frame of the selected face
        ----------
        face_id: (int) ID of selected face of Beam

        Return:
        ------
        compas Frame 
        """
        if face_id == 1:
            return self.frame.copy()
        if face_id == 2:
            new_origin = self.frame.represent_point_in_global_coordinates([0,self.height,0])
            return Frame(new_origin,self.frame.xaxis, self.frame.normal)
        if face_id == 3:
            new_origin = self.frame.represent_point_in_global_coordinates([0,self.height,self.width])
            return Frame(new_origin,self.frame.xaxis, self.frame.yaxis * -1.0)
        if face_id == 4:
            new_origin = self.frame.represent_point_in_global_coordinates([0,0,self.width])
            return Frame(new_origin,self.frame.xaxis, self.frame.normal * -1.0)
        else:
            raise IndexError('face_id index out of range')

    def face_plane(self,face_id):

        origin_frame = self.frame.copy()
        if face_id == 0:
            plane = Plane(origin_frame.point, origin_frame.xaxis)
        return plane

    def draw_uncut_mesh(self):
        '''Computes and returns the beam geometry.

        Returns
        -------
        compas.datastructures.Mesh
        The beam mesh without joint geoemtry

        '''
        box = Box(self.frame, self.length,self.width,self.height)
        box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces) 
        return box_mesh

    def draw_cut_match_mesh(self,match_beam_mesh):

        for joint in self.joints:
            self.mesh = self.trimesh_proxy_subtract(match_beam_mesh,joint.mesh)
        return self.mesh

    @classmethod #hence does not rely on the instance of the Beam class, inout of the type is enough
    def trimesh_proxy_subtract(cls,mesh_a,mesh_b):
        '''Computes boolean through trimesh by calling compas proxy.

        Returns
        -------
        compas.datastructures.Mesh

        '''
        with Proxy(package='Trimesh_proxy',python=python_exe_path) as f:
            result = f.trimesh_subtract(mesh_a, mesh_b)
            result_mesh = Mesh.from_data(result['value'])
        return result_mesh

        
if __name__ == '__main__':
    #Test 1 : Beam data to be saved and loaded and the two should be the same.
    import compas
    import tempfile
    import os
    from compas.datastructures import Mesh
    from compas.geometry import Point
    from compas.geometry import Vector
    from compas.geometry._primitives import Frame
    from compas.geometry._primitives.box import Box

    from id_generator import create_id

    name = create_id()

    #Create Beam object
    #beam = Beam(Frame.worldYZ(),1000,100,150,name)
    beam = Beam(Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),1000,100,150,name)

    #Update mesh - Boolean the joints from Mesh
    beam.update_mesh() 

    #Save Beam to Json
    beam.to_json(os.path.join(tempfile.gettempdir(), "beam.json"),pretty=True)
    
    #Load saved Beam Object
    loaded_beam = Beam.from_json(os.path.join(tempfile.gettempdir(), "beam.json"))

    #Assert that the two beam objects are different objects
    assert (beam is not loaded_beam)

    print("Test 1: Comparing two beam data dictionary:")
    assert (beam.data == loaded_beam.data)
    if (beam.data == loaded_beam.data):
        print("Correct") 
    else:
        print("Incorrect")
    

    print(beam.frame)
    for i in range (4):
        print (beam.face_frame(i+1))
    
    #Test 2 : Beam with Joint data attached and saved and loaded.
    from Joint_90lap import Joint_90lap

    #Create some joints on the beam
    new_joint = Joint_90lap(180,1,50,100,100)
    beam.joints.append(new_joint) #Note that the position of the joint is dummy data.
    new_joint.update_joint_mesh(beam)
    beam.update_mesh()

    #Save Beam with the appended Joint to Json
    beam.to_json(os.path.join(tempfile.gettempdir(), "beam.json"),pretty=True)
    
    #Load the saved Beam
    loaded_beam = Beam.from_json(os.path.join(tempfile.gettempdir(), "beam.json"))

    print("Test 2: Comparing two beam data dictionary:")
    assert (beam.data == loaded_beam.data)
    if (beam.data == loaded_beam.data):
        print("Correct") 
    else:
        print("Incorrect")
    print (beam.data)