
import rhinoscriptsyntax as rs
import Rhino 
import scriptcontext as sc
import math

import compas
import compas.geometry

from assembly_model import Model
from rhino_UI_utilities import UI_helpers
from id_generator import create_id

from compas.geometry import Vector
from compas_rhino.artists import Artist
from compas_rhino.artists import MeshArtist
from compas.geometry import subtract_vectors
from compas.geometry import dot_vectors
from compas.geometry import is_point_on_plane
from compas.geometry import project_points_plane
from compas.geometry import distance_point_point
from compas.geometry import is_intersection_plane_plane
from compas.geometry import Point
from compas_rhino.artists import Artist
from compas_rhino.artists import MeshArtist


__commandname__ = "rule_ConnectBeams_90Lap"

def check_for_parallel_vectors(start_beam,beams_to_check):
    #this function is only used once 
    #check is used to make sure all instances are true, not sure how to eleminate it
    check = None
    a = start_beam.frame.xaxis
    for beam in beams_to_check:  
        tol = 1.0
        b = beam.frame.xaxis
        if dot_vectors(a,b) != tol:
            return False
        else:
            check = True

    if check == True:
        return True 


def get_coplanar_planes(start_beam_plane,start_beam_origin,beams_to_connect):

    #this function is only used once 

    match_plane = [] #zero index 
    for beam in beams_to_connect:
        for i in range(1,5):
            beam_plane = beam.face_plane(i).copy()
            beam_origin = beam_plane.point
            test_1 = is_point_on_plane(start_beam_origin,beam_plane)
            test_2 = is_point_on_plane(beam_origin,start_beam_plane)
            if test_1 == True and test_2 == True:
                match_plane.append(beam_plane)
            else:
                pass 
    if len(match_plane) == len(beams_to_connect):
        return match_plane

    else:
        return False 


def RunCommand(is_interactive):

    #load model
    model = Model.from_json("data.json")

    #select beams
    selection_reference = []
    selection_reference.append(rs.GetObject(message = "select start Beam", filter = 32, preselect = True))
    selection_reference.extend(rs.GetObjects(message = "select Beams to connect", filter = 32, preselect = True))

    #load helpers 
    helper = UI_helpers() 

    #name search
    selected_beams = helper.extract_BeambyName(model, selection_reference)

    #check for parallel planes, uses the function above
    start_beam = selected_beams[0]
    beams_to_connect = selected_beams[1:]   
    parallel_check = check_for_parallel_vectors(start_beam,beams_to_connect)

    if parallel_check != True:
        raise IndexError('beams are not parallel')

    else: 
        print("beams are parallel")

    #check for coplanarity, uses the function above 
    coplanar_planes = {}
    for i in range(1,5):
        start_beam_plane = start_beam.face_plane(i).copy()
        start_beam_origin = start_beam_plane.point
        a = get_coplanar_planes(start_beam_plane,start_beam_origin,beams_to_connect)
        if a != False:
            coplanar_planes[''+str(i)] = a         
        else:
            pass

    if len(coplanar_planes.keys()) == 2:
        print("'success",coplanar_planes)

    else:
        raise IndexError('beams are not coplanar')
    
    #possible faces to create joint if the coplanar faces are 1&3 the faces to create a joint would be 2&4
    if coplanar_planes.keys()[0] == "1" or coplanar_planes.keys()[0] == "3":
        face_option_1 = "2"
        face_option_2 = "4"
    if coplanar_planes.keys()[0] == "2" or coplanar_planes.keys()[0] == "4":
        face_option_1 = "1"
        face_option_2 = "3"
    
    #user inputs
    face_id = rs.GetInteger(("possible face connections "+"face_id "+ face_option_1 +" or face_id "+ face_option_2),None,None,None)
    start_point = (helper.Get_SelectPointOnMeshEdge("Select mesh edge","Pick point on edge"))
    ext_start = rs.GetReal("extension length start",None,None,None)
    ext_end = rs.GetReal("extension length end",None,None,None)


    #project points, this would need a plane perpendicular to the coplanar planes
        #find perpendicular planes to project points  
    if coplanar_planes.keys()[0] == "1" or  coplanar_planes.keys()[0] == "3":
        start_beam_perpendicular_plane = start_beam.face_plane(6).copy()
    
    elif coplanar_planes.keys()[0] == "2" or  coplanar_planes.keys()[0] == "4":
        start_beam_perpendicular_plane = start_beam.face_plane(5).copy() 

        #checking which plane of the beams to connect is perpendicular to the start plane\
        # there planes are all at the ceneter of the beam for convenience of calculating point position later   
    perpendicular_plane = []
    for beam in beams_to_connect:
        for i in range(5,7):
            beam_plane = beam.face_plane(i).copy()
            angle_check = start_beam_perpendicular_plane.normal.angle(beam_plane.normal)
            if angle_check ==0 or angle_check == 180:
                perpendicular_plane.append(beam_plane)

    #project points
    projected_point_list = []
    #correct start_point to center
    new_start_point = project_points_plane([start_point],start_beam_perpendicular_plane)
    projected_point_list.extend(new_start_point)
    for plane in perpendicular_plane:
       new_point = project_points_plane(new_start_point,plane)
       projected_point_list.extend(new_point)

    pt_distance = []
    for pt in projected_point_list[1:]:
        pt_distance.append(distance_point_point(new_start_point[0],pt))
    beam_length = max(pt_distance) + ext_start + ext_end + selected_beams[0].height #height is added considering the position of start point of translation 


    #check if beams are to the right/left or top/bottom 
    if face_id == 1 or face_id == 4:
        if (selected_beams[0].frame.point.x > selected_beams[1].frame.point.x) or \
            (selected_beams[0].frame.point.y < selected_beams[1].frame.point.y) or \
                (selected_beams[0].frame.point.z < selected_beams[1].frame.point.z) :
            new_ext_end = beam_length - ext_start
            print("direction = left")
        else:
            new_ext_end = ext_end + selected_beams[0].height 
            print("direction = right")
    elif face_id == 2 or face_id == 3:
        if (selected_beams[0].frame.point.x > selected_beams[1].frame.point.x) or \
            (selected_beams[0].frame.point.y < selected_beams[1].frame.point.y) or \
                (selected_beams[0].frame.point.z < selected_beams[1].frame.point.z) :
            new_ext_end = ext_end + selected_beams[0].height 
            print("direction = right")          
        else:
            new_ext_end = beam_length - ext_start
            print("direction = left")


    #list of distance to move joints on match beam    
    model.rule_Connect_90lap(selected_beams,projected_point_list,face_id,beam_length,new_ext_end,create_id())

    #Data serialization 
    model.to_json("data.json", pretty = True)
    
    # Visualization 
    viz_point = []
    for pt in projected_point_list:
        a = (pt[0],pt[1],pt[2])
        viz_point.append({
            'pos': a,
            'color': (0,255,0)
        })

    artist = MeshArtist(None, layer ='BEAM::Beams_out')
    artist.clear_layer()
    artist.draw_points(viz_point)
    for beam in model.beams:
        artist = MeshArtist(beam.mesh, layer ='BEAM::Beams_out')#.mesh is not ideal fix in beam and assemble class
        artist.draw_faces(join_faces=True)

    

if __name__ == '__main__':
    RunCommand(True) 
