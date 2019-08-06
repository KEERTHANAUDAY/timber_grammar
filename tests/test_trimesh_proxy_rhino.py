import compas
from compas.geometry import Frame
from compas.geometry import Box 
from compas.datastructures import Mesh
from compas.rpc import Proxy

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist

import os

#construct the mesh
box = Box(Frame.worldXY(),500,100,100)
box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

box_2 = Box(([250,20,20], [300,0,100], [0,100,0]), 100, 50, 80)
box_mesh_2 = Mesh.from_vertices_and_faces(box_2.vertices, box_2.faces)

#call function
python_exe_path = 'C:\ProgramData\Anaconda3\envs\compas_assembly\python.exe'
import sys
python_exe_path = sys.executable

with Proxy(package='Trimesh_proxy',python=python_exe_path) as f:
    result = f.trimesh_subtract(box_mesh, box_mesh_2)
    result_mesh = Mesh.from_data(result['value'])

# print (result_mesh)


# import os
# HERE = os.path.dirname(_file_)
# DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
# FILE_O = os.path.join(DATA, 'compas_boolean_test_2.json')
# result.to_json(FILE_O, pretty=True)


# mesh = Mesh.from_json(FILE_I)

artist = MeshArtist(result_mesh, layer='Layer1')
artist.draw_vertices()
artist.draw_faces(join_faces=True)