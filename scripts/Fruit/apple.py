
__all__ = ['add','trimesh_subtract']

def add(x,y):
    return x + y

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
    
    boolean_sub = mesh_1.difference(mesh_2,'blender')
    result_compas_mesh = Mesh.from_vertices_and_faces(boolean_sub.vertices, boolean_sub.faces)
    return result_compas_mesh