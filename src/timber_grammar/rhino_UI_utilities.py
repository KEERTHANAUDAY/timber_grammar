import rhinoscriptsyntax as rs
import Rhino 
import scriptcontext as sc
from Beam import Beam
from compas.geometry import Plane
class UI_helpers(object):

    def __init__(self):

        pass

    def Get_SelectPointOnMeshEdge(self,message_0,message_1):
        """Performs 90Lap joint boolean operation to beam object:
        Parameters
        ----------
        message_0: First message to user
        message_1: Second message to user

        Return:
        ------
        Point3D 
        """
        go = Rhino.Input.Custom.GetObject()
        go.SetCommandPrompt(message_0)
        go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshEdge
        go.SubObjectSelect = True
        go.GroupSelect = False
        go.AcceptNothing(True)
        if go.Get()!= Rhino.Input.GetResult.Object: return
        objref = go.Object(0)
        index=objref.GeometryComponentIndex.Index
        mesh=objref.Mesh()
        edge_line=mesh.TopologyEdges.EdgeLine(index)
        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt(message_1)
        gp.Constrain(edge_line)
        get_rc = gp.Get()
        placed_point = rs.coerce3dpoint(sc.doc.Objects.AddPoint(gp.Point()))
        sc.doc.Views.Redraw()

        return placed_point

    def selectmeshface(self):#Not used yet
        """Selects a face of a mesh 
        Parameters
        ----------
        message_0: First message to user
        message_1: Second message to user

        Return:
        ------
        Point3D 
        """
        go = Rhino.Input.Custom.GetObject()
        go.GeometryFilter=Rhino.DocObjects.ObjectType.MeshFace
        go.SetCommandPrompt("Get mesh Face")
        go.Get()
        objref=go.Object(0)
        face_guid = objref.ObjectId
        go.Dispose()
        
        return face_guid 

    def get_match_frame(self,face_id):
        """Identifies the face_id of the match Beam
        Parameters
        ----------
        face_id: (int) of selected Beam Object

        Return:
        ------
        int  
        """
        if face_id == 4:
            match_face_id = 3
        elif face_id == 3:
            match_face_id = 3
        elif face_id == 2:
            match_face_id = 1
        elif face_id == 1:
            match_face_id = 1
        else:
            pass

        return match_face_id

    def get_Beam_interecting_Planes(self, BeamsRef,flag=0,face_id=None):
        """Computes the interecting planes of a given Beam
        ----------
        face_id: (int) of selected Beam Object

        Return:
        ------
        int  
        """
        if flag == 0:
            intersecting_planes = []
            frame = BeamsRef.get_face_frame(4)
            intersecting_planes.append(Plane(frame.point, frame.normal))
            frame = BeamsRef.get_face_frame(3)
            intersecting_planes.append(Plane(frame.point, frame.normal))
            return intersecting_planes
        elif flag == 1:
            frame = BeamsRef.get_face_frame(face_id)
            start_frame = Plane(frame.point, frame.normal)
            return start_frame
        else:
            pass



