# coding = utf-8
import Red9.core.Red9_Meta as r9Meta
import maya.cmds as cmds

mClass = r9Meta.MetaClass(name = 'MetaClass_Test')
cube1 = cmds.ls(cmds.polyCube()[0],l = True)[0]
print(cube1)
cube2 = cmds.ls(cmds.polyCube()[0],l = True)[0]
cube3 = cmds.ls(cmds.polyCube()[0],l = True)[0]

# connect cube1 to mClass
mClass.connectChild(cube1,'CubeA')
# connect cube2 and cube3 to mClass
mClass.connectChildren([cube2,cube3],'Cubes')

