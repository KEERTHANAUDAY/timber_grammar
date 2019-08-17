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
from compas_rhino.selectors import FaceSelector
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
    load = Model.from_json("create_beam.json")
#    print(load.data)

#    #select beambrhino way
    Obj_ref = rs.GetObject(message = "select mesh(es)", filter = 32, preselect = False, subobjects = True)
    Object_name = rs.ObjectName(Obj_ref)
    
    #select face & point(face needs to be implemented through UI)
    face_id = rs.GetInteger("face_id",1,None,None)
    joint_pt = Get_PointOnCurve("Select joint position")
    print(joint_pt)
    
#    Object_mesh = rs.coercemesh(Obj_ref)
#    Object_index = Object_mesh.ComponentIndex()

#    #select beam_compasway
#    Object_Id = select_meshes()
#    Object_name = get_object_names(Object_Id)
#    Object_mesh = mesh_from_guid(Mesh,Object_Id)
#    face = FaceSelector.select_face(Object_mesh)
#    print(face)
##
##    print(Object_index)#don't know name.mesh format is followed, needs to be fixed 
##    
#    #finding iteration
#    for key,value in load.data.items():
#        if key == 'beams':
#            for dict in value:
#                for key,value in dict.items():
#                    if key == 'name':#this line needs to be changed to compair the guid.objectname and name 
#                        test_data = dict
#    beam_from_list = Beam.from_data(test_data)
#    beam_mesh_from_list = beam_from_list.mesh                      
#
#    Object_index = Object_mesh.ComponentIndex()
##
##    Rhino.DocObjects.RhinoObject.SelectSubObject
##    Sub_select = Object_Id.SelectSubObject(Object_index,True,True)
##    test = Object_Id.SelectSubObject(Object_index,True,True)
##    print(Sub_select)





if __name__ == '__main__':
    RunCommand(True)    