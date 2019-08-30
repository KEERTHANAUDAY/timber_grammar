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
from Rhino.Commands import *
from Rhino.Geometry import *
from Rhino.Geometry.Intersect import *
from Rhino.Input import *
from Rhino.DocObjects import *
from scriptcontext import doc
from System.Collections.Generic import *
import scriptcontext as sc
import math

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

def Get_PointOnMeshEdge(msg0,msg1):
    #gets Mesh edge
    go = Rhino.Input.Custom.GetObject()
    go.SetCommandPrompt(msg0)
    go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshEdge
    go.SubObjectSelect = True
    go.GroupSelect = False
    go.AcceptNothing(True)
    if go.Get()!= Rhino.Input.GetResult.Object: return
    objref = go.Object(0)
    #get edge index
    index=objref.GeometryComponentIndex.Index
    #get mesh parent
    mesh=objref.Mesh()
    #get line representing mesh edge
    edge_line=mesh.TopologyEdges.EdgeLine(index)
    edge_point = edge_line[0]
    print(type(edge_point.X))
    #start a get point constrained to edge line
    gp = Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt(msg1)
    gp.Constrain(edge_line)
    get_rc = gp.Get()
    placed_point = rs.coerce3dpoint(sc.doc.Objects.AddPoint(gp.Point()))
    sc.doc.Views.Redraw()
    #The distance brom edgeline[0] to pickedpoint is calcuated here 
    distance = math.sqrt((placed_point.X - edge_point.X)**2 + (placed_point.Y - edge_point.Y)**2 + (placed_point.Z - edge_point.Z)**2)
    return distance 
    




point =Get_PointOnMeshEdge("Select mesh edge","Pick point on edge")
print(point)
print(type(point))
 
#
#    prj_points, indices = Intersection.ProjectPointsToMeshesEx({mesh}, point, Vector3d(1, 0, 0), 0)
#    for prj_pt in prj_points:
#        out = doc.Objects.AddPoint(prj_pt)
#    doc.Views.Redraw()
#    return out
#
#
#test_1 = test()
#print(type(test_1))


#
#
###artist = MeshArtist(None, layer='Beams_out')
###artist.clear_layer()
###for mesh in meshes:
##artist = MeshArtist(mesh1, layer='Beams_out')
##artist.clear_layer()
##artist.draw_faces(join_faces=True)
##

