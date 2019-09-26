import json

class Joint(object):

    def __init__(self):
        """Handel the creation of sub class objects
        """
        pass

    @classmethod
    def from_data(cls,data):
        """Construct a Joint object from structured data.
        This class method must be overridden by an inherited class.

        Parameters
        ----------

        data : dict
            The data dictionary.
            
        Returns
        -------

        object
            An object of the type (based on the 'type' value defined in data)

        Note
        ----

        This constructor method is meant to be used in conjuction with the
        corresponding *to_data* method.
        
        """
        
        #Remember to update this list of import for each new classes that are inhereted from this super class
        from Joint_90lap import Joint_90lap
        from Joint_90tenon import Joint_90tenon

        #Remember to update this dictionary if new classes are inhereted from this super class
        class_types = {
            'Joint_90lap':Joint_90lap,
            'Joint_90tenon':Joint_90tenon,
            }
        subclass_name = data['type']
        assert subclass_name in class_types , "Deserialized object type: %s is not listed in from_data() of Joint class." % subclass_name
        sub_class = class_types.get(subclass_name)
        
        # raise NotImplementedError("The inherited class %s did not implement from_data()" % cls.__name__)
        return sub_class.from_data(data)

    def to_data(self):
        """Returns a dictionary of structured data representing the data structure.
        Actual implementation is in @property def data(self) of the inherited class
        Returns
        -------
        dict
            The structured data.
        Note
        ----
        This method produces the data that can be used in conjuction with the
        corresponding *from_data* class method.
        """
        assert hasattr(self, 'data'), "Inherited class %s do not have data attribute" % self.__class__.__name__
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
            An object of the type of a Joint subclass
        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_json* method.
        """
        # PATH = os.path.abspath(os.path.join(filepath, '..', 'data'))
        with open(filepath, 'r') as fp:
            data = json.load(fp)

        #Create new object using from_data in inherited class
        return cls.from_data(data)
    
    def to_json(self, filepath, pretty=False):
        """Serialise the structured data representing the data structure to json.
        Parameters
        ----------
        filepath : str
            The path to the json file.
        """
        assert hasattr(self, 'data'), "Inherited class %s do not have data attribute" % self.__class__.__name__
        # PATH = os.path.abspath(os.path.join(filepath, '..', 'data'))
        with open(filepath, 'w+') as fp:
            if pretty:
                json.dump(self.data, fp, sort_keys=True, indent=4)
            else:
                json.dump(self.data, fp)


if __name__ == "__main__":
    #Test to create a inherited joint object, serialize and deserialize it. 
    from Joint_90lap import Joint_90lap 
    from compas.geometry._primitives import Frame

    j =  Joint_90lap(Frame.worldXY(),1,50,100,100)
    j.to_json("n.json",pretty=True)
    print(j)
    print (j.data)
    q = Joint.from_json("n.json")
    print(q)
    print (q.data)