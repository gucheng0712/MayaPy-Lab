# https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__py_ref_class_open_maya_1_1_m_vector_html


# MVector is not a shape, you cannot visualize it 
# in viewport directly

import maya.api.OpenMaya as om

vec1 = om.MVector(4,4,0)
vec2 = om.MVector(3,3,0)
vec3 = om.MVector(-1,4,0)
print(vec1, vec2, vec3)