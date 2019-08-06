import compas
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist

import os

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
FILE_I = os.path.join(DATA, 'compas_boolean_test_2.json')

mesh = Mesh.from_json(FILE_I)

artist = MeshArtist(mesh, layer='Beams_out_2')
artist.draw_vertices()
artist.draw_faces(join_faces=True)
