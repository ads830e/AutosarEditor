import sys

from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .AREditorWidgetBase import *

from .ARTool import ARTool, ARUtils
from Autosar_xsd import AUTOSAR_00049_STRICT_COMPACT


class AREditorWidgetClassic(AREditorWidgetBase):
    def __init__(self):
        super().__init__()

    def UpdateTreeView(self):

        self.qTextEdit_Desc.setText('fsf')
        self.qTextEdit_Msg.setText('fsf')

    def SetARTool(self, aRTool: ARTool):
        self.aRTool = aRTool

    def ReloadUI(self):
        super().Clear()
        treeWidgetItems = self.GenTreeWidgetItems()
        for treeWidgetItem in treeWidgetItems:
            self.qTreeWidget_Container.addTopLevelItem(treeWidgetItem)
        pass

    def GenTreeWidgetItems(self) -> list:
        if not self.aRTool:
            return list()
        ret = list()

        moddefs = list()
        if self.aRTool.TypeToObjectsDict.__contains__(AUTOSAR_00049_STRICT_COMPACT.ECUC_MODULE_DEF):
            moddefs = self.aRTool.TypeToObjectsDict[AUTOSAR_00049_STRICT_COMPACT.ECUC_MODULE_DEF]

        for moddef in moddefs:
            ret = ret + self.GenTreeWidgetItemsRecursive(moddef)
        return ret

    def GenTreeWidgetItemsRecursive(self, ARObject) -> list:
        return list()
