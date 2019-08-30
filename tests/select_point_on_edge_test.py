
import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

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
    
    #Object is a Mesh edge
#    index=objref.GeometryComponentIndex.Index
#    edge = objref.Object().Geometry.Edges[index]
#    Rhino.DocObjects.ObjRef.Mesh.E

    #point selection
    point = objref.SelectionPoint()
    go.Dispose()
    return point

#THIS IS THE POINT COORDINATES FOR THE DESIRED BOOL GEOMETRY LOCATION
test = Get_CrvPlusPointOnCurve("select distance")
print((test))