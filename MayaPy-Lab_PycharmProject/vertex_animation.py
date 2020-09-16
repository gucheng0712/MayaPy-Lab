import maya.api.OpenMaya as om
import maya.cmds as cmds
import math


def deform_point(time, point):
    time = time if time < 90 else 180 - time
    # construct translate
    th = 0 if time < 60 else (time / 30.0 - 2)
    ty = (1 - (1 - th) * (1 - th)) * 3
    # time to t parameter, where t = 0.5: original, t = 0: squash, t = 1: squeeze
    # t : 0.5 ~ 0, frame0-30; t:0~1, frame 30 - 90 
    t = 0.5 - time / 60.0 if time < 30 else time / 60.0 - 0.5
    # constuct sx and sy from t
    hmax = 1
    # sy: t=0.5, sy:1; t=0, sy:0.5; t=1, sy:1.5
    sy = t + 0.5
    # sx: t=0.5, sx:1; t=0, sx:1.5; t=1, sx:0.5
    sx = 1.5 - t
    # construct height based scale
    h_scale = (-math.cos(3.14 * abs(point.y)) * (t - 0.5) * 0.5 + 1)
    sx = h_scale * sx
    mat = om.MTransformationMatrix()
    mat.setScale([sx, sy, sx], om.MSpace.kObject)
    translation = om.MVector(0, ty, 0)
    mat.translateBy(translation, om.MSpace.kWorld)
    point = point * mat.asMatrix()
    return [point.x, point.y, point.z]


def set_animation(object_name, frames):
    selection = om.MSelectionList()
    selection.add(object_name)
    nodeDagPath = selection.getDagPath(0)
    mfnMesh = om.MFnMesh(nodeDagPath)
    points = mfnMesh.getPoints()

    for frame in range(frames):
        cmds.currentTime(frame)

        for index, p in enumerate(points):
            deform_p = deform_point(frame, p)
            cmds.xform("{0}.vtx[{1}]".format(object_name, index), t=deform_p, a=True, ws=True)

        cmds.setKeyframe(object_name, t=frame, at='pnts')


set_animation('pCube1', 120)

