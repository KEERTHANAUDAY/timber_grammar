
import math
import compas
from compas.geometry import Box
from compas.datastructures import Mesh
from compas.datastructures import mesh_bounding_box
from id_generator import create_id
from Joint import Joint
import json

from compas.rpc import Proxy
import sys
python_exe_path = sys.executable

class Beam():
    """ Beam class containing its size and connecting dowels
    """

    def __init__(self, frame, length, width, height,name):
        """ initialization

            :frame:           base plane for the beam 
            :length:          the length along the local x-axis (Typically the long side)
            :width:           the length along the local z-axis (Short Side of Side 1 and Side 3)
            :height:          the length along the local y-axis (Short Side of Side 2 and Side 4)
            
        """
        self.frame = frame
        self.length = length 
        self.width = width
        self.height = height 
        self.name = name
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
        * 'name'            => UUID for very instance
        """
        data = {
            'type'      : self.__class__.__name__, #Keep this line for deserialization
            'frame'     : None if (self.frame is None) else self.frame.to_data(),
            'length'    : self.length,
            'width'     : self.width,
            'height'    : self.height,
            'name'      : self.name,
            'mesh'      : None if (self.mesh is None) else self.mesh.to_data(),
            'joints'    : [joint.to_data() for joint in self.joints]
            }
        return data
    
    @data.setter
    def data(self, data):
        self.frame      = None if data.get('frame') is None else compas.geometry.Frame.from_data(data.get('frame')) or None
        self.face_id    = data.get('face_id') or None
        self.depth      = data.get('depth') or None
        self.width      = data.get('width') or None
        self.height     = data.get('height') or None
        self.name       = data.get('name') or None
        self.mesh       = None if data.get('mesh') is None else compas.datastructures.Mesh.from_data(data.get('mesh')) or None
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
        with open(filepath, 'r') as fp:
            data = json.load(fp)

        assert data['type'] ==  cls.__name__ , "Deserialized object type: %s is not equal to %s." % (data['type'] , cls.__name__)
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
            self.mesh =self.trimesh_proxy_subtract(self.mesh,joint.mesh)
        return self.mesh

    
    def draw_uncut_mesh(self):
        '''Computes and returns the beam geometry with boolean difference of all joints.

        Returns
        -------
        compas.datastructures.Mesh
        The beam mesh without joint geoemtry

        '''
        box = Box(self.frame, self.length,self.width,self.height)
        box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces) 
        return box_mesh

    def trimesh_proxy_subtract(mesh_a,mesh_b):
        with Proxy(package='Trimesh_proxy',python=python_exe_path) as f:
            result = f.trimesh_subtract(mesh_a.mesh, mesh_b.mesh)
            result_mesh = Mesh.from_data(result['value'])
        return result_mesh

        
if __name__ == '__main__':
    #test for data
    import compas
    from compas.datastructures import Mesh
    from compas.geometry._primitives import Frame
    from compas.geometry._primitives.box import Box
    from Joint_90lap import Joint_90lap
    from id_generator import create_id

    name = create_id()

    #Create Beam object
    beam = Beam(Frame.worldXY(),1000,100,150,name)
    # instance check
    test_1 = Beam(None, None, None, None, )
    test_1.joints.append(Joint_90lap(joint_frame,3,50,100,100))
    #Create some joints on the beam
    from Joint_90lap import Joint_90lap 
    from compas.geometry._primitives import Frame
    beam.joints.append(Joint_90lap(Frame.worldXY(),1,50,100,100)) #Note that the position of the joint is dummy data.
    from compas.geometry import Translation
    joint_frame = beam.frame.transformed(Translation([200,0,0]))
    beam.joints.append(Joint_90lap(joint_frame,3,50,100,100)) #Note that the position of the joint is dummy data.
    
    #Save Beam to Json
    print(beam)
    print(beam.data)
    beam.to_json("test.json",pretty=True)

    #Load saved Beam Object
    loaded_beam = Beam.from_json("test.json")
    print(loaded_beam)
    print(loaded_beam.data)
    beam.to_json("test2.json",pretty=True)
