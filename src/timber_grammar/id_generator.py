# import System
import uuid

def create_id():
    """Generates a UUID
    Return:
    ------
    UUID
    """
    g = str(uuid.uuid1())
    return g

if __name__ == "__main__":
    a = create_id()
    print(type(a))
    print(a)



