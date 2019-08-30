
import math
import compas
from compas.datastructures import Mesh
from compas.geometry import Box
from Joint import Joint

class Joint_90lap(Joint):
    """
    joint class containing varied joints
    """
    def __init__(self, frame,face_id, length, width, height):

        """
        :param fame:      plane of boolean geometry
        :param length:   length of boolean geometry
        :param width:     width of boolean geometry
        :param height:     height of boolean geometry
        """
        self.frame = frame
        self.face_id = face_id
        self.length = length
        self.width = width 
        self.height = height
        self.mesh = None

        #Perform initial calculation of the mesh (except when this is an empty object)
        if frame is not None:  
            self.update_joint_mesh()

            
    @property
    def data(self):
        """dict : A data dict representing all internal persistant data for serialisation.
        The dict has the following structure:
        * 'type'            => string (name of the class)
        * 'frame'           => dict of compas.frame.to_data()
        * 'face_id'         => int
        * 'length'           => double
        * 'width'           => double
        * 'height'          => double
        * 'mesh'            => dict of compas.mesh.to_data()
        """
        data = {
            'type'      : self.__class__.__name__, #Keep this line for deserialization
            'frame'     : None,
            'face_id'   : self.face_id,
            'length'     : self.length,
            'width'     : self.width,
            'height'    : self.height,
            'mesh'      : None,
            }
        if (self.frame is not None):
            data['frame'] = self.frame.to_data()
        if (self.mesh is not None) :
            data['mesh'] = self.mesh.to_data()
        return data
    
    @data.setter
    def data(self, data):
        self.frame      = None 
        if (data.get('frame') is not None): self.frame = compas.geometry.Frame.from_data(data.get('frame')) 
        self.face_id    = data.get('face_id') or None
        self.length      = data.get('length') or None
        self.width      = data.get('width') or None
        self.height     = data.get('height') or None
        self.mesh       = None 
        if (data.get('mesh') is not None): self.mesh = compas.datastructures.Mesh.from_data(data.get('mesh'))

    @classmethod
    def from_data(cls,data):
        new_object = cls(None,None,None,None,None) # Only this line needs to be updated
        new_object.data = data
        if new_object.mesh is None:
            new_object.update_joint_mesh()
        return new_object
   
    def update_joint_mesh(self):
        """Compute the negative mesh volume of the joint.

        Returns
        -------
        object
            A compas.Mesh

        Note
        ----
        The self.mesh is updated with the new mesh

        """
        box = Box(self.frame, self.length, self.width, self.height)
        box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces) 
        self.mesh = box_mesh
        return box_mesh
    
         
if __name__ == "__main__":

    #Test to create Joint_90lap object. Serialize and deserialize.
    #j.data and q.data should have the same value
    
    from compas.geometry._primitives import Frame
    j = Joint_90lap(Frame.worldXY(),1,50,100,100)
    print (j.data)
    j.to_json("test.json", pretty= True)
    q = Joint_90lap.from_json("test.json")
    print (q.data)




