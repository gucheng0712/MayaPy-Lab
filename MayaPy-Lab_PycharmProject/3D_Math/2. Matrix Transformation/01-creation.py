# https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__py_ref_class_open_maya_1_1_m_matrix_html

import maya.api.OpenMaya as om

mat1 = om.MMatrix(((1,0,0,0),
                   (0,1,0,0),
                   (0,0,1,0),
                   (2,4,2,1)))
print(mat1)