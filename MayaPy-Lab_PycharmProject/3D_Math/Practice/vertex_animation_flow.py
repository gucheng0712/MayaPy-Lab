# coding = utf-8
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import maya.cmds as cmds
import math
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


# main widget instance
def maya_main_window():
    """
    keep this window always be front of maya's window
    """
    main_win_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_win_ptr), QWidget)


class WaveSimulation(object):
    def __init__(self):
        self.meshObj = None
        self.simulating = False
        self.stop = False

        self.__amp = 0.5
        self.__freq = 0.5
        self.__spd = 0.5

    def set_amplitude(self, val):
        self.__amp = val

    def set_frequency(self, val):
        self.__freq = val

    def set_speed(self, val):
        self.__spd = val

    def build_mesh(self):
        """Create the water plane mesh"""
        if self.meshObj is None:
            self.reset()

        self.meshObj = cmds.polyPlane(n="WavePlane", sw=10, sh=10, w=20, h=20)
    def subdiv_mesh(self):
        if self.meshObj is None:
            return
        cmds.polySubdivideFacet(n = self.meshObj[0],dv = 1)

    def simulate(self, keyFrame=False, frames=-1):
        """play the animation"""
        if self.meshObj is None:
            return

        # Start simulation
        self.simulating = True

        # get points position from selection object
        selection = om.MSelectionList()
        selection.add(self.meshObj[0])
        nodeDagPath = selection.getDagPath(0)
        mfnMesh = om.MFnMesh(nodeDagPath)
        points = mfnMesh.getPoints()

        # check if should insert keyframe
        if keyFrame:
            self.simulate_with_keyframe(frames=frames, points=points)
        else:
            self.simulate_without_keyframe(points=points)

        # End Simulation
        self.simulating = False

    def simulate_with_keyframe(self, frames, points):
        """simulate and set keyframe"""
        for frame in range(frames):
            # update the time in the timeline
            cmds.currentTime(frame, edit=True)

            # break the loop if stop playing the preview
            if self.stop:
                self.stop = False
                break
            # traversal all points
            for index, p in enumerate(points):
                deform_p = self.deform_point(time=frame, point=p)
                cmds.xform("{0}.vtx[{1}]".format(self.meshObj[0], index), t=deform_p, a=True, ws=True)
            # insert keyframe
            cmds.setKeyframe(self.meshObj[0], t=frame, at="pnts")

    def simulate_without_keyframe(self, points):
        """ simulation without setting keyframes """
        frame = cmds.currentTime(q=True)  # get current timeline key position

        def infinite():
            while True:
                yield None

        # a infinite for loop
        for _ in infinite():
            frame += 1
            # break the loop if stop playing the preview
            if self.stop:
                self.stop = False
                break
            # traversal all points
            for index, p in enumerate(points):
                deform_p = self.deform_point(frame, p)
                cmds.xform("{0}.vtx[{1}]".format(self.meshObj[0], index), t=deform_p, a=True, ws=True)

            # force a redraw during script execution
            cmds.refresh()

    def deform_point(self, time, point):
        """per vertex operation"""

        # direction of the wave
        dir1 = om.MVector(0.47, 0, 0.35)
        dir2 = om.MVector(-0.96, 0, 0.23)
        dir3 = om.MVector(0.77, 0, -1.47)
        dir4 = om.MVector(-0.3, 0, -0.2)

        # overlay calculation
        point += self.wave(point, dir1, 0.016 * self.__amp, 0.8 * self.__freq, time * 20 * self.__spd)
        point += self.wave(point, dir4, 0.036 * self.__amp, 2.4 * self.__freq, time * 30 * self.__spd)
        point += self.wave(point, dir2, 0.024 * self.__amp, 3.6 * self.__freq, time * 30 * self.__spd)
        point += self.wave(point, dir3, 0.028 * self.__amp, 2.0 * self.__freq, time * 10 * self.__spd)

        return [point.x, point.y, point.z]

    def wave(self, point, flow_dir, amp, freq, time):
        """general gerstner wave calculation"""
        p = om.MVector(point.x, 0, point.z)
        d = om.MVector(flow_dir.x, 0, flow_dir.z).normal()
        f = (p * d) * freq + time / 120
        p.x = amp * d.x * math.cos(f)
        p.z = amp * d.z * math.cos(f)
        p.y = amp * math.sin(f)

        return p

    def stop_preview(self):
        if self.meshObj is None:
            return
        """stop playing the animation preview """
        if self.simulating:
            self.stop = True

    def reset(self):
        if self.meshObj is None:
            return
        cmds.select(all=True)
        cmds.delete()
        self.build_mesh()


# dialog window
class WaveWidget(MayaQWidgetBaseMixin, QDialog):
    def __init__(self, parent=None):
        super(WaveWidget, self).__init__(parent)
        # init WaveSimulation
        self.wave = WaveSimulation()

        self.init_widgets()

    def init_widgets(self):
        """Init Widget components"""
        self.setWindowTitle("Wave Editor")
        self.setMinimumWidth(200)
        self.resize(200, 300)
        # remove the question mark button in dialog by using XOR to exclude
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.__create_widgets()
        self.__create_layouts()
        self.__create_connections()

    def get_wave_amplitude(self):
        return self.ampSlider.value() / 100.0

    def get_wave_frequency(self):
        return self.freqSlider.value() / 100.0

    def get_wave_speed(self):
        return self.spdSlider.value() / 100.0

    def __build_property_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.resize(200, 30)
        slider.setValue(50)
        slider.setRange(1, 100)
        return slider

    def __create_widgets(self):
        self.ampSlider = self.__build_property_slider()
        self.spdSlider = self.__build_property_slider()
        self.freqSlider = self.__build_property_slider()

        self.generateWaterPlaneBtn = QPushButton("Generate Water Plane")
        self.addDivitionsBtn = QPushButton("Add Divisions")
        self.simulateBtn = QPushButton("Simulate")
        self.playPreviewBtn = QPushButton("Play Preview")
        self.stopPreviewBtn = QPushButton("Stop Preview")
        self.resetBtn = QPushButton("Reset")

    def __create_layouts(self):
        form_layout = QFormLayout()
        form_layout.addRow("Wave Amplitude: ", self.ampSlider)
        form_layout.addRow("Wave Speed: ", self.spdSlider)
        form_layout.addRow("Wave Frequency: ", self.freqSlider)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.generateWaterPlaneBtn)
        btn_layout.addWidget(self.addDivitionsBtn)
        btn_layout.addWidget(self.resetBtn)
        btn_layout.addWidget(self.playPreviewBtn)
        btn_layout.addWidget(self.stopPreviewBtn)
        btn_layout.addWidget(self.simulateBtn)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

    def __create_connections(self):
        self.ampSlider.valueChanged.connect(self.__amplitudeChanged)
        self.spdSlider.valueChanged.connect(self.__speedChanged)
        self.freqSlider.valueChanged.connect(self.__frequencyChanged)

        self.generateWaterPlaneBtn.clicked.connect(self.__generate_water_plane_btn_clicked)
        self.addDivitionsBtn.clicked.connect(self.__add_division_btn_clicked)
        self.simulateBtn.clicked.connect(self.__simulate_btn_clicked)
        self.playPreviewBtn.clicked.connect(self.__play_preview_btn_clicked)
        self.stopPreviewBtn.clicked.connect(self.__stop_preview_btn_clicked)
        self.resetBtn.clicked.connect(self.__reset_btn_clicked)

    def __amplitudeChanged(self):
        print(self.get_wave_amplitude())
        self.wave.set_amplitude(self.get_wave_amplitude())

    def __speedChanged(self):
        print(self.get_wave_speed())
        self.wave.set_speed(self.get_wave_speed())

    def __frequencyChanged(self):
        print(self.get_wave_frequency())
        self.wave.set_frequency(self.get_wave_frequency())

    def __generate_water_plane_btn_clicked(self):
        print("Generate Water Plane")
        self.wave.build_mesh()

    def __add_division_btn_clicked(self):
        print("Add Divisions")
        self.wave.subdiv_mesh()

    def __simulate_btn_clicked(self):
        print("Simulate")
        self.wave.simulate(keyFrame=True, frames=120)

    def __play_preview_btn_clicked(self):
        print("Play preview")
        self.wave.simulate(keyFrame=False)

    def __stop_preview_btn_clicked(self):
        print("Stop Preview")
        self.wave.stop_preview()

    def __reset_btn_clicked(self):
        print("Reset")
        self.wave.stop_preview()
        self.wave.reset()


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
