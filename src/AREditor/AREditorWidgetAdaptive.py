import sys

from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .AREditorWidgetBase import *

from .ARTool import ARTool, ARUtils
from Autosar_xsd import AUTOSAR_00049_STRICT_COMPACT


class AREditorWidgetAdaptive(AREditorWidgetBase):
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

        ApplicationTreeWidgetItem=ArxmlContainerTreeWidgetItem(None, 'Application')
        LibraryTreeWidgetItem=ArxmlContainerTreeWidgetItem(None, 'Library')
        MachineTreeWidgetItem=ArxmlContainerTreeWidgetItem(None, 'Machine')

        ret.append(ApplicationTreeWidgetItem)
        ret.append(LibraryTreeWidgetItem)
        ret.append(MachineTreeWidgetItem)

        ApplicationTreeWidgetItem.addChild(ArxmlContainerTreeWidgetItem(None, 'DataTypes'))

        'Std Cpp Implementation Data Type'
        

        ApplicationTreeWidgetItem.addChild(ArxmlContainerTreeWidgetItem(None, 'CompuMethods'))
        ApplicationTreeWidgetItem.addChild(ArxmlContainerTreeWidgetItem(None, 'ModeDeclarationGroups'))
        ApplicationTreeWidgetItem.addChild(ArxmlContainerTreeWidgetItem(None, 'PortInterfaces'))
        ApplicationTreeWidgetItem.addChild(ArxmlContainerTreeWidgetItem(None, 'SWComponents'))
        ApplicationTreeWidgetItem.addChild(ArxmlContainerTreeWidgetItem(None, 'Executables'))

        MachineTreeWidgetItem.addChild(ArxmlContainerTreeWidgetItem(None, 'Processes'))
        MachineTreeWidgetItem.addChild(ArxmlContainerTreeWidgetItem(None, 'Process Designs'))

        return ret



class ArxmlContainerTreeWidgetItem(QTreeWidgetItem):
    arobject = None

    def __init__(self, arobject, name=''):
        super().__init__()
        self.setText(0, name)
        self.arobject = arobject