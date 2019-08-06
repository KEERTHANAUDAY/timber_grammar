import compas
from compas.geometry import Box
from compas.datastructures import Mesh
from compas.geometry import Frame
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist
from compas_rhino.utilities import select_points
from compas_rhino.utilities import get_point_coordinates
from compas.geometry import subtract_vectors

box=Box(Frame.worldXY(),500,100,100)
mesh_1 = Mesh.from_vertices_and_faces(box.vertices, box.faces)

f = Frame([250,-50,-50], [300,0,0], [0,100,0])
f2 = Frame([250,20,20], [300,0,100], [0,100,0])
box_2 = Box(f2,100,50,100)
mesh_2 = Mesh.from_vertices_and_faces(box_2.vertices, box_2.faces)
##get point for second beam
#guids = select_points()
#
#
##get vectors of constructed box
#vertices_id = mesh_1.face_vertices(1)
#f_vertices = [] #vertices of the selected face
#for key in vertices_id:
#    f_vertex = mesh_1.vertex_coordinates(key)
#    f_vertices.append(f_vertex)
#
##vector calculation
#f_v1 = f_vertices[0]
#f_v2 = f_vertices[1]
#xaxis_vec = subtract_vectors(f_v1, f_v2)
#
#f_c = mesh_1.face_centroid(1)
#yaxis_vec = mesh_1.face_normal(1)
#
##frame at self.dist
#pt = get_point_coordinates(guids)
#mesh_2_frame = Frame(pt[0], xaxis_vec, yaxis_vec)
#
#




#visualization
artist = MeshArtist(mesh_1, layer='Beams_out_2')

artist.draw_vertices()
artist.draw_faces(join_faces=True)

artist = MeshArtist(mesh_2, layer='Beams_out_2')
artist.draw_vertices()
artist.draw_faces(join_faces=True)