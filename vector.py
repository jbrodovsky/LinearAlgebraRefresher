import math

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
            # Inner or Dot product
            assert self.dimension == v.dimension, "Cannot multiply vectors of differing lengths"
            return sum([x*y for x, y in zip(self.coordinates, v.coordinates)])
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
            
    def magnitude(self):
       mag = sum([x**2 for x in self.coordinates])
       return math.sqrt(mag)
   
    def direction(self):
        mag = self.magnitude()
        basis = [x/mag for x in self.coordinates]
        return Vector(basis)
    
    def get_angle(self, v):
        assert isinstance(v, Vector) and self.dimension == v.dimension, "Can only calculate the angle between vecotrs of the same number of dimensions"
        dot = self * v
        mag = self.magnitude() * v.magnitude()
        return math.acos(dot / mag)

if __name__ == '__main__':
    v1 = Vector([1,2,3])
    s = 2
    v2 = Vector([0,0,3])
    print(v1)
    print(v2)
    print(f"Scalar s: {s}")
    print("Sum: " + (v1 + v2).__str__())
    print("Difference: " + (v1 - v2).__str__())
    print("Scalar multiplication: " + (v1*s).__str__())
    print("Scalar division: " + (v1/s).__str__())
    dot = v1*v2
    print(f"Dot product: {dot}" )
    