import rhinoscriptsyntax as rc
import sys
my_path = 'C:\\Users\\ukeer\\timber_grammar'
sys.path.append(my_path)

import beam as bm
#import joints as J
from compas.geometry import Box
from compas.geometry import Frame
from compas_rhino.helpers import mesh_select_face
from compas_rhino.helpers import mesh_move_vertex
from compas_rhino.helpers import mesh_select_vertices
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist
from compas_rhino import select_points
from compas_rhino import get_point_coordinates
from compas.datastructures import Mesh
from compas.geometry import subtract_vectors
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import Transformation
from compas.datastructures import mesh_transform
reload(bm)

new_beam = Beam(Frame.worldXY(),3000,100,100)
new_beam.update_mesh()
artist = MeshArtist(mesh, layer='Beams_out_2')

artist.clear_layer()

artist.draw_vertices()

artist.draw_faces(join_faces=False)





#===============
#real test
#===============

#box = Box(Frame.worldXY(),3000,100,100)
#mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)
##select face
#face_id = mesh_select_face(mesh)#key of the mesh face
##select dist 
#dist = select_points()
#beam_in = bm.Beam(mesh, face_id, dist)

#==================
#test_code
#==================

#reload(J)
#box_2 = Box(Frame.worldXY(),1000,100,100)
#mesh_2 = Mesh.from_vertices_and_faces(box_2.vertices, box_2.faces)

##select face
#face_id = 5
#
##vertices_id
#vertices_id = mesh_2.face_vertices(face_id)
#print (vertices_id)
#
##vertices attributes
#vertices =[]
#for key in vertices_id:
#    a = mesh_2.vertex_coordinates(key)
#    vertices.append(a)
#print (vertices)
##
##vectors of face
##xaxis
#a_1 = vertices[0]
#x_v = vertices[1]
#n_1  = subtract_vectors(a_1, x_v)
#b_1 = add_vectors(a_1, scale_vector(n_1, 0.1))
##centroid
#a = mesh_2.face_centroid(face_id)
#n = mesh_2.face_normal(face_id)
#b = add_vectors(a, scale_vector(n, 100))
##yaxis 
#y_1 = vertices[1]
#y_2 = vertices[2]
#y_2 = subtract_vectors(y_1, y_2)
#y_3 = add_vectors(y_1, scale_vector(y_2, 2.5))
##newframe for new_beam
#pt = a
#v_1 = n_1
#v_2 = y_2
#new_beam_frame = Frame(pt, v_2, v_1)
#print(new_beam_frame)
#
##frame at point 
##select_dist of point for joint
#dist = select_points()
#pt = get_point_coordinates(dist)
#Frame_bool = Frame(pt[0], n_1, n )
##print(pt[0])
###frame to frame transformation 
##f1 = Frame([0, 0, 0], [1, 0, 0], [0, 0, 1])
##
#T = Transformation.from_frame_to_frame(new_beam_frame, Frame_bool)
#bool_mesh = mesh_transform(mesh_2, T)
##
##viz_normals
#lines = []
#
#lines.append({
#    'start' : a_1,
#    'end'   : b_1,
#    'arrow' : 'end',
#    'color' : (0, 255, 0)
#})
#lines.append({
#    'start' : a,
#    'end'   : b,
#    'arrow' : 'end',
#    'color' : (0, 255, 0)
#})
#lines.append({
#    'start' : y_1,
#    'end'   : y_3,
#    'arrow' : 'end',
#    'color' : (0, 255, 0)
#})
##
####===========================================
#####Visualize
#####===========================================
artist = MeshArtist(mesh, layer='Beams_out_2')
#artist_2 = MeshArtist(mesh_2, layer='Beams_out')
artist.clear_layer()
#artist_2.clear_layer()
artist.draw_vertices()
#artist_2.draw_vertices()
artist.draw_faces(join_faces=False)
#artist_2.draw_faces(join_faces=False)
##artist.draw_lines(lines)
#artist_2.draw_lines(lines)
