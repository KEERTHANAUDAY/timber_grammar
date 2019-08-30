import compas
from assembly_model import Model

#load Model
model = Model()

#This file should Run first to create an empty json file 
model.to_json("data.json", pretty = True)