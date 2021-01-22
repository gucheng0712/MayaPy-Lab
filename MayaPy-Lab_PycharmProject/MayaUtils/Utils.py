# coding = utf-8

def obj_vertex_painting(self, objToPaint, color):
    sel_obj = objToPaint
    selection = om.MSelectionList()
    selection.add(sel_obj)
    nodeDagPath = selection.getDagPath(0)
    mfnMesh = om.MFnMesh(nodeDagPath)
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')

    cmds.progressBar(gMainProgressBar,
                     edit=True,
                     beginProgress=True,
                     isInterruptable=True,
                     status='"VertexColor Painting ...',
                     maxValue=mfnMesh.numVertices)

    for vertId in range(mfnMesh.numVertices):
        if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True):
            break
        cmds.progressBar(gMainProgressBar, edit=True, step=1)
        col = om.MColor(color)
        mfnMesh.setVertexColor(col, vertId)

    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)


def findRoot(self, objType=""):
    """Find Root Joint"""
    rootObj = None
    if objType == "":
        print("No given type of root object")
        return None
    else:
        allObjs = cmds.ls(typ=objType)
        for obj in allObjs:
            parentObj = cmds.listRelatives(obj, parent=True, typ=objType)
            if not parentObj:
                rootObj = obj
    return rootObj


def bindSkinToJoint(self, joint, mesh):
    cmds.skinCluster(joint, mesh)


def getSkinClusterFromMesh(self, mesh):
    skinClusterStr2 = 'findRelatedSkinCluster("' + mesh + '")'
    return mel.eval(skinClusterStr2)