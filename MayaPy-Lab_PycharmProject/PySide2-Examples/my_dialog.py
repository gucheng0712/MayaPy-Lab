# coding=utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


def maya_main_window():
    """
    keep this window always be front of maya's window
    """
    main_win_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_win_ptr), QtWidgets.QWidget)


# custom Line Edit
class MyLineEdit(QtWidgets.QLineEdit):
    enter_pressed = QtCore.Signal(str)  # Create a new signal

    def keyPressEvent(self, e):
        super(MyLineEdit, self).keyPressEvent(e)
        if e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit(self.text())  # emit the signal when key is pressed
        elif e.key() == QtCore.Qt.Key_Backspace:
            self.enter_pressed.emit(self.text() + "(Backspace)")


# Dialog Window
class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(MyDialog, self).__init__(parent)

        self.setWindowTitle("My Dialog")
        self.setMinimumWidth(200)

        # remove the question mark button in dialog by using XOR to exclude
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):

        # Line Edit
        self.lineEdit1 = QtWidgets.QLineEdit()
        self.lineEdit2 = QtWidgets.QLineEdit()
        self.my_lineEdit = MyLineEdit()

        # Check Box
        self.checkBox1 = QtWidgets.QCheckBox("Check Box 1 Label")
        self.checkBox2 = QtWidgets.QCheckBox("Check Box 2 Label")

        # ComboBox
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItems(["ComboBoxItem 1", "ComboBoxItem 2", "ComboBoxItem 3", "ComboBoxItem 4"])

        # Button
        self.button1 = QtWidgets.QPushButton("Button 1")
        self.button2 = QtWidgets.QPushButton("Button 2")
        self.button3 = QtWidgets.QPushButton("NonStretched Button 3")
        self.button4 = QtWidgets.QPushButton("NonStretched Button 4")

    def create_layouts(self):

        # Form Layout
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Combo Box:", self.comboBox)
        form_layout.addRow("LineEdit1:", self.lineEdit1)
        form_layout.addRow("LineEdit2:", self.lineEdit2)
        form_layout.addRow("Custom LineEdit:", self.my_lineEdit)
        form_layout.addRow("Check Box 1:", self.checkBox1)
        form_layout.addRow("Check Box 2:", self.checkBox2)

        # Horizontal Layout for Normal Buttons
        btn_layout_A = QtWidgets.QHBoxLayout()
        btn_layout_A.addWidget(self.button1)
        btn_layout_A.addWidget(self.button2)

        # Horizontal Layout for Stretched Buttons
        btn_layout_B = QtWidgets.QHBoxLayout()
        # add stretch before the btn to prevent rest widgets get streched
        btn_layout_B.addStretch()
        btn_layout_B.addWidget(self.button3)
        btn_layout_B.addWidget(self.button4)

        # Main Layout: Vertical Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout_A)
        main_layout.addLayout(btn_layout_B)

    def create_connections(self):
        self.lineEdit1.editingFinished.connect(self.on_lineEdit1_Finished)
        self.lineEdit2.textChanged.connect(self.on_lineEdit2_Changed)
        self.my_lineEdit.enter_pressed.connect(self.on_Custom_lineEdit_Finished)
        self.checkBox1.toggled.connect(self.on_checkBox1_Checked)
        self.checkBox2.toggled.connect(self.on_checkBox2_Checked)
        self.button1.clicked.connect(self.on_Btn1_Clicked)
        self.comboBox.activated.connect(self.on_activated_int)  # print index
        self.comboBox.activated[str].connect(self.on_activated_str)  # print str

    # <editor-fold desc="Slots">
    # =================== Slots =================== #
    def on_Btn1_Clicked(self):
        print("Button 1 Clicked")

    def on_checkBox1_Checked(self):
        checked = self.checkBox1.isChecked()
        if checked:
            print("Check Box 1 is Checked")
        else:
            print("Check Box 1 is Unchecked")

    def on_checkBox2_Checked(self, checked):
        # if passing param then no need to get bool from checkBox1.isChecked()
        if checked:
            print("Check Box 2 is Checked")
        else:
            print("Check Box 2 is Unchecked")

    def on_lineEdit1_Finished(self):
        print("Finished line edit text: {0}".format(self.lineEdit1.text()))

    def on_lineEdit2_Changed(self, name):
        # if passing param then no need to get the line edit text
        print("Changed line edit text: {0}".format(name))

    def on_Custom_lineEdit_Finished(self, name):
        print("Finished Custom line edit text: {0}".format(name))

    def on_activated_int(self, index):
        print("Combo Box Index: {0}".format(index))

    def on_activated_str(self, text):
        print("Combo Box Text: {0}".format(text))

    # </editor-fold>


if __name__ == "__main__":

    # prevent maya opens 2 instance of the window
    try:
        # noinspection PyUnresolvedReferences
        m_dialog.close()
        # noinspection PyUnresolvedReferences
        m_dialog.deleteLater()
    except:
        pass

    m_dialog = MyDialog()
    m_dialog.show()
