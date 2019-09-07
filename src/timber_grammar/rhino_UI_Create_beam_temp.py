import rhinoscriptsyntax as rs

import Rhino
import compas
from compas.geometry import Frame
from id_generator import create_id
from assembly_model import Model
from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist

__commandname__ = "CreateBeam" 


def RunCommand( is_interactive ):
    #load model
    model = Model.from_json("data.json")

    #user input
    rc, corners = Rhino.Input.RhinoGet.GetRectangle()
    if rc != Rhino.Commands.Result.Success:
        return rc
    plane = Rhino.Geometry.Plane(corners[0], corners[1], corners[2])
    beam_frame = Frame(plane[0],plane[1],plane[2])
    length = rs.GetReal("length",4000,300,None)

    #Generate unique name for the Beam 
    name = create_id()
    
    #Create Beam 
    model.rule_create_beam(beam_frame,length,100,100,name)

    
    #Data serialization 
    model.to_json("data.json", pretty = True)
    
    #Visualization
    artist = MeshArtist(None, layer ='BEAM::Beams_out')
    artist.clear_layer()
    for beam in model.beams:
        artist = MeshArtist(beam.mesh, layer ='BEAM::Beams_out')#.mesh is not ideal fix in beam and assemble class
        artist.draw_faces(join_faces=True)
    return 0

if __name__ == '__main__':
    RunCommand(True)
