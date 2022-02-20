import math

from decimal import Decimal, getcontext, InvalidOperation
getcontext().prec = 30

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
        if isinstance(v, int) or isinstance(v, float) or isinstance(v, Decimal):
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
    
    def is_zero(self):
        tf = [i==0 for i in self.coordinates]
        return all(tf)
    
class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2
        if not isinstance(normal_vector, Vector):
            normal_vector = Vector(normal_vector)
        if not normal_vector:
            #all_zeros = ['0']*self.dimension
            all_zeros = [0 for i in range(self.dimension)]
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector
        if not constant_term:
            constant_term = float(0)
        self.constant_term = float(constant_term)
        self.set_basepoint()

    def set_basepoint(self):
        try:
            n = self.normal_vector.coordinates
            c = self.constant_term
            basepoint_coords = [0 for i in range(self.dimension)]
            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]
            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)
        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    def __str__(self):
        num_decimal_places = 3
        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)
            output = ''
            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'
            if not is_initial_term:
                output += ' '
            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))
            return output

        n = self.normal_vector.coordinates
        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)
        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e
        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output
    
    def __repr__(self):
        return self.__str__()
    
    def is_parallel_to(self, line):
        assert isinstance(line, Vector) or isinstance(line, Line), 'Must check with respect to line or vector'
        if isinstance(line, Vector):
            n2 = line
        else:
            n2 = line.normal_vector
        return self.normal_vector.check_parallel(n2)
    
    def is_orthogonal_to(self, line):
        assert isinstance(line, Vector) or isinstance(line, Line), 'Must check with respect to line or vector'
        if isinstance(line, Vector):
            n2 = line
        else:
            n2 = line.normal_vector
        return self.normal_vector.check_orthogonal(n2)
    
    def __eq__(self, line):
        if not isinstance(line, Line):
            return False
        if self.normal_vector.is_zero():
            if not line.normal_vector.is_zero():
                return False
            else:
                diff = self.constant_term - line.constant_term
                return MyDecimal(diff).is_near_zero()
        elif line.normal_vector.is_zero():
            return False        
        if not self.is_parallel_to(line):
            return False
        else:
            basepoint_difference = self.basepoint - line.basepoint
            if basepoint_difference.is_zero():
                return True
            else:
                return basepoint_difference.check_orthogonal(self.normal_vector)     
        
    def intersection_with(self, line):
        assert isinstance(line, Line), 'Must compare to another line'
        try:
            A, B = self.normal_vector.coordinates
            C, D = line.normal_vector.coordinates
            x = D*self.constant_term - B*self.constant_term
            y = -C*self.constant_term + A*self.constant_term
            denom = A*D - B*C
            V = Vector([x,y])
            return V / denom
        except ZeroDivisionError:
            if self == line:
                return self
            else:
                return None
        except InvalidOperation:
            print("CAUGHT!")
            if self == line:
                return self
            else:
                return None
        
    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
    
if __name__ == '__main__':
    # Vector problems
    print("--------- Vector Problems ---------")
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
    # Line problems
    print("--------- Line Problems ---------")
    l1 = Line(v1, 10)
    l2 = Line(v2, 0)
    l3 = Line(v3, 0)
    l4 = Line(3*v1, 0)
    print("Line 1: ", l1)
    print("Line 2: ", l2)
    print("Line 3: ", l3)
    print("Line 4: ", l4)
    l1pl1 = l1.is_parallel_to(l1)
    l1pl2 = l1.is_parallel_to(l2)
    l1pl3 = l1.is_parallel_to(l3)
    l1pl4 = l1.is_parallel_to(l4)
    l1ol1 = l1.is_orthogonal_to(l1)
    l1ol2 = l1.is_orthogonal_to(l2)
    l1ol3 = l1.is_orthogonal_to(l3)
    l1ol4 = l1.is_orthogonal_to(l4)
    l1il1 = l1.intersection_with(l1)
    l1il2 = l1.intersection_with(l2)
    l1il3 = l1.intersection_with(l3)
    l1il4 = l1.intersection_with(l4)
    l1eql1 = l1==l1
    l1eql2 = l1==l2
    l1eql3 = l1==l3
    l1eql4 = l1==l4
    print("Is Line 1...")
    print(f"\tParallel to line 1?\t{l1pl1}")
    print(f"\tParallel to line 2?\t{l1pl2}")
    print(f"\tParallel to line 3?\t{l1pl3}")
    print(f"\tParallel to line 4?\t{l1pl4}")
    print(f"\tOrthogonal to line 1?\t{l1ol1}")
    print(f"\tOrthogonal to line 2?\t{l1ol2}")
    print(f"\tOrthogonal to line 3?\t{l1ol3}")
    print(f"\tOrthogonal to line 4?\t{l1ol4}")    
    print(f"\tEqual to Line 1? {l1eql1}")
    print(f"\tEqual to Line 2? {l1eql2}")
    print(f"\tEqual to Line 2? {l1eql3}")
    print(f"\tEqual to Line 2? {l1eql4}")
    print("Where does Line 1 intersect with...")
    print(f"\tLine 1: {l1il1}")
    print(f"\tLine 2: {l1il2}")
    print(f"\tLine 3: {l1il3}")
    print(f"\tLine 4: {l1il4}")