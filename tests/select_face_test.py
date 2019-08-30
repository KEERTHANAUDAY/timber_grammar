import Rhino
import scriptcontext

go = Rhino.Input.Custom.GetObject()
go.GeometryFilter=Rhino.DocObjects.ObjectType.MeshFace
go.SetCommandPrompt("Get mesh Face")
go.Get()
objref=go.Object(0)
go.Dispose()
print(go)
print(type(go))
mesh = objref.Mesh()

print(mesh)