import compas
from compas.geometry import Frame
import rhinoscriptsyntax as rs 
from id_generator import create_id
from assembly_model import Model


#
#__commandname__ = "Create_beam"
#
#def RunCommand(is_interactive):
#get user input
plane = rs.GetRectangle()
if plane: frame=(rs.PlaneFromPoints(plane[0], plane[1], plane[3]))
beam_frame = Frame(frame[0],frame[1],frame[3])
length = rs.GetReal("length",1000,300,None)
name = create_id()

model = Model()

beam = model.create_beam(Frame.worldXY(),1000,100,100,name)
model.to_json("create_beam.json", pretty = True)



model.from_json("create_beam.json")

print(len(model.beams))




