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

__commandname__ = "Create_90Lap"

def Get_PointOnCurve(msg):
    #gets Mesh edge
    go = Rhino.Input.Custom.GetObject()
    go.SetCommandPrompt(msg)
    go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshEdge
    go.SubObjectSelect = True
    go.GroupSelect = False
    go.AcceptNothing(False)
    if go.Get()!=Rhino.Input.GetResult.Object: return
    objref = go.Object(0)
    point = objref.SelectionPoint()
    go.Dispose()
    return point

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
    model = Model()
    load = model.from_json("check_3.json")

    #select beambrhino way
    Obj_ref = rs.GetObject(message = "select mesh(es)", filter = 32, preselect = False, subobjects = True)
    Object_name = rs.ObjectName(Obj_ref)
    test = Object_name[:-5]
    
    #select face & point(face needs to be implemented through UI)
    face_id = rs.GetInteger("face_id",1,None,None)
    joint_pt = Get_PointOnCurve("Select joint position")
    
    #Match beam extension 
    extension = rs.GetReal("Enter Extension Length(Real)",200,None,None)
   
    #finding iteration
    data_dict = []
    for key,value in load.data.items():
        if key == 'beams':
           for dict in value:
             for key,value in dict.items():
                if value == test:
                    print(value)
                    print(test)
                    data_dict.append(dict)
    for i in range(len(data_dict)):
        if i>1:
            BeamRef = Beam.from_data(data_dict[-1]) #this is the beam
        else:
            BeamRef = Beam.from_data(data_dict[0])
                       
                    

    #finding information from dict optimize this 
    for key,value in BeamRef.data.items():
        if key == 'frame':
            for key,value in value.items():
                    if key == 'yaxis':
                        y = value
                        print(y)
                    elif key == 'xaxis':
                        x = value
  
    #90_lap boolean from assembly model
    m_beam = Model()
    joint_frame = Frame(joint_pt, x, y)
    beam_90_lap = m_beam.rule_90lap(BeamRef,joint_frame,1)
    
    #Creating Match beam 
    frame1 = Frame(joint_pt, x, y)
    frame2 = Frame(joint_pt, x, y)
    #translate frame position
    match_beam_joint_fame = frame2.transformed(Translation([0,50,0]))
    match_beam_frame = frame1.transformed(Translation([0,0,-(BeamRef.length+extension)/2]))
    test = m_beam.create_beam(match_beam_frame,BeamRef.width,(BeamRef.height),(BeamRef.length+extension),create_id())
    #Match beam boolean 
    matchbeam_90_lap = m_beam.rule_90lap(test,match_beam_joint_fame,1)
    print(test)

    #serialize data
    m_beam.to_json("check_3.json", pretty = True)

    #test visualizations
    artist = MeshArtist(beam_90_lap, layer ='BEAM::CreateJointGeo')#.mesh is not ideal fix in beam and assemble class
    artist.clear_layer()
    artist.draw_faces(join_faces=True)
    artist.redraw()

    artist2 = MeshArtist(matchbeam_90_lap, layer ='BEAM::CreatMatchBeam')#.mesh is not ideal fix in beam and assemble class
#    artist2.clear_layer()
    artist2.draw_faces(join_faces=True)
    artist2.redraw()



if __name__ == '__main__':
    RunCommand(True)    