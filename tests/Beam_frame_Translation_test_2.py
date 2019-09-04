import compas

from compas.geometry import Box
from compas.geometry import Frame
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist

mesh = []
#build mesh
frame=Frame.worldXY()
box = Box(frame,500,100,100)
mesh.append(Mesh.from_vertices_and_faces(box.vertices, box.faces))

#build mesh translation
new_frame = Frame(frame.point, frame.normal, (frame.yaxis*-1))
box_2 = Box(new_frame,500,100,100)
mesh.append(Mesh.from_vertices_and_faces(box_2.vertices, box_2.faces))

#visualization
artist = MeshArtist(None, layer='Beams_out')
artist.clear_layer()
for m in mesh:
    artist = MeshArtist(m, layer='Beams_out')
    artist.draw_faces(join_faces=True)