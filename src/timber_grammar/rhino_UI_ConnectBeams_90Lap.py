import rhinoscriptsyntax as rs
import Rhino 
import scriptcontext as sc

import compas
import compas.geometry
from compas.geometry import intersection_plane_plane
from compas.geometry import Point
from compas.geometry import project_points_plane
from compas.geometry import distance_point_plane
from assembly_model import Model
from rhino_UI_utilities import UI_helpers
from id_generator import create_id
from compas_rhino.artists import Artist
from compas_rhino.artists import MeshArtist

__commandname__ = "ConnectBeams_90Lap"

def RunCommand(is_interactive):

    #load model
    model = Model.from_json("data.json")

    #select meshes
    obj_refs = []
    obj_refs.append(rs.GetObject(message = "select start Beam", filter = 32, preselect = True))
    obj_refs.extend(rs.GetObjects(message = "select Beams to connect", filter = 32, preselect = True))

    #user inputs
    face_id = rs.GetInteger("face_id",None,0,5)
    helper = UI_helpers() 
    start_point = (helper.Get_SelectPointOnMeshEdge("Select mesh edge","Pick point on edge"))
    joint_points=[(Point(start_point[0],start_point[1],start_point[2]))]#list of compas points
    ext = rs.GetReal("extension length",None,None,None)
    
    #Beam search
    selected_beams = helper.extract_BeambyName(model, obj_refs)

    #finding parallel planes of selected beams 
    start_Beam_plane = helper.get_Beam_interecting_Planes(selected_beams[0],1,face_id)
    #extracting parallel planes 
    connecting_Beams_plane =[]
    test = []
    for BeamRef in selected_beams[1:]:
        intersecting_planes = helper.get_Beam_interecting_Planes(BeamRef,0,None)
        for plane in intersecting_planes:
            planes = intersection_plane_plane(plane,start_Beam_plane)
            if planes == None:
                parallel_plane = plane
                connecting_Beams_plane.append(parallel_plane)
            else:
                test.append(plane)

    projected_point_list = []
    list_point = [start_point]
    for plane in connecting_Beams_plane:
        projected_point_list.extend(project_points_plane(list_point,plane))
#unsure how to write the above loops as a comprehension, attempt below(unsucessful)
#    projected_point_list = [project_points_plane(list_point,plane)for plane in connecting_Beams_plane]

    joint_points.extend([Point(list[0],list[1],list[2])for list in projected_point_list])

    #create lap joint on selected beams 
    for selected_beam in selected_beams:
        for joint_point in joint_points:
            model.rule_90lap(selected_beam,joint_point,face_id)
    
    dist=[]
    for plane in test:
        dist.append(joint_points[0].distance_to_plane(plane))
    length = (max(dist))+ext+ext
    print(length)
#
    model.match_Beam_to_Beams(selected_beams,length,ext,create_id(),joint_points,face_id,helper.get_match_frame(face_id))
    #save model

    #Visualization 
    artist = MeshArtist(None, layer ='BEAM::Beams_out')
    artist.clear_layer()
    for beam in model.beams:
        artist = MeshArtist(beam.mesh, layer ='BEAM::Beams_out')#.mesh is not ideal fix in beam and assemble class
        artist.draw_faces(join_faces=True)



if __name__ == '__main__':
    RunCommand(True) 