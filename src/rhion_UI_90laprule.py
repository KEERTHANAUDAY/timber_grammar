if __name__ == "__main__":

import rhinoscriptsyntax as rs
import Beam as b

select_beam = rs.GetObject('Select beam mesh')
print(select_beam)
print(type(select_beam))

#load saved Beam object  (May be this is now how you search the datastructure?)
loaded_beam = b.Beam.from_json('test.json')
name = loaded_beam.name
print(loaded_beam.name)

if select_beam == name:
    print(name)  #after identifying the id how to link back to the instance 


