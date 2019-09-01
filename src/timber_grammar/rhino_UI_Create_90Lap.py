import rhinoscriptsyntax as rs
import Rhino 
import scriptcontext as sc

from assembly_model import Model
from Joint_90lap import Joint_90lap 
from Beam import Beam
from id_generator import create_id
from rhino_UI_utilities import UI_helpers

import compas
from compas.datastructures import Mesh
from compas.geometry import Translation
from compas_rhino.helpers import mesh_select_face
from compas_rhino.utilities import get_object_names
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist
from compas.geometry import Frame
from compas.geometry import distance_point_plane

import os
import math

__commandname__ = "Create_90Lap"

def RunCommand(is_interactive):
    """Interactive Rhino Command Creates 90 Lap joint on a seleceted Beam 

    Return:
    ------
    None
    """
    #load model
    model = Model.from_json("data.json")

    #Select mesh 
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
    helper = UI_helpers()
    joint_point = helper.Get_SelectPointOnMeshEdge("Select mesh edge","Pick point on edge")

    ext_a = rs.GetReal("extension_a up/left",None,None,None)
    ext_b = rs.GetReal("extension_b down/right",None,None,None)
    name = create_id() 
    

    #adding joints to selected Beam 
    model.rule_90lap (selected_beam,joint_point,face_id) 
     
    #create_match_beam with joint 
    model.match_beam(selected_beam,ext_a,ext_b,name,joint_point,face_id,helper.get_match_frame(face_id))

    #serialize data
    model.to_json("data.json", pretty = True)
    
    #Visualization 
    artist = MeshArtist(None, layer ='BEAM::Beams_out')
    artist.clear_layer()
    for beam in model.beams:
        artist = MeshArtist(beam.mesh, layer ='BEAM::Beams_out')#.mesh is not ideal fix in beam and assemble class
        artist.draw_faces(join_faces=True)


if __name__ == '__main__':
    RunCommand(True) 