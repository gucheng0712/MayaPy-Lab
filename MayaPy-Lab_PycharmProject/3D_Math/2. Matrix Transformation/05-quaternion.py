import maya.api.OpenMaya as om
import maya.cmds as cmds

# show the difference between eular rotation and quaternion slerp

def rad2deg(rad):
    return rad * 180.0 / 3.14159265


def deg2rad(deg):
    return deg * 3.1415926 / 180.0


cube1 = cmds.ls("pCube1")[0]
cube2 = cmds.ls("pCube2")[0]

angle_start = om.MEulerRotation(0, 0, 0)
angle_end = om.MEulerRotation(deg2rad(60), deg2rad(80), deg2rad(90))
angle_start_quat = angle_start.asQuaternion()
angle_end_quat = angle_end.asQuaternion()

frame_length = 50

for i in range(0, frame_length + 1):
    frame = i + 1
    perc = i / float(frame_length)
    rot = angle_end * perc + angle_start * (1 - perc)
    cmds.setKeyframe(cube1 + '.rx', v=rad2deg(rot.x), t=frame)
    cmds.setKeyframe(cube1 + '.ry', v=rad2deg(rot.y), t=frame)
    cmds.setKeyframe(cube1 + '.rz', v=rad2deg(rot.z), t=frame)
    rot_quat = om.MQuaternion.slerp(angle_start_quat, angle_end_quat, perc)
    rot = rot_quat.asEulerRotation()
    cmds.setKeyframe(cube2 + '.rx', v=rad2deg(rot.x), t=frame)
    cmds.setKeyframe(cube2 + '.ry', v=rad2deg(rot.y), t=frame)
    cmds.setKeyframe(cube2 + '.rz', v=rad2deg(rot.z), t=frame)