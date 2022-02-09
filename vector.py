class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
    def __add__(self, v):
        assert self.dimension == v.dimension, "Cannot add vectors of differing dimentions"
        new_coords = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coords)
    
    def __sub__(self, v):
        assert self.dimension == v.dimension, "Cannot add vectors of differing dimentions"
        new_coords = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coords)
    
    def __mul__(self, v):
        if isinstance(v, int) or isinstance(v, float):
            new_coords = [v*c for c in self.coordinates]
            return Vector(new_coords)
        elif isinstance(v, Vector):
            pass
        else:
            print("Cannot multiply these values.")
        
    def __truediv__(self, v):
        if isinstance(v, int) or isinstance(v, float):
            new_coords = [c/v for c in self.coordinates]
            return Vector(new_coords)
        elif isinstance(v, Vector):
            pass
        else:
            print("Cannot multiply these values.")

if __name__ == '__main__':
    v1 = Vector([1,2,3])
    s = 2
    v2 = Vector([0,0,3])
    print(v1 + v2)
    print(v1 - v2)
    print(v1*s)
    print(v1/s)