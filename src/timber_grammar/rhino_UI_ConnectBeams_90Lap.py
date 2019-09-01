import rhinoscriptsyntax as rs
import Rhino 
import scriptcontext as sc

import compas
from compas.geometry import intersection_plane_plane
from assembly_model import Model
from rhino_UI_utilities import UI_helpers

__commandname__ = "ConnectBeams_90Lap"

def RunCommand(is_interactive):

    #load model
    model = Model.from_json("data.json")

    #select meshes
    obj_refs = []
    obj_refs.append(rs.GetObject(message = "select start Beam", filter = 32, preselect = True))
    obj_refs.append(rs.GetObject(message = "select Beams to connect", filter = 32, preselect = True))

    #list of beam names
    seleceted_beam_names = [rs.ObjectName(name)[:-5] for name in obj_refs]

    #list of selected beams 
    selected_beams = []
    for beam in model.beams:
        for name in seleceted_beam_names:
            if(beam.name == name):
                selected_beam = beam 
                selected_beams.append(selected_beam)
                break
    assert (selected_beam != None for selected_beam in selected_beams)
   
    
    #user inputs
    face_id = rs.GetInteger("face_id",None,0,5)
    helper = UI_helpers()
    start_point = helper.Get_SelectPointOnMeshEdge("Select mesh edge","Pick point on edge")

    #finding parallel planes of selected beams 
    start_Beam_plane = helper.get_Beam_interecting_Planes(selected_beams[0],1,face_id)
    print(start_Beam_plane)
    connecting_Beams_planes=[helper.get_Beam_interecting_Planes(BeamRef,0,None) for BeamRef in selected_beams[1:]]


    connecting_Beams_plane =[]
    for BeamRef in selected_beams[1:]:
        #list of the two intersecting planes of a single Beam 
        intersecting_planes = helper.get_Beam_interecting_Planes(BeamRef,0,None) 

        for plane in intersecting_planes:
            test = intersection_plane_plane(plane,start_Beam_plane)
            print(test)
            if test == None:
                parallel_plane = plane
                connecting_Beams_plane.append(parallel_plane)
            else:
                pass
                
    print(connecting_Beams_plane)

  


    #create lap joint on selected beams  
    #create match beam for match beam 

    #save model

    #paint mesh 

if __name__ == '__main__':
    RunCommand(True) 