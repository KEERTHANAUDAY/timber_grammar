import rhinoscriptsyntax as rs

import compas
from compas.geometry import Frame
from id_generator import create_id
from assembly_model import Model

__commandname__ = "CreateBeam"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
    plane = rs.GetRectangle()
    if plane: frame=(rs.PlaneFromPoints(plane[0], plane[1], plane[3]))
    beam_frame = Frame(frame[0],frame[1],frame[3])
    length = rs.GetReal("length",1000,300,None)
    name = create_id()
    model = Model()
    beam = model.create_beam(Frame.worldXY(),1000,100,100,name)
    model.to_json("create_beam.json", pretty = True)
    return 0

if __name__ == '__main__':
    RunCommand(True)
