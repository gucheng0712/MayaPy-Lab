import maya.api.OpenMaya as om
import maya.cmds as cmds
import random

sel_name = cmds.ls(sl=True)[0]
selection = om.MSelectionList()
selection.add(sel_name)
nodeDagPath = selection.getDagPath(0)
mfnMesh = om.MFnMesh(nodeDagPath)

for vertId in range(mfnMesh.numVertices):
    col = om.MColor([random.random(), random.random(), random.random(), 1])
    mfnMesh.setVertexColor(col, vertId)