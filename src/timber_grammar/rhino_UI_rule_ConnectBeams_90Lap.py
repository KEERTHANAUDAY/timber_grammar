
import rhinoscriptsyntax as rs
import Rhino 
import scriptcontext as sc
import math

import compas
import compas.geometry

from assembly_model import Model
from Derivation import Derivation
import rhino_UI_utilities
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
from compas.geometry import intersection_line_plane
from compas.geometry import Point
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import Line
from compas.geometry import Plane
from compas_rhino.artists import Artist
from compas_rhino.artists import MeshArtist



__commandname__ = "rule_ConnectBeams_90Lap"

def check_for_parallel_vectors(start_beam,beams_to_check):
    #this function is only used once 

    a = start_beam.frame.xaxis
    for beam in beams_to_check:  
        tol = 1.0e-5
        b = beam.frame.xaxis
        if abs(abs(dot_vectors(a,b)) - 1.0) > tol:
            return False

    return True 


def get_coplanar_planes(start_beam_plane,start_beam_origin,beams_to_connect):

    #this function is only used once 

    match_plane = [] #zero index retun index not plane 
    face_ids = []
    for beam in beams_to_connect:
        for i in range(1,5):
            beam_plane = beam.face_plane(i).copy()
            beam_origin = beam_plane.point
            test_1 = is_point_on_plane(start_beam_origin,beam_plane)
            test_2 = is_point_on_plane(beam_origin,start_beam_plane)
            if test_1 == True and test_2 == True:
                match_plane.append(beam_plane)
                face_ids.append(i)
            else:
                print("i"+ str(i))
                pass 
    if len(match_plane) == len(beams_to_connect):
        return [match_plane,face_ids]

    else:
        return False 


def RunCommand(is_interactive):

    #load Derivation and model
    derivation = Derivation.from_json(rhino_UI_utilities.get_json_file_location())
    model = derivation.get_next_step()

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
    face_ids_coplanar_planes = {}
    for i in range(1,5):
        start_beam_plane = start_beam.face_plane(i).copy()
        start_beam_origin = start_beam_plane.point
        a = get_coplanar_planes(start_beam_plane,start_beam_origin,beams_to_connect)
        if a != False:
            coplanar_planes[''+str(i)] = a[0]  
            face_ids_coplanar_planes[''+str(i)] = a[1]
        else:
            pass
    print("face_dictionary here",face_ids_coplanar_planes)
    if len(coplanar_planes.keys()) == 2:
        print("'success",coplanar_planes)
    else:
        raise IndexError('beams are not coplanar')
    

    #user inputs
    face_id = rs.GetInteger(("possible face connections "+"face_id "+  coplanar_planes.keys()[0] +" or face_id "+  coplanar_planes.keys()[1]),None,None,None)
    start_point = (helper.Get_SelectPointOnMeshEdge("Select mesh edge","Pick point on edge"))
    ext_start = rs.GetReal("extension length start",200,None,None)
    ext_end = rs.GetReal("extension length end",200,None,None)

    #list of coplanar planes extracted from coplanar_planes dict using face_id as key
    coplanar_planes_along_selected_face = []
    coplanar_planes_along_selected_face.append(start_beam.face_plane(face_id).copy())
    for key,value in coplanar_planes.items():
        if key == ""+str(face_id):
            coplanar_planes_along_selected_face.extend(value)

    #list of face_ids of coplanar planes 
    coplanar_face_ids = []
    coplanar_face_ids.append(face_id)
    for key,value in face_ids_coplanar_planes.items():
        if key == ""+str(face_id):
            coplanar_face_ids.extend(value)


    #intersection points by passing a line from the origin of start beam to the adjacent planes of the coplanar planes of all beams
    points_to_compare = [] 
    for i in range(len(selected_beams)):
        beam = selected_beams[i]
        start_beam_selected_face_frame = selected_beams[0].face_frame(face_id)  
        line_pt_a =  start_beam_selected_face_frame.point
        normal = start_beam_selected_face_frame.normal
        line_pt_b =  add_vectors(line_pt_a,scale_vector(normal,0.3))
        line_to_intersect = Line(line_pt_a,line_pt_b)

        face_index = coplanar_face_ids[i]
        adjacent_planes = beam.neighbour_face_plane(face_index)
        for p in adjacent_planes:
            intersection_point = intersection_line_plane(line_to_intersect,p)
            points_to_compare.append(intersection_point)


    viz_pts = []
    #project distance from  points_to_compare to the plane of the start Beam 
    distances = []
    start_beam_face_frame = start_beam.face_frame(face_id).copy()
    start_beam_Plane_perpendicular_to_face_id_Plane = Plane(start_beam_face_frame.point,start_beam_face_frame.normal)
    viz_pts.append(start_beam_Plane_perpendicular_to_face_id_Plane.point)
    for point in points_to_compare:
        viz_pts.append(point)
        vector = subtract_vectors(point, start_beam_Plane_perpendicular_to_face_id_Plane.point)
        distances.append(dot_vectors(vector, start_beam_Plane_perpendicular_to_face_id_Plane.normal))
   

    #search to find max point
    maximum_distance = max(distances)
    minimum_distance = min(distances)
    beam_length = (maximum_distance - minimum_distance) + ext_start + ext_end 
    ext_len = maximum_distance + ext_start
                
    #project selected point to perpendicular planes of the beams to connect 
    if coplanar_planes.keys()[0] == "1" or  coplanar_planes.keys()[0] == "3":
        start_beam_perpendicular_plane = start_beam.face_plane(5).copy()
    
    elif coplanar_planes.keys()[0] == "2" or  coplanar_planes.keys()[0] == "4":
        start_beam_perpendicular_plane = start_beam.face_plane(6).copy() 
  
    tol = 1.0e-5
    # tol = 5.0
    perpendicular_plane = []
    for beam in beams_to_connect:
        for i in range(5,7):
            beam_plane = beam.face_plane(i).copy()
            print("beam_plane",beam_plane)
            angle_check = start_beam_perpendicular_plane.normal.angle(beam_plane.normal)
            print("angle",angle_check)
            if (abs(angle_check) - 0) < tol or (abs(angle_check) - 180) < tol:
                perpendicular_plane.append(beam_plane)
            
    print(perpendicular_plane)
    print(len(perpendicular_plane))
    #project points
    projected_point_list = []
    new_start_point = project_points_plane([start_point],start_beam_perpendicular_plane)
    projected_point_list.extend(new_start_point)
    for plane in perpendicular_plane:
       new_point = project_points_plane(new_start_point,plane)
       projected_point_list.extend(new_point)

    #list of distance to move joints on match beam    
    model.rule_Connect_90lap(selected_beams,projected_point_list,coplanar_face_ids,beam_length,ext_len,create_id())
    print(len(projected_point_list))
    print(projected_point_list)


    #Save Derivation (Model is also saved)
    derivation.to_json(rhino_UI_utilities.get_json_file_location(), pretty = True)
    
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
