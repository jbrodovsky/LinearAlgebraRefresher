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
    
    def __repr__(self):
        return self.__str__()
    
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
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __rsub__(self, v):
        assert self.dimension == v.dimension, "Cannot add vectors of differing dimentions"
        new_coords = [y-x for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coords)
    
    def __neg__(self):
        new_coords = [-x for x in self.coordinates]
        return Vector(new_coords)        
        
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
        assert isinstance(v, Vector) and self.dimension == v.dimension, "Can only calculate the angle between vectors of the same number of dimensions"
        dot = self * v
        mag = self.magnitude() * v.magnitude()
        return math.acos(dot / mag)
    
    def check_parallel(self, v):
        angle = self.get_angle(v)
        return angle == 0.0 or angle == math.pi
    
    def check_orthogonal(self, v):
        angle = self.get_angle(v)
        return angle == math.pi/2 or angle == -math.pi/2 or angle == 3*math.pi/2 or angle == -3*math.pi/2
    
    def get_projection(self, v):
        # Project v onto self
        assert isinstance(v, Vector) and self.dimension == v.dimension, "Can only calculate the projection between vectors of the same number of dimensions"
        if self.check_orthogonal(v):
            new_coords = [0 for x in self.coordinates]
            return Vector(new_coords)
        else:
            mag = self.__mul__(v.direction())
            return self.direction() * mag
    
    def cross(self, v):
        # Must convert 2D vectors to 3D
        assert isinstance(v, Vector) and self.dimension>=2 and self.dimension == v.dimension, "Can only calculate the cross between vectors of the same number of dimensions"
        if self.dimension == 2:
            self.coordinates += (0, )
            self.dimension += 1
            v.coordinates += (0, )
            v.dimension += 1
        assert self.dimension <= 3, "Cross product only valid for 3D and 7D space; 7D calculation not implemented"
        x1, y1, z1 = self.coordinates
        x2, y2, z2 = v.coordinates
        new_coords = [y1*z2 - y2*z1,
                      -(x1*z2 - x2*z1),
                      x1*y2 - x2*y1]
        self.coordinates = self.coordinates[:2]
        v.coordinates = v.coordinates[:2]
        return Vector(new_coords)
    
if __name__ == '__main__':
    v1 = Vector([0,1])
    v2 = Vector([1,0])
    v3 = Vector([-1,0.25])
    s = 2
    print(v1)
    print(v2)
    print(v3)
    print(f"Scalar s: {s}")
    print("Sum: " + (v1 + v2).__str__())
    print("Difference: " + (v1 - v2).__str__())
    print("Scalar multiplication: " + (v1*s).__str__())
    print("Scalar division: " + (v1/s).__str__())
    dot = v1*v2
    print(f"Dot product: {dot}" )
    v1pv2 = v1.check_parallel(v2)
    v1pv1s = v1.check_parallel(v1*s)
    v1pv1n = v1.check_parallel(-v1)
    v1ov2 = v1.check_orthogonal(v2)
    v1ov1s = v1.check_orthogonal(v1*s)
    v1ov1n = v1.check_orthogonal(-v1)
    v1ov3 = v1.check_orthogonal(v3)
    print("Is Vector 1...")
    print(f"\tParallel to v2?\t{v1pv2}")
    print(f"\tParallel to v1 * s?\t{v1pv1s}")
    print(f"\tParallel to -v1?\t{v1pv1n}")
    print(f"\tOrthogonal to v2?\t{v1ov2}")
    print(f"\tOrthogonal to v1*s?\t{v1ov1s}")
    print(f"\tOrthogonal to -v1?\t{v1ov1n}")
    print(f"\tOrthogonal to v3?\t{v1ov3}")
    
    
    
    
    