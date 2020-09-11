import maya.api.OpenMaya as om

axis1 = om.MVector(1,0,0)
axis2 = om.MVector(0,1,0)
print axis1 ^ axis2
print axis2 ^ axis1

axis1 = om.MVector(0.707, 0.707, 0)
axis2 = om.MVector(0, 0, 1)
axis3 = axis1 ^ axis2
print axis3