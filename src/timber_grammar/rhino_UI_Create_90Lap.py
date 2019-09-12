
import rhinoscriptsyntax as rs
import Rhino 
import scriptcontext as sc

from assembly_model import Model
from Derivation import Derivation
from Beam import Beam
from Joint_90lap import Joint_90lap 

from id_generator import create_id
from rhino_UI_utilities import UI_helpers
import rhino_UI_utilities

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

def Get_distancefromBeamYZFrame(BeamRef,placed_point):
        """Computes the distance from selected point to Beam YZ_Plane(face_id = 0)
        Parameters:
        ----------
        BeamRef: Beam Object
        placed_point: Point3d
        Return:
        ------
        distance (double)
        """
        YZ_Plane = BeamRef.face_plane(0)
        dist = distance_point_plane(placed_point,YZ_Plane)
        return dist

def RunCommand(is_interactive):
    """Interactive Rhino Command Creates 90 Lap joint on a seleceted Beam 

    Return:
    ------
    None
    """
    #load Derivation and model
    derivation = Derivation.from_json(rhino_UI_utilities.get_json_file_location())
    model = derivation.get_next_step()

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

    ext_start = rs.GetReal("extension start ",200,None,None)
    ext_end = rs.GetReal("extension end ",200,None,None)
    name = create_id() 
    
    #adding joints to selected Beam 
    #joint_distance_from_start = Get_distancefromBeamYZFrame(selected_beam,joint_point)
    joint_distance_from_start = selected_beam.Get_distancefromBeamYZFrame(joint_point)
    match_beam_origin =  model.rule_90lap(selected_beam,joint_distance_from_start,face_id,ext_start,ext_end,name) 
     


    #Save Derivation (Model is also saved)
    derivation.to_json(rhino_UI_utilities.get_json_file_location(), pretty = True)

    #Visualization
    viz_point = []
    for pt in match_beam_origin:
        a = (pt[0],pt[1],pt[2])
        viz_point.append({
            'pos': a,
            'color': (0,255,0)
        })


    #Visualization 
    artist = MeshArtist(None, layer ='BEAM::Beams_out')
    artist.clear_layer()
    artist.draw_points(viz_point)
    for beam in model.beams:
        artist = MeshArtist(beam.mesh, layer ='BEAM::Beams_out')#.mesh is not ideal fix in beam and assemble class
        artist.draw_faces(join_faces=True)


if __name__ == '__main__':
    RunCommand(True) 