__all__ = ['trimesh_subtract']

def trimesh_subtract(c_mesh1,c_mesh2):
    import compas
    from compas.datastructures import Mesh
    import trimesh
    assert isinstance(c_mesh1,Mesh)
    assert isinstance(c_mesh2,Mesh)
    
    mesh1_v = c_mesh1.to_vertices_and_faces()[0]
    mesh1_f = c_mesh1.to_vertices_and_faces()[1]  

    mesh2_v = c_mesh2.to_vertices_and_faces()[0]
    mesh2_f = c_mesh2.to_vertices_and_faces()[1]

    mesh_1 = trimesh.Trimesh(vertices=mesh1_v, faces=mesh1_f, process=False)
    mesh_2 = trimesh.Trimesh(vertices=mesh2_v, faces=mesh2_f, process=False)
    
    #print(mesh_1.vertices)
    #print(mesh_2.vertices)
    boolean_sub = mesh_1.difference(mesh_2,engine='scad')
    #print(boolean_sub.vertices)

    
    result_compas_mesh = Mesh.from_vertices_and_faces(boolean_sub.vertices, boolean_sub.faces)
    return result_compas_mesh


if __name__ == '__main__':

    import compas
    from compas.geometry import Frame
    from compas.geometry import Box 
    from compas.datastructures import Mesh

    #construct the mesh
    box = Box(Frame.worldXY(),500,100,100)
    box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

    box_2 = Box(([250,20,20], [300,0,100], [0,100,0]), 100, 50, 80)
    box_mesh_2 = Mesh.from_vertices_and_faces(box_2.vertices, box_2.faces)

    print(trimesh_subtract(box_mesh, box_mesh_2))


