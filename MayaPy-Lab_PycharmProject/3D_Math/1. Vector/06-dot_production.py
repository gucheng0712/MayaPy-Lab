import maya.api.OpenMaya as om

norm1 = om.MVector(1,0,0)
norm2 = om.MVector(2,3,1)
norm2.normalize()
dot_norm = norm1 * norm2
print dot_norm
print norm1.x*norm2.x + norm1.y*norm2.y + norm1.z*norm2.z
norm2_perpd = norm1 * dot_norm
print norm2_perpd