import maya.api.OpenMaya as om

norm1 = om.MVector(1,0,0)
norm2 = om.MVector(2,3,1)
norm2.normalize()
print norm1, norm2
print norm1.length(), norm2.length()

norm_interp = norm1 * 0.5 + norm2 * 0.5
print norm_interp
print norm_interp.length()
norm_interp.normalize()
print norm_interp
print norm_interp.length()