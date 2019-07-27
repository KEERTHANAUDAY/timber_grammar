import compas
from compas.datastructures import Mesh
import os
import compas_rhino
from compas_rhino.helpers import mesh_from_guid

#exporting file 
HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
FILE_O = os.path.join(DATA, 'test.json')

#select mesh 
guid = compas_rhino.select_mesh()
test_mesh = mesh_from_guid(Mesh, guid)

#save file
test_mesh.to_json(FILE_O, pretty=True)