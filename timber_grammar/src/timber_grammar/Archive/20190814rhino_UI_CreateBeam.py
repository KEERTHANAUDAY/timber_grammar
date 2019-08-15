import rhinoscriptsyntax as rs
import System
import compas
 
from compas.datastructures import Mesh
from compas.geometry import Frame
from assembly_model import Model
from id_generator import create_id
import Beam as b

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist

#def rule_create_beam():
#    model.load_beams()
#    #Ask for user to input beam location
#    #Ask for beam direction
#    #Ask for width, length , height
#    model.create_beam(Frame.worldXY(),depth, width, height)
#    
#    #Visualize all the beams in Rhino
#    #Clear Rhino preview layer.
#    for beam_mesh in model.mesh:
#        #Paint the mesh

# Load previous model
m = Model()
n = m.from_json("model.json")

### ---- Begin of function --- ###
### 
# Print the name of the function to Rhino Command Line:
__commandname__ = "CreateBeam"

#def RunCommand( is_interactive ):
#    pass
#
## Ask user for beam input
#plane = rs.GetRectangle()
#if plane:
#    frame = rs.PlaneFromPoints(plane[0], plane[1], plane[3])
#beam_frame = Frame(frame[0],frame[1],frame[3])   
#
#width = rs.GetReal("width",100, 100, 200)
#height = rs.GetReal("height",100, 100, 200)
#length = rs.GetReal("length",1000, 300, None)
#name = create_id()
#
## Create new beam and add it to model.beams[]
#model.create_beam(beam_frame,length,width,height,name)
#
####
#### ---- End of function --- ###
#
## Save data
#model.to_json("model.json", pretty=True)
#
## Update Visualization
#artist = MeshArtist(None, layer='Beams_out')
#artist = Artist(layer='Beams_out')
#
#artist.clear_layer()
#for beam in model.beams:
#    # print(beam)
#    print(beam.name)
#    artist = MeshArtist(beam.mesh, layer='Beams_out')
#    artist.draw_faces(join_faces=True)
#    
#
#    
