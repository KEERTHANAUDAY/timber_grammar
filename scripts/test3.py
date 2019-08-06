import compas
from compas.geometry import Frame
from compas.geometry import Box 
from compas.datastructures import Mesh
from compas.rpc import Proxy

#import Trimesh_proxy
import Fruit

#construct the mesh
box = Box(Frame.worldXY(),500,100,100)
box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

box_2 = Box(([250,20,20], [300,0,100], [0,100,0]), 100, 50, 80)
box_mesh_2 = Mesh.from_vertices_and_faces(box_2.vertices, box_2.faces)

#call function
with Proxy(package='Fruit') as f:
    result = f.apple.trimesh_subtract(box_mesh, box_mesh_2)

#result = Fruit.apple.trimesh_subtract(box_mesh, box_mesh_2)
print (Fruit.apple.add(2,8))

# print(type(result))
# print(result)
# result.to_json(FILE_O, pretty=True)