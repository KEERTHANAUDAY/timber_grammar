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
        # if face_id == 4:
        #     match_face_id = 3
        # elif face_id == 3:
        #     match_face_id = 3
        # elif face_id == 2:
        #     match_face_id = 1
        # elif face_id == 1:
        #     match_face_id = 1
        # else:
        #     pass
        if face_id==4 or face_id==3: face_id=3
        elif face_id==2 or face_id==1:face_id=1
        return face_id

    def get_start_face(self,face_id):
        
        if face_id == 3 or face_id == 1: face_id == 4
        elif face_id == 4 or face_id == 2: face_id == 3
        return face_id

    def get_Beam_interecting_Planes(self, BeamsRef,flag=0,face_id=None):
        """Computes the interecting planes of a given Beam
        ----------

        """
        if flag == 0:
            intersecting_planes = []
            frame = BeamsRef.get_face_frame(4)
            intersecting_planes.append(Plane(frame.point, frame.normal))
            frame = BeamsRef.get_face_frame(3)
            intersecting_planes.append(Plane(frame.point, frame.normal))
            return intersecting_planes
        elif flag == 1:
            frame = BeamsRef.get_face_frame(self.get_start_face(face_id))
            start_frame = Plane(frame.point, frame.normal)
            return start_frame
        else:
            pass

    def extract_BeambyName(self,model, obj_refs):
        """Extracts the Beam object by peforming a name search 
        ---------
        """
        seleceted_beam_names = [rs.ObjectName(name)[:-5] for name in obj_refs]
        selected_beams = []
        for name in seleceted_beam_names:
            for beam in model.beams:
                if(beam.name == name):
                    selected_beam = beam 
                    selected_beams.append(selected_beam)
                    break
        assert (selected_beam != None for selected_beam in selected_beams)
        return (selected_beams)

## Reimplementation of COMPAS because some user do not have latest COMPAS
def get_document_basename():
    return rs.DocumentName()

def get_document_filename():
    import os
    basename = get_document_basename()
    if not basename:
        return None
    return os.path.splitext(basename)[0]

def get_document_filepath():
    return rs.DocumentPath()

def get_json_file_location():
    filename = get_document_filename()
    if not filename: return None
    
    path = get_document_filepath()
    return path + filename + ".json"



