import compas
from compas.geometry import Box
from compas.geometry import Frame
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist
from compas_rhino.helpers import mesh_select_face
from compas.geometry import Vector
from compas.geometry import Translation
from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
import rhinoscriptsyntax as rs
import Rhino

#    joint_frame = beam.frame.transformed(Translation([200,0,0]))
def Get_PointOnCurve(msg):
    #gets Mesh edge
    go = Rhino.Input.Custom.GetObject()
    go.SetCommandPrompt(msg)
    go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshEdge
    go.SubObjectSelect = True
    go.GroupSelect = False
    if go.Get()!=Rhino.Input.GetResult.Object: return
    objref = go.Object(0)
    point = objref.SelectionPoint()
    go.Dispose()
    return point

def Get_PointDistanceFromOriginFace(mesh,box,pts_toproject):

    dir_vec = box.frame.xaxis 
    ray = Rhino.Geometry.Ray3d(pts_toproject, dir_vec)
    lineLength = Rhino.Geometry.Intersect.Intersection.MeshRay(mesh,ray)
    if lineLength >= 0:
        distance = lineLength
    return distance
    
    
meshes = []
box = Box(Frame.worldXY(),100,50,100)
mesh1 = Mesh.from_vertices_and_faces(box.vertices, box.faces)
meshes.append(mesh1)
print(box.frame)

#This is the logic for a robust 
side_4 = Frame.worldXY()
side_1 = Frame(add_vectors((box.frame.point),(0,box.zsize,0)),box.frame.xaxis, box.frame.normal)
side_2 = Frame(subtract_vectors((side_1.point),(0,box.ysize,0)), box.frame.xaxis, box.frame.yaxis)
side_3 = Frame(add_vectors((side_1.point),(0,0,(box.zsize/2))),box.frame.xaxis, box.frame.zaxis)

#side_2 test
box2 = Box(side_1,100,50,100)
mesh2 = Mesh.from_vertices_and_faces(box2.vertices, box2.faces)
meshes.append(mesh2)

#side_3 test
box3 = Box(side_2,100,50,100)
mesh3 = Mesh.from_vertices_and_faces(box3.vertices, box3.faces)
meshes.append(mesh3)

#side_4 test
box4 = Box(side_3,100,50,100)
mesh4 = Mesh.from_vertices_and_faces(box4.vertices, box4.faces)
meshes.append(mesh4)

####tests for point projection 
test = Get_PointOnCurve("select point")
Obj_ref = rs.GetObject(message = "select mesh(es)", filter = 32, preselect = False, subobjects = True)
mesh_test = rs.coercemesh(Obj_ref)
print(test)

dir_vec = Rhino.Geometry.Vector3d(box.frame.xaxis.x,box.frame.xaxis.y,box.frame.xaxis.z)
print(type(dir_vec))
ray = Rhino.Geometry.Ray3d(test, dir_vec) #needs to be fed as rhino vector
lineLength = Rhino.Geometry.Intersect.Intersection.MeshRay(mesh_test,ray)
print(test)
#
#
###artist = MeshArtist(None, layer='Beams_out')
###artist.clear_layer()
###for mesh in meshes:
##artist = MeshArtist(mesh1, layer='Beams_out')
##artist.clear_layer()
##artist.draw_faces(join_faces=True)
##

