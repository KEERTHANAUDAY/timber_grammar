"""Places a point along a curve at a specified distance from picked end
Script by Mitch Heynick, 23 March 2014"""

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

def PlacePointAlongCrv():
    crvObj=rs.GetCurveObject("Select curve near desired end")
    if crvObj==None: return
    tol=rs.UnitAbsoluteTolerance()
    crvLen=rs.CurveLength(crvObj[0])
    
    msg="Distance from picked end to place point?"
    len=rs.GetReal(msg,minimum=tol, maximum=crvLen-tol)
    if len==None: return
    
    crv=sc.doc.Objects.Find(crvObj[0]).Geometry
    #crv.Domain[0] is crv start parameter; crvObj[4] is pick parameter    
    lenA=crv.GetLength(Rhino.Geometry.Interval(crv.Domain[0],crvObj[4]))
    #flip curve if pick is closer to end
    if lenA>(crvLen/2.0): crv.Reverse()
    
    rc,par = crv.LengthParameter(len)
    if rc: 
        pt=crv.PointAt(par)
        sc.doc.Objects.AddPoint(pt)
    sc.doc.Views.Redraw()
    
PlacePointAlongCrv()