import maya.api.OpenMaya as om
import maya.cmds as cmds

cube1 = cmds.ls('pCube1')
cube2 = cmds.ls('pCube2')
cube1_global_transform = om.MMatrix(cmds.xform(cube1,q=True, matrix=True, ws=True))
cube2_global_transform = om.MMatrix(cmds.xform(cube2,q=True, matrix=True, ws=True))
cube2_local_transform = om.MMatrix(cmds.xform(cube2,q=True, matrix=True, r=True))

basis_x = om.MVector(cube1_global_transform.getElement(0,0), cube1_global_transform.getElement(0,1), cube1_global_transform.getElement(0,2))
basis_y = om.MVector(cube1_global_transform.getElement(1,0), cube1_global_transform.getElement(1,1), cube1_global_transform.getElement(1,2))
basis_z = om.MVector(cube1_global_transform.getElement(2,0), cube1_global_transform.getElement(2,1), cube1_global_transform.getElement(2,2))


local_translate = om.MVector(cube2_local_transform.getElement(3,0), cube2_local_transform.getElement(3,1), cube2_local_transform.getElement(3,2))

global_translate = om.MVector(cube2_global_transform.getElement(3,0), cube2_global_transform.getElement(3,1), cube2_global_transform.getElement(3,2))

print "Local: "+ str(local_translate)
print local_translate.x * basis_x + local_translate.y * basis_y + local_translate.z * basis_z
print global_translate