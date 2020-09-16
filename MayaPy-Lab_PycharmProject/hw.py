import maya.api.OpenMaya as om
import maya.cmds as cmds
import math


def build_water_plane():
    return cmds.polyPlane(n = "WaterPlane", sw = 20, sh = 20, w = 10, h = 10)

def wave(point, flow_dir, amp, freq, time):
    p = om.MVector(point.x,0,point.z)
    d = om.MVector(flow_dir.x,0,flow_dir.z).normal()
    f = (p*d)*freq+time/120
    p.x = amp*d.x*math.cos(f)
    p.z = amp*d.z*math.cos(f)
    p.y = amp * math.sin(f)

    return p



def deform_point(time, point):
    # write your fancy deformation code here!

    dir1 = om.MVector(0.47, 0, 0.35)
    dir2 = om.MVector( -0.96, 0,  0.23)
    dir3 = om.MVector(0.77, 0, -1.47)
    dir4 = om.MVector(-0.3, 0, -0.2)

    point += wave(point, dir1, 0.016, 0.4, time*20)
    point += wave(point, dir2, 0.024, 1.8, time*30)
    point += wave(point, dir3, 0.028, 1.0, time*10)
    point += wave(point, dir4, 0.036, 1.2, time*30)

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
            mfnMesh.setVertexColor(vertCol,index)
        cmds.setKeyframe(object_name, t=frame, at='pnts')


try:
    cmds.delete(mesh)
except:
    pass

mesh = build_water_plane()
set_animation(mesh[0], 120)


