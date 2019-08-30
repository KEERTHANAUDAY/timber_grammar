import Rhino
from compas.geometry import Frame
import rhinoscriptsyntax as rs

def RunCommand():
    rc, corners = Rhino.Input.RhinoGet.GetRectangle()
    if rc != Rhino.Commands.Result.Success:
        return rc
    print(corners)
    plane = Rhino.Geometry.Plane(corners[0], corners[1], corners[2])
    beam_frame = Frame(plane[0],plane[1],plane[3])
    u_dir = rs.Distance(corners[0], corners[1])
    v_dir = rs.Distance(corners[1], corners[2])
    print(beam_frame)    
    print(u_dir)  
    print(v_dir )
    return beam_frame


if __name__ == "__main__":
    RunCommand()

