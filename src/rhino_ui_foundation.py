import rhinoscriptsyntax as rs
import System
import compas
 
from compas.datastructures import Mesh
from compas.geometry import Frame
from assembly_model import Model
from id_generator import create_id

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
           
plane = rs.GetRectangle()
if plane:
    frame = rs.PlaneFromPoints(plane[0], plane[1], plane[3])
beam_frame = Frame(frame[0],frame[1],frame[3])   

length = rs.GetReal("length",None, 300, None)
width = rs.GetReal("width",None, 100, 200)
height = rs.GetReal("height",None, 100, 200)
name = create_id()

model = Model()
test = model.create_beam(beam_frame,length,width,height,name)

#serialize data
model.to_json("test.json", pretty=True)
    
for beam in model.uncut_beam:
    print(beam)
    print(beam.name)
    artist = MeshArtist(beam.mesh, layer='Beams_out')
    artist.clear_layer()
    artist.draw_faces(join_faces=True)
    

    
