import compas
from compas.geometry import Frame
from assembly_model import Model
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
        

model = Model()

beam_frame = Frame.worldXY()
test = model.create_beam(beam_frame,1000,100,100)
beam_frame = Frame([0,100,300], [1,2,0], [0,5,6])

test = model.create_beam(beam_frame,1000,100,100)

for beam in model.beams:
    print(type(beam))
    artist = MeshArtist(beam.beam_mesh, layer='Beams_out_2')
    artist.clear_layer()
    artist.draw_vertices()
    artist.draw_faces(join_faces=False)

