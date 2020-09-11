import maya.api.OpenMaya as om

vec1 = om.MVector(4,4,0)
vec3 = om.MVector(-1,4,0)
vec4 = vec1 + vec3
print vec4