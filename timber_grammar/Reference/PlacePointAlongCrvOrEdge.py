"""Places a point along a curve at a specified distance from picked end
This version supports picking Brep edges as well as curves
Script by Mitch Heynick, 24 March 2014"""

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

def GetCrvPlusPointOnCrv(msg):
    #gets curve or Brep edge curve; returns curve plus pick point
    go = Rhino.Input.Custom.GetObject()
    go.SetCommandPrompt(msg)
    go.GeometryFilter = Rhino.DocObjects.ObjectType.Curve
    go.SubObjectSelect = True
    go.GroupSelect = False
    go.AcceptNothing(False)
    
    if go.Get()!=Rhino.Input.GetResult.Object: return
    objref = go.Object(0)
    index=objref.GeometryComponentIndex.Index
    if index==-1:
        #object is a curve
        crv=objref.Object().Geometry
    else:
        #object is a Brep edg
        edge=objref.Object().Geometry.Edges[index]
        crv=edge.ToNurbsCurve()
    point = objref.SelectionPoint()
    go.Dispose()
    return crv, point

def PlacePointAlongCrvOrEdge():
    msg="Select curve or surface edge near desired end"
    crvObj=GetCrvPlusPointOnCrv(msg)
    if crvObj==None: return
    crv,pickPt=crvObj
    
    tol=rs.UnitAbsoluteTolerance()
    crvLen=crv.GetLength()
    msg="Distance from picked end to place point?"
    len=rs.GetReal(msg,minimum=tol, maximum=crvLen-tol)
    if len==None: return
    
    #crv.Domain[0] is crv start parameter; find pick parameter
    rc,pickPar=crv.ClosestPoint(pickPt)
    if not rc: return
    lenA=crv.GetLength(Rhino.Geometry.Interval(crv.Domain[0],pickPar))
    #flip curve if pick is closer to end
    if lenA>(crvLen/2.0): crv.Reverse()
        
    
    rc,par = crv.LengthParameter(len)
    if rc: 
        pt=crv.PointAt(par)
        sc.doc.Objects.AddPoint(pt)
    sc.doc.Views.Redraw()
    
PlacePointAlongCrvOrEdge()