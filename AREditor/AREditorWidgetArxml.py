import sys

from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .AREditorWidgetBase import *

from .ARTool import ARTool, ARUtils
from Autosar_xsd import AUTOSAR_00049_STRICT_COMPACT


class AREditorWidgetArxml(AREditorWidgetBase):
    aRTool = None

    def __init__(self):
        super().__init__()
        self.qTreeWidget_Container.itemClicked.connect(self.__qTreeWidget_Container_itemClicked)

    def __qTreeWidget_Container_itemClicked(self, item, column):
        selecteditems = self.qTreeWidget_Container.selectedItems()
        if not selecteditems:
            self.ClearDesc()
            self.ClearDetail()
            return
        if len(selecteditems) > 1:
            self.ClearDesc()
            self.ClearDetail()
            return
        selecteditem = selecteditems[0]
        if not selecteditem:
            self.ClearDesc()
            self.ClearDetail()
            return
        if not isinstance(selecteditem, ArxmlContainerTreeWidgetItem):
            self.ClearDesc()
            self.ClearDetail()
            return

        self.UpdateDetailWidget(selecteditem.arobject)

    def UpdateDetailWidget(self, arobject):
        qWidget_Detail = QWidget()
        vLayout = QVBoxLayout()
        vLayout.setAlignment(Qt.AlignTop)
        vLayout.setContentsMargins(2, 2, 2, 2)
        qWidget_Detail.setLayout(vLayout)
        self.qScrollArea_Detail.setWidget(qWidget_Detail)

        shortname = self.aRTool.GetARObjectShortName(arobject)
        vLayout.addLayout(ArxmlDetailItem(ArxmlDetailItemType.STRING,
                                          name='SHORT-NAME',
                                          value=shortname,
                                          labelminwidth=250))

        if not hasattr(arobject, 'member_data_items_'):
            return
        member_data_items_ = getattr(arobject, 'member_data_items_')

        for key in member_data_items_.keys():
            MemberSpec: AUTOSAR_00049_STRICT_COMPACT.MemberSpec_ = member_data_items_[key]

            if MemberSpec.name == 'S':
                continue
            elif MemberSpec.name == 'T':
                continue
            '''
            elif MemberSpec.name == 'UUID':
                continue
            elif MemberSpec.name == 'ADMIN_DATA':
                continue
            elif MemberSpec.name == 'SHORT_NAME_FRAGMENTS':
                continue
            elif MemberSpec.name == 'SHORT_NAME_PATTERN':
                continue
            elif MemberSpec.name == 'ANNOTATIONS':
                continue
            elif MemberSpec.name == 'VARIATION_POINT':
                continue
            elif MemberSpec.name == 'BLUEPRINT_POLICYS':
                continue
            '''


            try:
                attrval = getattr(arobject, MemberSpec.name)
                attrname = MemberSpec.child_attrs['name']
                vLayout.addLayout(ArxmlDetailItem(ArxmlDetailItemType.STRING,
                                                  name=attrname,
                                                  labelminwidth=250))
            finally:
                pass

        pass
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
        if ShortName:
            ThisName = ShortName
        elif ShortDefRef:
            ThisName = ShortDefRef

        member_data_items_ = getattr(ARObject, 'member_data_items_')

        if ThisName:
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


class ArxmlDetailItemType(Enum):
    STRING = 1
    FLOAT = 2
    INTEGER = 3
    ENUM = 4
    REFERENCE = 5
    BOOL = 6


class ArxmlDetailItem(QVBoxLayout):
    def __init__(self,
                 itemtype: ArxmlDetailItemType,
                 name: str = '',
                 value: str = '',
                 labelminwidth=200,
                 enums: list = list()):
        super().__init__()

        self.isvaluesetting = False

        self.itemtype = itemtype

        HBoxLayout = QHBoxLayout()
        self.addLayout(HBoxLayout)

        space0 = QWidget()
        space0.setFixedHeight(1)
        self.addWidget(space0)

        Lable = QLabel(name)
        if labelminwidth < 200:
            labelminwidth = 200
        Lable.setFixedWidth(labelminwidth)
        HBoxLayout.addWidget(Lable)
        HBoxLayout.setStretch(0, 0)
        if itemtype == ArxmlDetailItemType.STRING:
            self.__TextEditor = QLineEdit()
            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(2, 0)
        elif itemtype == ArxmlDetailItemType.FLOAT:
            self.__TextEditor = QLineEdit()
            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(2, 0)
        elif itemtype == ArxmlDetailItemType.INTEGER:
            self.__TextEditor = QLineEdit()
            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(2, 0)
        elif itemtype == ArxmlDetailItemType.ENUM:
            self.__EnumComboBox = QComboBox()
            self.__EnumComboBox.setEditable(True)
            if enums:
                self.__EnumComboBox.addItems(enums)

            HBoxLayout.addWidget(self.__EnumComboBox)
            HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(2, 0)
        elif itemtype == ArxmlDetailItemType.BOOL:
            self.__BoolCheckBox = QCheckBox()
            HBoxLayout.addWidget(self.__BoolCheckBox)
            HBoxLayout.setStretch(1, 0)
            HBoxLayout.addStretch(1)
        elif itemtype == ArxmlDetailItemType.REFERENCE:
            self.__TextEditor = QLineEdit()
            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(1, 1)
            self.__BtnRef = QPushButton('.')
            self.__BtnRef.setFixedWidth(20)
            HBoxLayout.addWidget(self.__BtnRef)
            HBoxLayout.setStretch(2, 0)
        self.setValue(value)

    def setValue(self, value: str):
        self.isvaluesetting = True
        if self.itemtype == ArxmlDetailItemType.STRING:
            self.__TextEditor.setText(value)
        elif self.itemtype == ArxmlDetailItemType.FLOAT:
            self.__TextEditor.setText(value)
        elif self.itemtype == ArxmlDetailItemType.INTEGER:
            self.__TextEditor.setText(value)
        elif self.itemtype == ArxmlDetailItemType.ENUM:
            self.__EnumComboBox.setCurrentText(value)
        elif self.itemtype == ArxmlDetailItemType.BOOL:
            if value is None:
                self.__BoolCheckBox.setChecked(False)
            elif value.upper() == 'TRUE':
                self.__BoolCheckBox.setChecked(True)
            elif value.upper() == '1':
                self.__BoolCheckBox.setChecked(True)
            else:
                self.__BoolCheckBox.setChecked(False)
        elif self.itemtype == ArxmlDetailItemType.REFERENCE:
            self.__TextEditor.setText(value)
        self.isvaluesetting = False

    def getValue(self) -> str:
        if self.itemtype == ArxmlDetailItemType.STRING:
            return self.__TextEditor.getText()
        elif self.itemtype == ArxmlDetailItemType.FLOAT:
            return self.__TextEditor.getText()
        elif self.itemtype == ArxmlDetailItemType.INTEGER:
            return self.__TextEditor.getText()
        elif self.itemtype == ArxmlDetailItemType.ENUM:
            return self.__EnumComboBox.currentText()
        elif self.itemtype == ArxmlDetailItemType.BOOL:
            if self.__BoolCheckBox.isChecked():
                return "true"
            else:
                return "false"
        elif self.itemtype == ArxmlDetailItemType.REFERENCE:
            return self.__TextEditor.getText()
        return ''
