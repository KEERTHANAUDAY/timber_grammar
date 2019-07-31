import compas 
from compas.datastructures import Mesh
from compas.rpc import Proxy
t = Proxy('trimesh')

class Trimesh_proxy_subtract(object):
    """
    this class performs a boolean difference of input meshes
    """
    def __init__(self, beam_mesh, joint_mesh):

        """
        :param beam_mesh:   compas Mesh of beam
        :param joint_mesh:  compas Mesh of joint
        """
        self.beam_mesh = beam_mesh
        self.joint_mesh = joint_mesh
        self.mesh = None

        #Perform initial calculation of the mesh (except when this is an empty object)
        if beam_mesh is not None:  
            self.update_boolean()
        
    def update_boolean(self):
        """Compute the boolean difference operation through trimesh.

        Returns
        -------
        object
            A compas.Mesh

        Note
        ____
        The beam_mesh is updated with the new mesh
        """

        #constructing Trimesh from compas mesh
        mesh1_v = self.beam_mesh.to_vertices_and_faces()[0]
        mesh1_f = self.beam_mesh.to_vertices_and_faces()[1]  

        mesh2_v = self.joint_mesh.to_vertices_and_faces()[0]
        mesh2_f = self.joint_mesh.to_vertices_and_faces()[1]

        mesh_1 = t.Trimesh(vertices=mesh1_v, faces=mesh1_f, process=False)
        mesh_2 = t.Trimesh(vertices=mesh2_v, faces=mesh2_f, process=False)

        boolean_sub = mesh_1.difference(mesh_2,'blender')
        boolean_mesh = Mesh.from_vertices_and_faces(boolean_sub.vertices, boolean_sub.faces)
        self.mesh = boolean_mesh
        


if __name__ == '__main__':
    import compas 
    from compas.geometry import Frame
    from compas.geometry import Box 
    from compas.datastructures import Mesh
 
    #construct the box
    box = Box(Frame.worldXY(),500,100,100)
    box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)
    box_2 = Box(([250,-50,-50], [300,0,0], [0,100,0]), 100, 100, 200)
    box_mesh_2 = Mesh.from_vertices_and_faces(box_2.vertices, box_2.faces)

    mesh = Trimesh_proxy_subtract(box_mesh, box_mesh_2)
    a = mesh.mesh
    print(type(mesh))


        
