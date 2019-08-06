import compas 
from compas.datastructures import Mesh
from compas.geometry import Frame
from compas.geometry import Box 
import trimesh

#construct the mesh
box1 = Box(Frame.worldXY(),500,100,100)
box1 = Mesh.from_vertices_and_faces(box1.vertices, box1.faces)
box1 = box1.to_vertices_and_faces()

# box2 = Box(([250,-50,-50], [300,0,0], [0,100,0]), 100, 100, 200)
box2 = Box(([250,20,20], [300,0,100], [0,100,0]), 100, 50, 80)
box2 = Mesh.from_vertices_and_faces(box2.vertices, box2.faces)
box2 = box2.to_vertices_and_faces()

print('Compas Mesh 1 for Boolean')
print (box1)
print('Compas Mesh 2 for Boolean')
print (box2)

mesh_1 = trimesh.Trimesh(vertices=box1[0], faces=box1[1], process=False)
mesh_2 = trimesh.Trimesh(vertices=box2[0], faces=box2[1], process=False)

print('Trimesh Mesh 1 for Boolean')
print (mesh_1.vertices)
print (mesh_1.faces)
print('Trimesh Mesh 2 for Boolean')
print (mesh_2.vertices)
print (mesh_2.faces)

print('Trimesh Mesh 3 is Boolean Result')
mesh_3 = mesh_1.difference(mesh_2,'blender')
print (mesh_3.vertices)
print (mesh_3.faces)






