# -*- coding: utf-8 -*-

# ===============================================================
# Basic MetaClass Use:
# ===============================================================

import Red9.core.Red9_Meta as r9Meta
import maya.cmds as cmds

# make a new blank meta Class MayaNode
node = r9Meta.MetaClass(name="CustomMetaData")
node.select()

'''
If a Maya node is passed in and it has the mClass attribute of a class
thats known then the following call with return the correct class object.

NOTE: there's a global RED9_META_REGISTERY which holds registered mClasses
found at start using itersubclasses, called in the r9Meta.registerMClassInheritanceMapping()
'''
new = r9Meta.MetaClass(cmds.ls(sl=True)[0])
print(type(new))  # >> <class 'Red9_Meta.MetaClass'>
print(r9Meta.RED9_META_REGISTERY)

cmds.polyCube(name="MyCube")
# get the pCube1's maya node as a meta class object
myCubeNode = r9Meta.MetaClass("MyCube")

'''
Attribute Handling
===============================================================
Attribute management for the node. If no type flag is passed in
then the code automatically figures what attrType to add from the
given value.
'''

# ======Standard Attribute Handling====== #
myCubeNode.addAttr('intTest', 3)
myCubeNode.addAttr('floatTest', 1.333)
myCubeNode.addAttr('doubleTest', value=1.123545, attrType='double')  # require specify attrType
myCubeNode.addAttr('floatTestWithMinMax', 2.0, hidden=False, min=0, max=10)
myCubeNode.addAttr('stringTest', "this_is_a_string")
myCubeNode.addAttr('boolTest', False)
myCubeNode.addAttr('float3_Test', value=(1.22, 1.33, 10.21), attrType='float3')
myCubeNode.addAttr('double3_Test', value=(1.121222, 1.332233, 10.232321), attrType='double3', min=1, max=15,
                   hidden=False)

print(myCubeNode.intTest)  # >> 3
myCubeNode.intTest = 10  # set back to the MayaNode
print(myCubeNode.intTest)  # >> 10

print(myCubeNode.floatTest)  # >> 1.333
myCubeNode.floatTest = 3.55
print(myCubeNode.floatTest)  # >> 3.55

print(myCubeNode.stringTest)  # >>'this_is_a_string'
myCubeNode.stringTest = "change the text"
print(myCubeNode.stringTest)  # >>change the text

print(myCubeNode.boolTest)  # >>False
myCubeNode.boolTest = True  # set back to the MayaNode
print(myCubeNode.boolTest)  # >>True

# ===== Enum Attribute Handling ===== #
# need to specify the attrType
# settable via the string or the index
myCubeNode.addAttr('enum', enumName='A:B:C:D:E:F', attrType='enum')
myCubeNode.enum = 'A'
print(myCubeNode.enum)  # >> 0 always returns the actual index
myCubeNode.enum = 2
print(myCubeNode.enum)  # >> 2

# ===== Dictionary or JSON Handling ===== #
testDict = {'jsonFloat': 1.05, 'jsonInt': 3, 'jsonString': 'Hello World', 'jsonBool': True}
myCubeNode.addAttr('jsonTest', testDict)  # create a string attr with JSON serialized data
print(myCubeNode.jsonTest['jsonString'])  # >> 'Hello World'

# ===== message attribute handling ===== #
# A message attribute is a dependency node attribute that does not transmit data.
# Message attributes only exist to formally declare relationships between nodes.
# By connecting two nodes via message attributes, a relationship between those nodes is expressed.
cmds.polyCube()
cmds.polyCube()
cmds.polyCube()
cmds.polyCube()

# Create a Non multi-msg attr and wire pCube1 to it
myCubeNode.addAttr('msgSingleTest', value='pCube1', attrType='messageSimple')
print(myCubeNode.msgSingleTest)  # >> ['pCube1']
myCubeNode.msgSingleTest = 'pCube2'
# NOTE pCube1 will be disconnected and the msg will connect to Cube2
print(myCubeNode.msgSingleTest)  # >> ['pCube2']

# TODO 不知道为啥multi-msg在maya中不会被序列化到ui上
# Create a Multi-message attr and wire pCube1 to it, index not Matters
myCubeNode.addAttr('msgMultiTest', value=['pCube2', 'pCube3', 'pCube4'], attrType='message')
print(myCubeNode.msgMultiTest)  # >> ['pCube2','pCube3','pCube4']
myCubeNode.msgMultiTest = 'pCube2'
print(myCubeNode.msgMultiTest)  # >> ['pCube2'] # pCube3 and pCube4 have now been disconnected
myCubeNode.msgMultiTest = ['pCube3', 'pCube4']
print(myCubeNode.msgMultiTest)  # >>['pCube3','pCube4']

# connect 'pCube4' to the node with a attribute name 'myChild'
myCubeNode.connectChild('pCube4', 'myChild')
print(myCubeNode.myChild)

# deleting an attribute from node
delattr(myCubeNode, 'myChild')

'''
Blind Usage for any Maya Node
===============================================================
Lets do the same thing on a standard Maya node without the MetaClass. Here we're
going to simply use the MetaClass wrapping to manage a standard lambert Node.
'''

# translating a cube to (1,3,2) through node
myCubeNode.translate = (1, 3, 2)

mLambert = r9Meta.MetaClass('lambert1')
# mLambert is just a Python MetaNode and doesn't exist as a MayaNode
print(mLambert.diffuse)  # >>0.5
print(mLambert.color)  # >>(0.5, 0.5, 0.5)
mLambert.color = (1, 0.2, 0.2)  # sets the compound float3 attr

mLambert.diffuse = 0.7  # sets the diffuse directly
print(mLambert.diffuse)  # >>0.7

'''
General Methods
===============================================================
Generic call to find all mClass nodes in the scene. This also takes
a type argument so you can return only nodes of a given class type
NOTE: the given class type must exist as a key in the RED9_META_REGISTRY 
'''
mClass = r9Meta.getMetaNodes()
print(mClass)
mClass = r9Meta.getMetaNodes(dataType='mClass',mTypes='MetaRig')
print(mClass)
#Return only MetaRig class objects. If the dataType isn't 'mClass' then we
#return the standard MayaNodes, else we return the mClass initialized to the class object
cmds.select( 'pCube3', add=True )
cmds.select( 'pCube4', add=True )
#Connect the selected Maya Nodes to the mClass node under a Multi-Message attr 'mirrorLeft'
myCubeNode.connectChildren(cmds.ls(sl=True),'mirrorLeft')
print(myCubeNode.mirrorLeft)    #will now return all connected nodes to the message attr

#Connect the selected Maya Node to the mClass node under a NON Multi-Message attr 'simpleChild'
#this is what most of the MRig calls use as a single connection describes a single MayaNode
myCubeNode.connectChild(cmds.ls(sl=True)[0],'simpleChild')
print(myCubeNode.simpleChild)    #will now return all connected nodes to the message attr

# TODO 不知道为什么这里的返回的是空的列表
nodes = r9Meta.getConnectedMetaNodes(cmds.ls(sl=True))
print(nodes)
print(type(cmds.polyCube()))
