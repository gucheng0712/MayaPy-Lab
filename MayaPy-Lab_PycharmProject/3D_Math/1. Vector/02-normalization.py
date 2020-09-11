
import maya.api.OpenMaya as om
import math

vec1 = om.MVector(4,4,0)
vec2 = om.MVector(3,3,0)
vec3 = om.MVector(-1,4,0)

print "\tsqrt(x^2 + y^2 + z^2) is \t{0}".format(math.sqrt(vec1.x**2 + vec1.y**2 + vec1.z**2))
print "\tLength of vec1 is \t\t\t{0}".format(vec1.length())
vec1_norm = vec1.normal()
print "\tNormalized vec1 is {0}, \n\t\tits length is {1}".format(vec1_norm, vec1_norm.length())