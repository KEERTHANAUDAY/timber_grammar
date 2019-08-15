import rhinoscriptsyntax as rs
import compas
import System
 
from compas.datastructures import Mesh
from compas.geometry import Frame
from assembly_model import Model
from compas_rhino.artists import MeshArtist
from compas_rhino.helpers import mesh_select_face
from compas_rhino.artists import Artist
from compas_rhino.utilities import select_mesh
from compas_rhino.helpers import mesh_from_guid

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
        
       
plane = rs.GetRectangle()
if plane:
    frame = rs.PlaneFromPoints(plane[0], plane[1], plane[3])
    
beam_frame = Frame(frame[0],frame[1],frame[3])   

length = rs.GetReal("length",None, 300, None)
width = rs.GetReal("width",None, 100, 200)
height = rs.GetReal("height",None, 100, 200)
distance = rs.GetReal("distance",None, None, None)

model = Model()
test = model.create_beam(beam_frame,length,width,height)
test_cut = model.rule_90lap(test.mesh,0,distance)
test_return = model.create_beam_match(test,0,500,distance)
print(test_return)


artist1 = MeshArtist(test_return, layer='Beams_out')
artist1.draw_faces(join_faces=True)
#    
for beam in model.beams:
    artist = MeshArtist(beam, layer='Beams_out')
    artist.draw_faces(join_faces=True)
#    

    
    
