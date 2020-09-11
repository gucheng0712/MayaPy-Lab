import maya.cmds as cmds
import maya.api.OpenMaya as om
import math
rot_angle = math.pi / 8
mat_rot   = om.MMatrix((\
                (math.cos(rot_angle), math.sin(rot_angle),0,0),\
                (math.sin(rot_angle),-math.cos(rot_angle),0,0),\
                (0,0,1,0),\
                (0,0,0,1)))
rot_angle = math.pi / 7
mat_rot2  = om.MMatrix((\
                (math.cos(rot_angle), 0,-math.sin(rot_angle),0),\
                (0,1,0,0),\
                (math.sin(rot_angle),0,-math.cos(rot_angle),0),\
                (0,0,0,1)))

#按不同顺序旋转的结果不同
print(mat_rot * mat_rot2) 
print(mat_rot2 * mat_rot)