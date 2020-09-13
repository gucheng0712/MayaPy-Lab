# coding = utf-8
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import maya.cmds as cmds
import math
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

def maya_main_window():
    """
    keep this window always be front of maya's window
    """
    main_win_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_win_ptr), QWidget)


# dialog window
class WaveWidget(MayaQWidgetBaseMixin, QDialog):
    def __init__(self, parent=None):
        super(WaveWidget, self).__init__(parent)
        self.setWindowTitle("Wave Editor")
        self.setMinimumWidth(200)
        self.resize(200,300)
        # remove the question mark button in dialog by using XOR to exclude
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.waveTypeComboBox = QComboBox()
        self.waveTypeComboBox.addItems(["A","B","C"])

        pass

    def create_layouts(self):
        pass

    def create_connections(self):
        pass


if __name__ == "__main__":
    # prevent maya opens 2 instance of the window
    try:
        # noinspection PyUnresolvedReferences
        m_widget.close()
        # noinspection PyUnresolvedReferences
        m_widget.deleteLater()
    except:
        pass
    m_widget = WaveWidget()
    m_widget.show()
