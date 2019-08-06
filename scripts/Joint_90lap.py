import math
import compas
from compas.datastructures import Mesh
from compas.geometry import Box
from Joint import Joint

class Joint_90lap(Joint):
    """
    joint_90lap class creates 90degree lap joint
    """
    def __init__(self, frame, face_id, depth, width, height):

        """
        :param fame:      plane of boolean geometry
        :param depth:   depth of boolean geometry
        :param width:     width of boolean geometry
        :param height:     height of boolean geometry
        """
        self.frame = frame
        self.face_id = face_id
        self.depth = depth
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
        * 'depth'           => double
        * 'width'           => double
        * 'height'          => double
        * 'mesh'            => dict of compas.mesh.to_data()
        """
        data = {
            'type'      : self.__class__.__name__, #Keep this line for deserialization
            'frame'     : None if (self.frame is None) else self.frame.to_data(),
            'face_id'   : self.face_id,
            'depth'     : self.depth,
            'width'     : self.width,
            'height'    : self.height,
            'mesh'      : None if (self.mesh is None) else self.mesh.to_data(),
            }
        return data
    
    @data.setter
    def data(self, data):
        self.frame      = None if data.get('frame') is None else compas.geometry.Frame.from_data(data.get('frame')) or None
        self.face_id    = data.get('face_id') or None
        self.depth      = data.get('depth') or None
        self.width      = data.get('width') or None
        self.height     = data.get('height') or None
        self.mesh       = None if data.get('mesh') is None else compas.datastructures.Mesh.from_data(data.get('mesh')) or None
    
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
        box = Box(self.frame, self.width,self.height,self.depth)
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




