# https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__py_ref_class_open_maya_1_1_m_matrix_html

import maya.api.OpenMaya as om
import maya.cmds as cmds
import math

# translate by (2,3,2)
mat_trans = om.MMatrix((
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (2, 4, 2, 1)
))

# rotate along z 30 degree
rot_angle = math.pi / 6
mat_rot = om.MMatrix((
    (math.cos(rot_angle), math.sin(rot_angle), 0, 0),
    (math.sin(rot_angle), -math.cos(rot_angle), 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1)
))

# scale by (3,2,1)
mat_scale = om.MMatrix((
    (3, 0, 0, 0),
    (0, 2, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1)
))

# create a cube at (0,0,0)
try:
    selected_object = cmds.select("MyCube")

except:
    cube = cmds.polyCube(n="MyCube")
    selected_object = cmds.select(cube)

selected_object_world_matrix = om.MMatrix(cmds.xform(selected_object, query=True, matrix=True, worldSpace=True))

# matrix RST (make sure is this order)
new_transform = selected_object_world_matrix * mat_scale * mat_rot * mat_trans
cmds.xform(selected_object, m=list(new_transform), ws=True)
# equal to
# cmds.xform( selected_object, ro=(0, 0, 30), t = (2,4,2), s = (3,2,1) )

# MPoint is homogenize vector, 4elements
point1 = om.MPoint(0, 0, 0, 1)
point1 = point1 * new_transform
print point1

# Inverse Matrix
mat1 = om.MMatrix(((1,0,0,0),(0,1,0,0),(0,0,1,0),(2,4,2,1)))
print mat1.inverse()
print mat1.inverse() * mat1

# Transpose Matrix
print mat1.transpose()