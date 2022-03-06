import sys
from ctypes.wintypes import BOOLEAN

from enum import Enum, EnumMeta

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import re

from .AREditorWidgetBase import *

from .ARTool import ARTool, ARUtils
from Autosar_xsd import AUTOSAR_00049_STRICT_COMPACT


class AREditorWidgetArxml(AREditorWidgetBase):
    aRTool = None

    def __init__(self):
        super().__init__()
        self.qTreeWidget_Container.itemClicked.connect(self.__qTreeWidget_Container_itemClicked)

        self.qTreeWidget_Container.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略
        self.qTreeWidget_Container.customContextMenuRequested.connect(self.qTreeWidget_ContainerCustomContextMenuRequested)  # 绑定事件


    def qTreeWidget_ContainerCustomContextMenuRequested(self, pos):
        item = self.qTreeWidget_Container.currentItem()
        item1 = self.qTreeWidget_Container.itemAt(pos)
        if item != None and item1 != None:
            popMenu = QMenu()
            popMenu.addAction(QAction(u'aaa', self))
            popMenu.addAction(QAction(u'bbb', self))
            popMenu.triggered[QAction].connect(self.processtrigger)
            popMenu.exec_(QCursor.pos())
        return

    def processtrigger(self, q):
        QMessageBox.information(None, "DDDD ", "CCCCC", QMessageBox.Yes)
        return

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

        if not hasattr(arobject, 'member_data_items_'):
            return
        member_data_items_ = getattr(arobject, 'member_data_items_')

        for key in member_data_items_.keys():
            MemberSpec: AUTOSAR_00049_STRICT_COMPACT.MemberSpec_ = member_data_items_[key]

            # if MemberSpec.container > 0:
            #    continue

            try:
                if MemberSpec.name == 'S':
                    continue
                elif MemberSpec.name == 'T':
                    continue

                attrname = MemberSpec.child_attrs['name']

                attrtypename0 = re.sub('^AR:', '', MemberSpec.data_type)
                attrtypename1 = re.sub('[\\W]', '_', attrtypename0)

                if hasattr(AUTOSAR_00049_STRICT_COMPACT, attrtypename1):
                    attrtype = getattr(AUTOSAR_00049_STRICT_COMPACT, attrtypename1)

                    attrtypemember_data_items_ = []
                    try:
                        attrtypemember_data_items_ = getattr(attrtype, "member_data_items_")
                    except BaseException:
                        attrtypemember_data_items_ = []
                    finally:
                        pass

                    if attrtypemember_data_items_:
                        if attrtype.member_data_items_.__contains__('valueOf_'):
                            strval = ''
                            try:
                                attrval = getattr(arobject, MemberSpec.name)
                                strval = attrval.valueOf_
                            except BaseException:
                                pass

                            if (attrtypename1 == 'BOOLEAN'):
                                detailitem = ArxmlDetailItem(arobject=arobject,
                                                             itemtype=ArxmlDetailItemType.BOOL,
                                                             name=attrname,
                                                             value=strval,
                                                             labelminwidth=250)
                                vLayout.addLayout(detailitem)
                                detailitem.afterEditedSignal.connect(self.ArxmlDetailItemAfterEdited)
                                pass
                            else:
                                detailitem = ArxmlDetailItem(arobject=arobject,
                                                             itemtype=ArxmlDetailItemType.STRING,
                                                             name=attrname,
                                                             value=strval,
                                                             labelminwidth=250)
                                vLayout.addLayout(detailitem)
                                detailitem.afterEditedSignal.connect(self.ArxmlDetailItemAfterEdited)
                                pass

                        else:
                            pass

                    elif issubclass(attrtype, Enum):
                        strval = ''
                        try:
                            attrval = getattr(arobject, MemberSpec.name)
                            strval = attrval
                        except BaseException:
                            pass
                        attrenums = []
                        for attrenumi in attrtype:
                            attrenums.append(attrenumi.value)
                            pass
                        detailitem = ArxmlDetailItem(arobject=arobject,
                                                     itemtype=ArxmlDetailItemType.ENUM,
                                                     name=attrname,
                                                     value=strval,
                                                     labelminwidth=250,
                                                     enums=attrenums)
                        vLayout.addLayout(detailitem)
                        detailitem.afterEditedSignal.connect(self.ArxmlDetailItemAfterEdited)
                        pass
                elif (attrtypename1 == 'STRING__SIMPLE'):
                    strval = ''
                    try:
                        attrval = getattr(arobject, MemberSpec.name)
                        if attrval:
                            strval = str(attrval)
                    except BaseException:
                        pass
                    detailitem = ArxmlDetailItem(arobject=arobject,
                                                 itemtype=ArxmlDetailItemType.STRING,
                                                 name=attrname,
                                                 value=strval,
                                                 labelminwidth=250)
                    vLayout.addLayout(detailitem)
                    detailitem.afterEditedSignal.connect(self.ArxmlDetailItemAfterEdited)
                    pass


            except BaseException:
                pass
            finally:
                pass

        pass

        descstr: str = ''

        try:
            typestr = type(arobject).__name__
            try:
                typestr = re.search(r'([\w]+)Type\d*\s*$', typestr, re.M).group(1)
            except BaseException:
                pass
            descstr += 'Type: ' + typestr + "\n"
        except BaseException:
            pass

        try:
            descstr += 'Path: ' + self.aRTool.GetPath(arobject) + "\n"
        except BaseException:
            pass

        self.qTextEdit_Desc.setText(descstr)

    def ArxmlDetailItemAfterEdited(self, object, name, value):
        #QMessageBox.information(None, "CCCC ", "CCCCC", QMessageBox.Yes)
        self.IndicateUnSaved()
        return

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
            # ret = ret + self.GenTreeWidgetItemsRecursive(aRXmlFile.Autosar, None)
            filenamei = str(aRXmlFile.FileName)

            filenamei1 = re.search(r'[^\\/]+\.(ar)?xml', filenamei, re.M | re.I).group()

            thisnode = ArxmlContainerTreeWidgetItem(aRXmlFile, name=filenamei1)
            ret.append(thisnode)
            subchildren = self.GenTreeWidgetItemsRecursive(aRXmlFile.Autosar, None)
            for subchild in subchildren:
                thisnode.addChild(subchild)
        return ret

    def GenTreeWidgetItemsRecursive(self, ARObject, name) -> list:
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
        elif name:
            ThisName = name
        else:
            ThisName = type(ARObject).__name__

        member_data_items_ = getattr(ARObject, 'member_data_items_')

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

            attrname = MemberSpec.name
            if MemberSpec.child_attrs:
                if MemberSpec.child_attrs.__contains__('name'):
                    attrname = MemberSpec.child_attrs['name']

            if isinstance(attrval, list):
                for attrvali in attrval:
                    subchildrens = subchildrens + self.GenTreeWidgetItemsRecursive(attrvali, attrname)
                continue
            else:
                subchildrens = subchildrens + self.GenTreeWidgetItemsRecursive(attrval, attrname)
            pass
        for subchild in subchildrens:
            thisnode.addChild(subchild)
        '''
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
        '''
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
    value: str = None
    name: str = None
    afterEditedSignal: pyqtSignal = pyqtSignal(object, str, str)
    arobject = None

    def __init__(self,
                 arobject=None,
                 itemtype: ArxmlDetailItemType = ArxmlDetailItemType.STRING,
                 name: str = '',
                 value: str = '',
                 labelminwidth=200,
                 enums: list = list()):
        super().__init__()

        if not value:
            value = ''

        self.value = value
        self.arobject = arobject
        self.isvaluesetting = False

        self.itemtype = itemtype
        self.name = name

        HBoxLayout = QHBoxLayout()
        self.addLayout(HBoxLayout)

        space0 = QWidget()
        space0.setFixedHeight(1)
        self.addWidget(space0)

        space1 = QWidget()
        space1.setFixedWidth(2)

        HBoxLayout.addWidget(space1)
        HBoxLayout.setStretch(0, 0)

        Lable = QLabel(name)
        if labelminwidth < 200:
            labelminwidth = 200
        Lable.setFixedWidth(labelminwidth)
        HBoxLayout.addWidget(Lable)
        HBoxLayout.setStretch(1, 0)
        if itemtype == ArxmlDetailItemType.STRING:
            self.__TextEditor = QLineEdit()
            self.__TextEditor.editingFinished.connect(self.TextEditorEditingFinished)

            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(2, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(3, 0)
        elif itemtype == ArxmlDetailItemType.FLOAT:
            self.__TextEditor = QLineEdit()
            self.__TextEditor.editingFinished.connect(self.TextEditorEditingFinished)

            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(2, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(3, 0)
        elif itemtype == ArxmlDetailItemType.INTEGER:
            self.__TextEditor = QLineEdit()
            self.__TextEditor.editingFinished.connect(self.TextEditorEditingFinished)

            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(2, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(3, 0)
        elif itemtype == ArxmlDetailItemType.ENUM:
            self.__EnumComboBox = QComboBox()
            self.__EnumComboBox.setEditable(False)
            if enums:
                self.__EnumComboBox.addItems(enums)

            self.__EnumComboBox.currentTextChanged.connect(self.EnumComboBoxCurrentTextChanged)

            HBoxLayout.addWidget(self.__EnumComboBox)
            HBoxLayout.setStretch(2, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(3, 0)
        elif itemtype == ArxmlDetailItemType.BOOL:
            self.__BoolCheckBox = QCheckBox()
            self.__BoolCheckBox.stateChanged.connect(self.BoolCheckBoxStateChanged)

            HBoxLayout.addWidget(self.__BoolCheckBox)
            HBoxLayout.setStretch(2, 0)
            HBoxLayout.addStretch(1)
        elif itemtype == ArxmlDetailItemType.REFERENCE:
            self.__TextEditor = QLineEdit()
            self.__TextEditor.editingFinished.connect(self.TextEditorEditingFinished)

            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(2, 1)
            self.__BtnRef = QPushButton('.')
            self.__BtnRef.setFixedWidth(20)
            HBoxLayout.addWidget(self.__BtnRef)
            HBoxLayout.setStretch(3, 0)
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
            elif value.upper() == 'YES':
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
            return self.__TextEditor.text()
        elif self.itemtype == ArxmlDetailItemType.FLOAT:
            return self.__TextEditor.text()
        elif self.itemtype == ArxmlDetailItemType.INTEGER:
            return self.__TextEditor.text()
        elif self.itemtype == ArxmlDetailItemType.ENUM:
            return self.__EnumComboBox.currentText()
        elif self.itemtype == ArxmlDetailItemType.BOOL:
            if self.__BoolCheckBox.isChecked():
                return "true"
            else:
                return "false"
        elif self.itemtype == ArxmlDetailItemType.REFERENCE:
            return self.__TextEditor.text()
        return ''

    def TextEditorEditingFinished(self):
        if self.isvaluesetting:
            return
        self.AfterEdited()
        return

    def BoolCheckBoxStateChanged(self, status):
        if self.isvaluesetting:
            return
        self.AfterEdited()
        return

    def EnumComboBoxCurrentTextChanged(self, newtext):
        if self.isvaluesetting:
            return
        self.AfterEdited()
        return

    def AfterEdited(self):
        if self.value == self.getValue():
            return
        self.value = self.getValue()
        if self.afterEditedSignal:
            self.afterEditedSignal.emit(self.arobject, self.name, self.value)
        return
