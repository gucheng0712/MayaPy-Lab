import maya.api.OpenMaya as om
import maya.cmds as cmds

sel_name = cmds.ls(sl=True)[0]
selection = om.MSelectionList()
selection.add(sel_name)
nodeDagPath = selection.getDagPath(0)
mfnMesh = om.MFnMesh(nodeDagPath)

for vertId in range(mfnMesh.numVertices):
    vtPos = mfnMesh.getPoint(vertId, space=om.MSpace.kWorld) # kWorld for world
    n = om.MVector(vtPos.x, vtPos.y, vtPos.z).normalize()
    # do not use setFaceVertexNormal, since we don't need unshared normal per vertex
    mfnMesh.setVertexNormal(n, vertId)