import math
import compas
import json
import sys

from Beam import Beam
from assembly_model import Model


class Derivation(object):
    """ Derivation class holds a list of models
    mesh proxy)
    """

    def __init__(self):
        """ initialization
           
        """
        self.models = []


    @property   
    def data(self):
        """dict : A data dict representing all internal persistant data for serialisation.
        The dict has the following structure:
        * 'type'            => string (name of the class)
        * 'models'           => list of dict of Beam.to_data()
        """
        data = {
            'type'      : self.__class__.__name__, #Keep this line for deserialization
            'models'    : [model.to_data() for model in self.models],
            }
        return data
    
    @data.setter
    def data(self, data):

        for model_data in data.get('models') :
            self.models.append(Model.from_data(model_data))
    
    @classmethod
    def from_data(cls,data):
        """Construct a Derivation object from structured data.
        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        object
            An object of the type Derivation

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_data* method.

        """

        new_object = cls() # Only this line needs to be updated
        new_object.data = data

        return new_object
   
    def to_data(self):
        """Returns a dictionary of structured data representing the data structure.
        Actual implementation is in @property def data(self)

        Returns
        -------
        dict
            The structured data.

        Note
        ----
        This method produces the data that can be used in conjuction with the
        corresponding *from_data* class method.

        """
        return self.data

    @classmethod
    def from_json(cls, filepath):
        """Construct a datastructure from structured data contained in a json file.

        Parameters
        ----------
        filepath : str
            The path to the json file.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_json* method.

        """
        #If file cannot be found, create an empty file and write an empty cls data into it.
        import os
        if (os.path.isfile(filepath) == False):
            empty_cls = cls()
            empty_cls.to_json(filepath)
            print('New Json Created: Type=', empty_cls.data['type'])
            return empty_cls

        #Open file and load load content
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        print('Json Loaded: Type=', data['type'])

        assert data['type'] ==  cls.__name__ , "Deserialized object type: %s is not equal to %s." % (data['type'] , cls.__name__)
        return cls.from_data(data)

    def to_json(self, filepath, pretty=False):
        """Serialise the structured data representing the data structure to json.

        Parameters
        ----------
        filepath : str
            The path to the json file.

        """
        # PATH = os.path.abspath(os.path.join(filepath, '..', 'data'))
        with open(filepath, 'w+') as fp:
            if pretty:
                json.dump(self.data, fp, sort_keys=True, indent=4)
            else:
                json.dump(self.data, fp)

    @property
    def count(self):
        return len(self.models)
      
    def get_step(self,index):
        if index < 0 or index > self.count:
            raise IndexError('index= ', index , ' is out of range, item count=' , self.count)
        return self.models[index]

    def remove_last_step(self):
        return self.models.pop()
        
    def get_next_step(self):
        if (self.count == 0):
            next_model = Model()
        else:
            next_model = Model.from_data( self.get_step(self.count-1 ).data )

        self.models.append(next_model)
        return next_model     
        
if __name__ == '__main__':
    import compas
    import tempfile
    import os

    #Test 1 : Save a model and load it back and compare their data
    print("Test 1: Derivation Data Save and Load to JSON")

    #Create Beam object
    beam = Beam.debug_get_dummy_beam(include_joint=True)

    #Add beam to model
    model = Model()
    model.beams.append(beam)

    #Add model to derivation
    derivation = Derivation()
    derivation.models.append(model)
    derivation.get_next_step()

    #Save Model 
    derivation.to_json(os.path.join(tempfile.gettempdir(), "derivation.json"),pretty=True)
    
    #Load the saved Model
    loaded_derivation = Derivation.from_json(os.path.join(tempfile.gettempdir(), "derivation.json"))

    print("Comparing two Derivation's data dictionary:")
    assert (derivation.data == loaded_derivation.data)
    if (derivation.data == loaded_derivation.data):
        print("Correct") 
    else:
        print("Incorrect")
    print("-- -- -- -- -- -- -- --")       

    print("Test 2: Print out dummy derivation (with Joint) data")
    print (derivation.data)
    
    print("-- -- -- -- -- -- -- --")       

    print("Test 3: Add and delete models")
    derivation = Derivation()
    print("Testing .get_next_step() when Derivation is empty ")
    derivation.get_next_step() # This should return an empty model
    assert (derivation.count == 1)
    print("Testing .models.append(model)")
    derivation.models.append(model)
    assert (derivation.count == 2)
    print("Testing .get_next_step() and compare the new copy")
    derivation.get_next_step()
    derivation.get_next_step()
    assert derivation.models[2].data == derivation.models[3].data 
    print("Testing .remove_last_step()")
    derivation.remove_last_step()
    assert (derivation.count == 3)
 
    if (derivation.count == 3):
        print("Correct") 
    else:
        print("Incorrect")

    print("-- -- -- -- -- -- -- --")