from assembly_model import Model

test = Model.from_json("create_beam.json")
print(test.data)