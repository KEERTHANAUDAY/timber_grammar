import compas
from assembly_model import Model
model = Model()

model.to_json("data.json", pretty = True)