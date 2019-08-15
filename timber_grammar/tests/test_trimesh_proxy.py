import compas 
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

python_exe_path = 'C:\ProgramData\Anaconda3\envs\compas_assembly\python.exe'
import sys
python_exe_path = sys.executable

# with Proxy('Trimesh_proxy',python=python_exe_path) as t:
with Proxy('timber_grammar.Trimesh_proxy',python=python_exe_path) as t:
    result = Mesh.from_data(t.trimesh_subtract(box_mesh, box_mesh_2)['value'])

print (result)


# exporting file 
# import os
# HERE = os.path.dirname(__file__)
# DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
# FILE_O = os.path.join(DATA, 'compas_boolean_test.json')
# result.to_json('FILE_O', pretty=True)