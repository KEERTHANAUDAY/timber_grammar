import compas 
from compas.geometry import Frame
from compas.geometry import Box 
from compas.datastructures import Mesh
from compas.rpc import Proxy
from compas.datastructures import mesh_subdivide_tri
trimesh = Proxy('trimesh')
#=====================================
#COMPAS geometry
#=====================================
box = Box(Frame.worldXY(), 500, 100, 100)
box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

f= Frame([250,-50,-50], [300,0,0], [0,100,0])
box_2 = Box(f, 100, 100, 200)
box_mesh_2 = Mesh.from_vertices_and_faces(box_2.vertices, box_2.faces)

#subdivision
# mesh_1 = mesh_subdivide_tri(box_mesh, k=1)
# mesh_2 = mesh_subdivide_tri(box_mesh_2, k=1)

#get list of vertices & faces
mesh_1_v = box_mesh.to_vertices_and_faces()[0]
mesh_1_f = box_mesh.to_vertices_and_faces()[1]

mesh_2_v = box_mesh_2.to_vertices_and_faces()[0]
mesh_2_f = box_mesh_2.to_vertices_and_faces()[1]
#=====================================
#trimesh proxy
#=====================================

#triangulate in trimesh

#T1 = trimesh.geometry.triangulate_quads(mesh_1p)
mesh_1p = trimesh.Trimesh(vertices=mesh_1_v, faces=mesh_1_f, process=False)
mesh_2p = trimesh.Trimesh(vertices=mesh_2_v, faces=mesh_2_f, process=False)

#with Proxy('trimesh') as trimesh:
  
a = mesh_1p.difference(mesh_2p, 'blender')
test = Mesh.from_vertices_and_faces(a.vertices, a.faces)
print(test)

    #a.export('test_compasgeo_proxy-3.stl') 
    

#if __name__ == "__main__":
  