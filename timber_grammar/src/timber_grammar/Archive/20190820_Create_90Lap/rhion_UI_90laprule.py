import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import System
import compas
 
from compas.datastructures import Mesh
from compas.geometry import Frame
from assembly_model import Model
from id_generator import create_id
import Beam as b

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import Artist


def Get_CrvPlusPointOnCurve(msg):
        #gets Mesh edge
        go = Rhino.Input.Custom.GetObject()
        go.SetCommandPrompt(msg)
        go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshEdge
        go.SubObjectSelect = True
        go.GroupSelect = False
        go.AcceptNothing(False)
        if go.Get()!=Rhino.Input.GetResult.Object: return
        objref = go.Object(0)
        point = objref.SelectionPoint()
        go.Dispose()
        return point

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
model = Model.from_Json("model.json")

### ---- Begin of function --- ###
### ### ### ### ### ### ### ### ### ###

# Ask user to select a beam object in Rhino scene
GUID = rs.SelectOneMesh()
# Find the name of the selected Rhino object  
selected_beam_name = rs.getName(GUID)
# Loop through all beams in model to identify the selected beam
selected_beam = None
for beam in model.beams:
    if (beam.name == selected_beam_name):
        selected_beam = beam
        break
# Raise error if the beam cannot be found
assert (selected_beam != None)
# Do something with this beam. 

#Ask use to select which face to put the lap joint
# Ask user where along the beam to make the joint

# Create new beam in the right 90 deg position
# with default length

# Add joint in both beams

#

### ### ### ### ### ### ### ### ### ###
### ---- End of function --- ###

# Save data
model.to_json("model.json", pretty=True)

# Update Visualization
artist = MeshArtist(None, layer='Beams_out')
artist = Artist(layer='Beams_out')
artist.clear_layer()
for beam in model.beams:
    # print(beam)
    print(beam.name)
    artist = MeshArtist(beam.mesh, layer='Beams_out')
    artist.draw_faces(join_faces=True)
    



# if __name__ == "__main__":

#     import rhinoscriptsyntax as rs
#     import Beam as b

#     select_beam = rs.GetObject('Select beam mesh')
#     print(select_beam)
#     print(type(select_beam))
# #
##    #load saved Beam object  (May be this is now how you search the datastructure?)
#    loaded_beam = b.Beam.from_json('test2.json')
#    
##
###    if select_beam == name:
###        print(name)  #after identifying the id how to link back to the instance 
##
##
