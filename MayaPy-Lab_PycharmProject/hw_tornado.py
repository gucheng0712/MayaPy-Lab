import maya.api.OpenMaya as om
import maya.cmds as cmds



def deform_point(time, point):
    # write your fancy deformation code here!

    x = sin(point.y+time)
    z = sin(point.y+time)
    point.x+=x
    point.z+=z
    return [point.x, point.y, point.z]


def set_animation(object_name, frames):
    selection = om.MSelectionList()
    selection.add(object_name)
    nodeDagPath = selection.getDagPath(0)
    mfnMesh = om.MFnMesh(nodeDagPath)
    points = mfnMesh.getPoints()
    for frame in range(frames):
        for index, p in enumerate(points):
            deform_p = deform_point(frame, p)
            cmds.xform("{0}.vtx[{1}]".format(object_name, index), t=deform_p, a=True, ws=True)
        cmds.currentTime(frame)
        cmds.setKeyframe(object_name, t=frame, at='pnts')


set_animation('pCube1', 120)


