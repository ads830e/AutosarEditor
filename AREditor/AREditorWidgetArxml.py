import sys

from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .AREditorWidgetBase import *

from .ARTool import ARTool, ARUtils


class AREditorWidgetArxml(AREditorWidgetBase):
    aRTool = None

    def __init__(self):
        super().__init__()
        self.aRTool = None

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
        for aRXmlFile in self.aRTool.ARXmlFiles:
            ret = ret + self.GenTreeWidgetItemsRecursive(aRXmlFile.Autosar)
        return ret

    def GenTreeWidgetItemsRecursive(self, ARObject) -> list:
        if not ARObject:
            return list()
        if not hasattr(ARObject, 'member_data_items_'):
            return list()
        ret = list()

        ShortName = self.aRTool.GetARObjectShortName(ARObject)
        ShortDefRef = self.aRTool.GetARObjectShortDefRef(ARObject)

        ThisName = None
        if ShortName :
            ThisName = ShortName
        elif ShortDefRef :
            ThisName = ShortDefRef

        member_data_items_ = getattr(ARObject, 'member_data_items_')

        if ThisName :
            thisnode = ArxmlContainerTreeWidgetItem(ARObject, name=ThisName)
            ret.append(thisnode)
            subchildrens = list()

            for key in member_data_items_.keys():
                MemberSpec = member_data_items_[key]

                if MemberSpec.name == 'S':
                    continue
                elif MemberSpec.name == 'T':
                    continue

                attrval = getattr(ARObject, MemberSpec.name)
                if not attrval:
                    continue
                # attrval not None here

                if isinstance(attrval, list):
                    for attrvali in attrval:
                        subchildrens = subchildrens + self.GenTreeWidgetItemsRecursive(attrvali)
                    continue
                else:
                    subchildrens = subchildrens + self.GenTreeWidgetItemsRecursive(attrval)
                pass
            for subchild in subchildrens:
                thisnode.addChild(subchild)
        else:
            for key in member_data_items_.keys():
                MemberSpec = member_data_items_[key]

                if MemberSpec.name == 'S':
                    continue
                elif MemberSpec.name == 'T':
                    continue

                attrval = getattr(ARObject, MemberSpec.name)
                if not attrval:
                    continue
                # attrval not None here

                if isinstance(attrval, list):
                    for attrvali in attrval:
                        ret = ret + self.GenTreeWidgetItemsRecursive(attrvali)
                    continue
                else:
                    ret = ret + self.GenTreeWidgetItemsRecursive(attrval)
                pass
        return ret


class ArxmlContainerTreeWidgetItem(QTreeWidgetItem):
    arobject = None

    def __init__(self, arobject, name=''):
        super().__init__()
        self.setText(0, name)
        self.arobject = arobject
