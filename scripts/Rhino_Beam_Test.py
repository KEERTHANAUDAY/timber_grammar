import compas
print (compas.__version__)
import sys
print (sys.version)


from compas.geometry import Frame
from compas.geometry import Box 
from compas.datastructures import Mesh
from compas.rpc import Proxy

#construct the mesh
box = Box(Frame.worldXY(),500,100,100)
box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

box_2 = Box(([250,20,20], [300,0,100], [0,100,0]), 100, 50, 80)
box_mesh_2 = Mesh.from_vertices_and_faces(box_2.vertices, box_2.faces)

#call function

with Proxy('Trimesh_proxy') as t:
    result = t.Trimesh_proxy.subtract(box_mesh, box_mesh_2)
print(type(result))
print(result)