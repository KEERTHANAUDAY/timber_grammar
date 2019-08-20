import rhinoscriptsyntax as rs
import Rhino 
import scriptcontext as sc

from assembly_model import Model
import compas
from compas.datastructures import Mesh
from compas.geometry import Translation
from compas_rhino.helpers import mesh_select_face
from compas_rhino.utilities import select_meshes
from compas_rhino.utilities import get_object_names
from compas_rhino.helpers import mesh_from_guid
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist
from compas.geometry import Frame
from Joint_90lap import Joint_90lap 
from Beam import Beam
from id_generator import create_id
import os
import math

__commandname__ = "Create_90Lap"

def Get_SelectPointOnMeshEdge(message_0,message_1):
    #gets Mesh edge
    go = Rhino.Input.Custom.GetObject()
    go.SetCommandPrompt(message_0)
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
    gp.SetCommandPrompt(message_1)
    gp.Constrain(edge_line)
    get_rc = gp.Get()
    placed_point = rs.coerce3dpoint(sc.doc.Objects.AddPoint(gp.Point()))
    sc.doc.Views.Redraw()
    #The distance brom edgeline[0] to pickedpoint is calcuated here 
    distance = math.sqrt((placed_point.X - edge_point.X)**2 + (placed_point.Y - edge_point.Y)**2 + (placed_point.Z - edge_point.Z)**2)
    return distance 
    
def selectmeshface():
    go = Rhino.Input.Custom.GetObject()
    go.GeometryFilter=Rhino.DocObjects.ObjectType.MeshFace
    go.SetCommandPrompt("Get mesh Face")
    go.Get()
    objref=go.Object(0)
    face_guid = objref.ObjectId
    go.Dispose()
    return face_guid 

def RunCommand(is_interactive):
    #load model
    model = Model.from_json("test_18.json")

    #select beambrhino way
    Obj_ref = rs.GetObject(message = "select mesh(es)", filter = 32, preselect = False, subobjects = True)
    selected_beam_name = (rs.ObjectName(Obj_ref)[:-5])
    #Loop through all beams in model to identify the selected beam
    selected_beam = None
    for beam in model.beams:
        if(beam.name == selected_beam_name):
            selected_beam = beam
            break
    assert (selected_beam != None)

    #list of user inputs(face needs to be implemented through UI)
    face_id = rs.GetInteger("face_id",None,0,5)
    joint_dist = Get_SelectPointOnMeshEdge("Select mesh edge","Pick point on edge")
    extension = rs.GetReal("Enter Extension Length up/left",100,None,None)
    extension = rs.GetReal("Enter Extension Length down/right",100,None,None)

    #create_match_beam # has to be derived from beam frame
    # match_beam_frame = Frame(joint_pt,selected_beam.frame.xaxis, selected_beam.frame.yaxis)
    # match_beam_frame_T = match_beam_frame.transformed(Translation([0,0,-(selected_beam.length+extension)/2]))
    # match_beam = model.create_beam(match_beam_frame_T,selected_beam.width,selected_beam.height,selected_beam.length,create_id())

    #adding joints

    model.rule_90lap(selected_beam,joint_dist,face_id)
    # model.rule_90lap(match_beam,joint_pt,3)

    #serialize data
    model.to_json("test_18.json", pretty = True)
  
    artist = MeshArtist(None, layer ='BEAM::Beams_out')
    artist.clear_layer()
    for beam in model.beams:
        #test visualizations
        print(beam.name)
        artist = MeshArtist(beam.mesh, layer ='BEAM::Beams_out')#.mesh is not ideal fix in beam and assemble class
        artist.draw_faces(join_faces=True)
        artist.draw_vertices()

if __name__ == '__main__':
    RunCommand(True) 