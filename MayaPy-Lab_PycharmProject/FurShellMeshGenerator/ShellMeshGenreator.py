# execfile("C:\\Users\\cgu2\\Documents\\Git Repository\\MayaPy-Lab\\MayaPy-Lab_PycharmProject\\FurShellMeshGenerator\\ShellMeshGenreator.py")


# coding = utf-8
from __future__ import division
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
from maya import cmds
import math
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

# main widget instance
def maya_main_window():
    """
    keep this window always be front of maya's window
    """
    main_win_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_win_ptr), QWidget)

class ShellGenerator(object):
    def __init__(self, layerAmount):
        self.layerAmount = layerAmount
        self.furStep =  1 / float(self.layerAmount)
        self.obj = cmds.ls(sl=True)[0]
        self.objsToCombine = []

    def generate(self):
        # Duplicate Objects
        for i in range(0,self.layerAmount+1):
            self.objsToCombine.append(cmds.duplicate(self.obj))
        # Vertex Painting
        for i in range(0,self.layerAmount+1):
            paintObj = self.objsToCombine[i][0]
            paintColor = [i * self.furStep, 0, 0, 1]
            self.__obj_vertex_painting(paintObj,paintColor,i)

        # Combine selected objects
        for o in self.objsToCombine:
            cmds.select(o, add=True)
        combinedObj = cmds.polyUnite()[0]

        mel.eval("cleanUpScene 3")  # clean up the scene unused objects
        cmds.delete(ch=True)  # remove history

        # set parent back after combined
        objParent = cmds.listRelatives(self.obj, parent=True)
        cmds.parent(combinedObj, objParent)

        # Find the Root Joint in the scene
        rig = self.__findRoot("joint")

        # Bind Skin and Joint
        self.__bind_skin_to_joint(rig, combinedObj)

        # Copy Skin Weight through skin cluster
        sourceCluster = self.__get_skin_cluster_from_mesh(self.obj)
        targetCluster = self.__get_skin_cluster_from_mesh(combinedObj)
        cmds.copySkinWeights(ss=sourceCluster, ds=targetCluster, noMirror=True)
        cmds.delete(self.obj)
        # rename object
        cmds.rename(combinedObj, self.obj)

    def __obj_vertex_painting(self, objToPaint,color,index=0):
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
                         status=str(index)+': VertexColor Painting ...',
                         maxValue=mfnMesh.numVertices)

        for vertId in range(mfnMesh.numVertices):
            if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True):
                break
            cmds.progressBar(gMainProgressBar, edit=True, step=1)
            col = om.MColor(color)
            mfnMesh.setVertexColor(col, vertId)

        cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)

    def __findRoot(self,objType=""):
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


    def __bind_skin_to_joint(self,joint, mesh):
        cmds.skinCluster(joint, mesh)


    def __get_skin_cluster_from_mesh(self,mesh):
        skinClusterStr2 = 'findRelatedSkinCluster("' + mesh + '")'
        return mel.eval(skinClusterStr2)



# dialog window
class MainWindow(QDialog):
    def __init__(self,  parent=maya_main_window()):
        super(MainWindow, self).__init__(parent)
        self.init_widgets()

    def init_widgets(self):
        """Init Widget components"""
        self.setWindowTitle("Shell Generator")
        self.setMinimumWidth(140)
        self.setMaximumWidth(140)
        self.setMinimumHeight(100)
        self.setMaximumHeight(100)
        # remove the question mark button in dialog by using XOR to exclude
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.__create_widgets()
        self.__create_layouts()
        self.__create_connections()

    def __create_widgets(self):
        self.generateShellLabel = QLabel("Shell Layer Amount")
        self.shellLayerSpinBox = QSpinBox()
        self.shellLayerSpinBox.setValue(5)
        self.shellLayerSpinBox.setMinimum(5)
        self.shellLayerSpinBox.setMaximum(100)
        self.generateShellBtn = QPushButton("Generate")

    def __create_layouts(self):
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.generateShellLabel)
        content_layout.addWidget(self.shellLayerSpinBox)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.generateShellBtn)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(content_layout)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)

    def __create_connections(self):
        self.generateShellBtn.clicked.connect(self.__generate_shell_btn_clicked)

    def __generate_shell_btn_clicked(self):
        print("Generate Fur Shell")
        self.shellGenerator = ShellGenerator(self.shellLayerSpinBox.value())
        self.shellGenerator.generate()



if __name__ == "__main__":
    # prevent maya opens 2 instance of the window
    try:
        # noinspection PyUnresolvedReferences
        m_widget.close()
        # noinspection PyUnresolvedReferences
        m_widget.deleteLater()
    except:
        pass

    m_widget = MainWindow()
    m_widget.show()

