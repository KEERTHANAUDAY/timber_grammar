import rhinoscriptsyntax as rs
import Rhino 
import scriptcontext as sc

from assembly_model import Model
import compas
from compas.datastructures import Mesh
from compas_rhino.helpers import mesh_select_face
from compas_rhino.utilities import select_meshes
from compas_rhino.utilities import get_object_names
from compas_rhino.helpers import mesh_from_guid
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist
from compas.geometry import Frame
from Joint_90lap import Joint_90lap 
from Beam import Beam
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
    load = model.from_json("check_1.json")
#    print(load.data)

    #select beambrhino way
    Obj_ref = rs.GetObject(message = "select mesh(es)", filter = 32, preselect = False, subobjects = True)
    Object_name = rs.ObjectName(Obj_ref)
    
    #select face & point(face needs to be implemented through UI)
    face_id = rs.GetInteger("face_id",1,None,None)
    joint_pt = Get_PointOnCurve("Select joint position")
#    print(joint_pt)
   
    #finding iteration
    for key,value in load.data.items():
        if key == 'beams':
            for dict in value:
                for key,value in dict.items():
                    if key == 'name':#this line needs to be changed to compair the guid.objectname and name 
                        test_data = dict
    beam_from_list = Beam.from_data(test_data)#this is the beam
#    print(type(beam_from_list))

    #finding information from dict optimize this 
    for key,value in beam_from_list.data.items():
        if key == 'frame':
            for key,value in value.items():
                    if key == 'yaxis':
                        y = value
                    elif key == 'xaxis':
                        x = value
    
#    print(type(beam_from_list))
    print(beam_from_list.data)
    
    #create joint frame here
    joint_frame = Frame([145,0,0], x, y)
    
    #90_lap boolean from assembly model
    test = Model()
    beam_90_lap = test.rule_90lap(beam_from_list,joint_frame,1)
    
    test.to_json("check_1.json", pretty = True)
  
#     test.create_beam(Frame.worldXY(),500,500,500,456)
#    test.to_json("create_beam_10.json", pretty = True)
#    
    
    
    
    
    
    
    
    
    
    #serialize data
#    print(model)
#    beam_90_lap.to_json("create_beam_3.json", pretty = True)
    
    #this is just a test has to be implemented in assembly
    #model to perform multiple booleans 
#    joint =beam_from_list.joints.append( Joint_90lap(joint_frame,1,100,100,50))
#    test = beam_from_list.update_mesh()
#    print(test)
#    save = beam_from_list.to_json("create_beam.json",pretty=True)
#     


#
    #test visualizations
    artist = MeshArtist(beam_90_lap, layer ='BEAM::CreateJointGeo')#.mesh is not ideal fix in beam and assemble class
    artist.clear_layer()
    artist.draw_faces(join_faces=True)
    artist.redraw()



if __name__ == '__main__':
    RunCommand(True)    