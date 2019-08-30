from Joint import Joint

class Joint_90tenon(Joint):
    
    def __init__(self,a):
        self.a = a
        raise NotImplementedError ("Joint_90tenon is not actually implmented yet")
    
    @property
    def data(self):
        """dict : A data dict representing all internal persistant data for serialisation.
        The dict has the following structure:
        * 'type'            => string
        * 'a'               => int
        * 'mesh'            => dict of compas.mesh.to_data()
        """
        data = {
            'type' : self.__class__.__name__, #Keep this line for deserialization
            'a'  : self.a,
            #'mesh'  : self.mesh.data,
            #'joints'  : [j.data for j in self.joints]
            }
        return data
    
    @data.setter
    def data(self, data):
        self.a   = data.get('a') or None
    
    @classmethod
    def from_data(cls,data):
        new_object = cls(None)
        new_object.data = data
        return new_object



if __name__ == "__main__":
    j =  Joint_90tenon(10)
    print(j.__class__.__name__)
    print(j.data['type'])
    pass