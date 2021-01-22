import maya.api.OpenMaya as om
import maya.cmds as cmds

sel_name = cmds.ls(sl=True)[0]
selection = om.MSelectionList()
selection.add(sel_name)
nodeDagPath = selection.getDagPath(0)
mfnMesh = om.MFnMesh(nodeDagPath)

print mfnMesh.getPoints()
testP = om.MPoint(1,2,3)
mfnMesh.setPoint(0, testP)