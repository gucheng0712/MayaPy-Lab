from __future__ import division
from collections import namedtuple
import math
import random

import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

from Qt import QtCore
from Qt import QtWidgets


def angledDetector(distance, angle):
    cosAngle = math.cos(angle / 180 * math.pi)

    def detector(boid1, boid2):
        toBoid2 = (boid1.position - boid2.position)
        if toBoid2.length() > distance:
            return False
        if boid1.velocity.normalized().dot(toBoid2.normalized()) > cosAngle:
            return False
        return True
    return detector


class Vec3(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super(Vec3, self).__init__()
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __sub__(self, other):
        return self + (-other)

    def length(self):
        return math.sqrt(self.dot(self))

    def normalize(self):
        length = self.length()
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length

    def normalizeTo(self, length):
        self.normalize()
        self *= length

    def normalized(self):
        length = self.length()
        if length != 0:
            return Vec3(self.x / length, self.y / length, self.z / length)
        return Vec3()

    def dot(self, other):
        return sum(self * other)

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        raise ValueError('Vec3 can only multiplies number or Vec3.')

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return self * (1 / other)
        raise ValueError('Vec3 can only divide number.')

    def __rtruediv__(self, other):
        if isinstance(other, (float, int)):
            return Vec3(other / self.x, other / self.y, other / self.z)
        raise ValueError('Only number can divide Vec3.')

    def __repr__(self):
        return 'Vec3({}, {}, {}, length={})'.format(self.x, self.y, self.z, self.length())


class Boid(object):
    def __init__(self, name):
        super(Boid, self).__init__()
        self.name = name
        self.position = Vec3(*cmds.getAttr('{}.translate'.format(name))[0])
        self.velocity = Vec3(*cmds.getAttr('{}.velocity'.format(name))[0])
        self.force = Vec3()

    def addForce(self, force):
        self.force += force

    def applyForce(self):
        self.velocity += self.force
        self.force = Vec3()
        cmds.setAttr('{}.velocity'.format(self.name), self.velocity.x, self.velocity.y, self.velocity.z, type='double3')

    def applyVelocity(self):
        self.position += self.velocity
        cmds.move(self.position.x, self.position.y, self.position.z, self.name, relative=False)

    def limitVelocity(self, low, high):
        currentLength = self.velocity.length()
        if currentLength > high:
            self.velocity.normalizeTo(high)
        elif currentLength < low:
            self.velocity.normalizeTo(low)

    def attract(self, position, multiplier):
        self.addForce((position - self.position) * multiplier)

    def avoid(self, neighbours, multiplier):
        for other in neighbours:
            self.addForce(1 / (self.position - other.position) * multiplier)

    def align(self, neighbours, factor):
        if not neighbours:
            return
        vels = []
        for other in neighbours:
            vels.append(other.velocity.normalized())
        length = self.velocity.length()
        # this should be slerp instead of lerp
        direction = self.velocity.normalized() * (1 - factor) + sum(vels, Vec3()).normalized() * factor
        self.velocity = direction * length

    def followCenter(self, neighbours, multiplier):
        if not neighbours:
            return
        poss = []
        for other in neighbours:
            poss.append(other.position)
        center = sum(poss, Vec3()) / len(neighbours)
        self.addForce((center - self.position) * multiplier)

    def applyBorder(self, low, high):
        while self.position.x < low.x:
            self.position.x += (high.x - low.x)
        while self.position.y < low.y:
            self.position.y += (high.y - low.y)
        while self.position.z < low.z:
            self.position.z += (high.z - low.z)
        while self.position.x > high.x:
            self.position.x -= (high.x - low.x)
        while self.position.y > high.y:
            self.position.y -= (high.y - low.y)
        while self.position.z > high.z:
            self.position.z -= (high.z - low.z)


def clamp(value, minimum, maximum):
    return max(min(value, maximum), minimum)


class AutoRangeSlider(QtWidgets.QSlider):
    resized = QtCore.Signal()

    def resizeEvent(self, event):
        super(AutoRangeSlider, self).resizeEvent(event)
        w = event.size().width()
        self.setMaximum(w)
        self.resized.emit()


class OptionWidget(QtWidgets.QWidget):

    def value(self):
        raise NotImplementedError()


class FloatOptionWidget(OptionWidget):
    def __init__(self, minimum=0, maximum=100.0, default=None, clamp=False, parent=None):
        super(FloatOptionWidget, self).__init__(parent=parent)
        self._minimum = minimum
        self._maximum = maximum
        self._range = maximum - minimum
        self._clamp = clamp
        self._setupUI()
        self._connectSignals()
        self.setValue(default if default is not None else self._minimum)
        self._setSpinBoxValue()
        self._setSliderValue()

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def _setupUI(self):
        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._slider = AutoRangeSlider(QtCore.Qt.Horizontal)
        self._layout.addWidget(self._slider)

        self._doubleSpinBox = QtWidgets.QDoubleSpinBox()
        self._doubleSpinBox.setMaximum(self._maximum if self._clamp else 1e9)
        self._doubleSpinBox.setMinimum(self._minimum)
        self._layout.addWidget(self._doubleSpinBox)

    def _connectSignals(self):
        self._slider.valueChanged.connect(self._sliderValueChangedSlot)
        self._slider.resized.connect(self._sliderResizedSlot)
        self._doubleSpinBox.valueChanged.connect(self._doubleSpinBoxValueChangedSlot)

    def _clampIfNecessary(self, value):
        if self._clamp:
            return clamp(value, self._minimum, self._maximum)
        return value

    def _setSpinBoxValue(self):
        self._doubleSpinBox.blockSignals(True)
        self._doubleSpinBox.setValue(self._value)
        self._doubleSpinBox.blockSignals(False)

    def _setSliderValue(self):
        t = (self._value - self._minimum) / self._range
        t = clamp(t, 0.0, 1.0)
        p = self._slider.minimum() + int((self._slider.maximum() - self._slider.minimum()) * t)
        self._slider.blockSignals(True)
        self._slider.setValue(p)
        self._slider.blockSignals(False)

    def _sliderResizedSlot(self):
        self._setSliderValue()

    def _sliderValueChangedSlot(self, value):
        t = (value - self._slider.minimum()) / (self._slider.maximum() - self._slider.minimum())
        newValue = self._minimum + t * self._range
        self.setValue(newValue)
        self._setSpinBoxValue()

    def _doubleSpinBoxValueChangedSlot(self, value):
        newValue = self._clampIfNecessary(value)
        self.setValue(newValue)
        self._setSliderValue()


class IntOptionWidget(OptionWidget):
    def __init__(self, minimum=0, maximum=100, default=None, clamp=False, parent=None):
        super(IntOptionWidget, self).__init__(parent=parent)
        self._minimum = minimum
        self._maximum = maximum
        self._range = maximum - minimum
        self._clamp = clamp
        self._setupUI()
        self._connectSignals()
        self.setValue(default if default is not None else self._minimum)
        self._setSpinBoxValue()
        self._setSliderValue()

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def _setupUI(self):
        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._slider.setMinimum(self._minimum)
        self._slider.setMaximum(self._maximum)
        self._layout.addWidget(self._slider)

        self._spinBox = QtWidgets.QSpinBox()
        self._spinBox.setMaximum(self._maximum if self._clamp else 1e9)
        self._spinBox.setMinimum(self._minimum)
        self._layout.addWidget(self._spinBox)

    def _connectSignals(self):
        self._slider.valueChanged.connect(self._sliderValueChangedSlot)
        self._spinBox.valueChanged.connect(self._spinBoxValueChangedSlot)

    def _setSpinBoxValue(self):
        self._spinBox.blockSignals(True)
        self._spinBox.setValue(clamp(self._value, self._minimum, self._maximum))
        self._spinBox.blockSignals(False)

    def _setSliderValue(self):
        self._slider.blockSignals(True)
        self._slider.setValue(self._value)
        self._slider.blockSignals(False)

    def _sliderValueChangedSlot(self, value):
        self.setValue(value)
        self._setSpinBoxValue()

    def _spinBoxValueChangedSlot(self, value):
        self.setValue(value)
        self._setSliderValue()


OPTION_WIDGET_CLASS_DICT = {
    'float': FloatOptionWidget,
    'int': IntOptionWidget,
}

Option = namedtuple('Option', ['name', 'label', 'valueType', 'detail'])


class BoidWidget(MayaQWidgetBaseMixin, QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(BoidWidget, self).__init__(parent=parent)
        self.stop = False
        self.simulating = False
        self._options = [
            Option('radius', 'Radius', 'float', {'minimum': 0.0, 'maximum': 100.0, 'default': 10.0}),
            Option('count', 'Count', 'int', {'minimum': 0, 'maximum': 200, 'default': 100, 'clamp': False}),
            Option('frame', 'Frame', 'int', {'minimum': 0, 'maximum': 200, 'default': 120, 'clamp': False}),
            Option('attract_multiplier', 'Attract', 'float', {
                   'minimum': 0.0, 'maximum': 1.0, 'default': 0.1, 'clamp': False}),
            Option('avoid_multiplier', 'Avoid', 'float', {'minimum': 0.0,
                                                          'maximum': 1.0, 'default': 0.1, 'clamp': False}),
            Option('follow_multiplier', 'Follow', 'float', {
                   'minimum': 0.0, 'maximum': 1.0, 'default': 0.3, 'clamp': False}),
            Option('align_factor', 'Align', 'float', {'minimum': 0.0, 'maximum': 1.0, 'default': 0.3}),
            Option('min_velocity', 'Minimum Velocity', 'float', {
                   'minimum': 0.0, 'maximum': 10.0, 'default': 0.1, 'clamp': False}),
            Option('max_velocity', 'Maximum Velocity', 'float', {
                   'minimum': 0.0, 'maximum': 10.0, 'default': 3.0, 'clamp': False}),
            Option('detect_distance', 'Detect Distance', 'float', {
                   'minimum': 0.0, 'maximum': 30.0, 'default': 15.0, 'clamp': False}),
            Option('detect_angle', 'Detect Angle', 'float', {
                   'minimum': 0.0, 'maximum': 180.0, 'default': 120.0, 'clamp': True}),
        ]
        self._optionWidgets = {}
        self._setupUI()
        self._connectSignals()
        self.setWindowTitle('Boids')
        self.resize(600, 600)

    def _setupUI(self):
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self._optionsLayout = QtWidgets.QFormLayout()
        self._layout.addLayout(self._optionsLayout)

        for option in self._options:
            optionWidget = OPTION_WIDGET_CLASS_DICT[option.valueType](**(option.detail))
            self._optionWidgets[option.name] = optionWidget
            self._optionsLayout.addRow(option.label, optionWidget)

        self._buttonsLayout = QtWidgets.QHBoxLayout()
        self._layout.addLayout(self._buttonsLayout)

        self._resetButton = QtWidgets.QPushButton('Reset')
        self._buttonsLayout.addWidget(self._resetButton)

        self._generateButton = QtWidgets.QPushButton('Generate')
        self._buttonsLayout.addWidget(self._generateButton)

        self._simulateButton = QtWidgets.QPushButton('Simulate')
        self._buttonsLayout.addWidget(self._simulateButton)

        self._runButton = QtWidgets.QPushButton('Run')
        self._buttonsLayout.addWidget(self._runButton)

        self._stopButton = QtWidgets.QPushButton('Stop')
        self._buttonsLayout.addWidget(self._stopButton)

    def getOptionValue(self, name):
        return self._optionWidgets[name].value()

    def _connectSignals(self):
        self._resetButton.clicked.connect(self._resetButtonClickedSlot)
        self._generateButton.clicked.connect(self._generateButtonClickedSlot)
        self._runButton.clicked.connect(self._runButtonClickedSlot)
        self._simulateButton.clicked.connect(self._simulateButtonClickedSlot)
        self._stopButton.clicked.connect(self._stopButtonClickedSlot)

    def _resetButtonClickedSlot(self):
        boids = cmds.ls('boid*', type='transform')
        if boids:
            cmds.delete(boids)
        if cmds.currentTime(query=True) != 1:
            cmds.currentTime(1, edit=True)

    def _generateButtonClickedSlot(self):
        count = self.getOptionValue('count')
        radius = self.getOptionValue('radius')
        for i in range(count):
            boid = cmds.polyCube(w=1, h=1, d=1)[0]
            boid = cmds.rename(boid, 'boid')
            length = radius * random.uniform(0, 1)
            radXZ = 2 * math.pi * random.uniform(0, 1)
            radY = math.pi * random.uniform(-1, 1)
            xn = math.sin(radXZ) * math.cos(radY)
            yn = math.cos(radXZ) * math.cos(radY)
            zn = math.sin(radY)
            x = xn * length
            y = yn * length
            z = zn * length
            cmds.move(x, y, z, boid)
            cmds.addAttr(boid, longName="velocity", attributeType='double3')
            cmds.addAttr(boid, longName="velocityX", attributeType='double', p='velocity')
            cmds.addAttr(boid, longName="velocityY", attributeType='double', p='velocity')
            cmds.addAttr(boid, longName="velocityZ", attributeType='double', p='velocity')
            cmds.setAttr('{}.velocity'.format(boid), xn, yn, zn, type='double3')
            cmds.polyColorPerVertex(
                boid,
                r=random.uniform(0, 1),
                g=random.uniform(0, 1),
                b=random.uniform(0, 1),
                a=1,
                colorDisplayOption=True
            )

    def _simulateButtonClickedSlot(self):
        self.simulate(frames=self.getOptionValue('frame'))

    @property
    def attractMultiplier(self):
        return self._attractMultiplier

    def simulateSingleFrame(self, boids, detector, update=True):
        QtWidgets.QApplication.instance().processEvents()
        # selection = set(cmds.ls(selection=True, long=True, type='transform') or [])
        detector = angledDetector(
            distance=self.getOptionValue('detect_distance'),
            angle=self.getOptionValue('detect_angle')
        )
        for boid in boids:
            # force based
            boid.attract(Vec3(), self.getOptionValue('attract_multiplier'))

            neighbours = [other for other in boids if other is not boid and detector(boid, other)]
            boid.avoid(neighbours, multiplier=self.getOptionValue('avoid_multiplier'))
            boid.followCenter(neighbours, multiplier=self.getOptionValue('follow_multiplier'))
            boid.applyForce()

            # velocity based
            boid.align(neighbours, factor=self.getOptionValue('align_factor'))

            boid.limitVelocity(
                self.getOptionValue('min_velocity'),
                self.getOptionValue('max_velocity')
            )
            boid.applyVelocity()

            # boid.applyBorder(Vec3(-30, -30, -30), Vec3(30, 30, 30))
            if update:
                cmds.setKeyframe('{}.translate'.format(boid.name))

    def _runButtonClickedSlot(self):
        self.simulate(False)

    def simulate(self, update=True, frames=-1):
        self.simulating = True
        boids = [Boid(name) for name in cmds.ls('boid*', type='transform', long=True)]
        time = cmds.currentTime(query=True)

        def infinite():
            while True:
                yield None

        for _ in (range(frames) if frames > 0 else infinite()):
            print(frames)
            if self.stop:
                self.stop = False
                break
            self.simulateSingleFrame(boids, update)
            if update:
                time += 1
                cmds.currentTime(time, edit=True)
            else:
                cmds.refresh()

        self.simulating = False

    def _stopButtonClickedSlot(self):
        if self.simulating:
            self.stop = True


def main():
    widget = BoidWidget()
    widget.show()


if __name__ == '__main__':
    main()
