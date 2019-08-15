import Rhino
import scriptcontext as sc

def add_id(mesh):
    
    #add to doc, guid is returned
    id = sc.doc.Objects.AddMesh(mesh)
    
    #create objRef from guid
    objRef = Rhino.DocObjects.ObjRef(id)
    
    #get rhinoObject from objRef
    obj = objRef.Object()
    
    #set your user string to the object attributes
    obj.Attributes.SetUserString("ID", str(id))
    
    #very important: commit changes to the object in the rhinodoc
    obj.CommitChanges()
    
    #redraw
    sc.doc.Views.Redraw()
    
if __name__ == "__main__":
    
    
    
    