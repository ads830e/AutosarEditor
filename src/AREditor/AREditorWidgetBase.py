import sys

from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class AREditorWidgetBase(QFrame):
    def __init__(self):
        super().__init__()

        self.qTextEdit_Desc = QTextEdit()
        self.qTextEdit_Desc.setReadOnly(True)

        self.qTextEdit_Msg = QTextEdit()
        self.qTextEdit_Msg.setReadOnly(True)

        self.qTreeWidget_Container = QTreeWidget()
        self.qTreeWidget_Container.setColumnCount(1)
        self.qTreeWidget_Container.setHeaderHidden(True)

        self.qScrollArea_Detail = QScrollArea()

        # self.qScrollArea_Detail.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.qScrollArea_Detail.setWidgetResizable(True)

        __vbox1 = QVBoxLayout()
        __vbox1.addWidget(QLabel('Container'))
        __vbox1.addWidget(self.qTreeWidget_Container)
        __vbox1.setContentsMargins(1, 1, 1, 1)

        __vbox2 = QVBoxLayout()
        __vbox2.addWidget(QLabel('Detail'))
        __vbox2.addWidget(self.qScrollArea_Detail)
        __vbox2.setContentsMargins(1, 1, 1, 1)

        __vbox3 = QVBoxLayout()
        __vbox3.setContentsMargins(1, 1, 1, 1)
        __vbox3.addWidget(QLabel('Description'))
        __vbox3.addWidget(self.qTextEdit_Desc)

        __vbox4 = QVBoxLayout()
        __vbox4.setContentsMargins(1, 1, 1, 1)
        __vbox4.addWidget(QLabel('Message'))
        __vbox4.addWidget(self.qTextEdit_Msg)

        __qFrame1 = QFrame()
        __qFrame1.setFrameShape(QFrame.StyledPanel)
        __qFrame2 = QFrame()
        __qFrame2.setFrameShape(QFrame.StyledPanel)
        __qFrame3 = QFrame()
        __qFrame3.setFrameShape(QFrame.StyledPanel)
        __qFrame4 = QFrame()
        __qFrame4.setFrameShape(QFrame.StyledPanel)

        __qFrame1.setLayout(__vbox1)
        __qFrame2.setLayout(__vbox2)
        __qFrame3.setLayout(__vbox3)
        __qFrame4.setLayout(__vbox4)

        __qFrame1.setMinimumSize(50, 50)
        __qFrame2.setMinimumSize(50, 50)
        __qFrame3.setMinimumSize(50, 50)
        __qFrame4.setMinimumSize(50, 50)

        self.__splitterh1 = QSplitter(Qt.Horizontal)
        self.__splitterh2 = QSplitter(Qt.Horizontal)

        self.__splitterh1.splitterMoved.connect(self.__moveSplitter)
        self.__splitterh2.splitterMoved.connect(self.__moveSplitter)

        self.__splitterh1.addWidget(__qFrame1)
        self.__splitterh1.addWidget(__qFrame2)

        self.__splitterh1.setStretchFactor(0, 10)
        self.__splitterh1.setStretchFactor(1, 30)

        self.__splitterh2.addWidget(__qFrame3)
        self.__splitterh2.addWidget(__qFrame4)

        self.__splitterh2.setStretchFactor(0, 10)
        self.__splitterh2.setStretchFactor(1, 30)

        __splitterv1 = QSplitter(Qt.Vertical)
        __splitterv1.addWidget(self.__splitterh1)
        __splitterv1.addWidget(self.__splitterh2)

        __splitterv1.setStretchFactor(0, 20)
        __splitterv1.setStretchFactor(1, 10)

        __splitterv1.setContentsMargins(1, 1, 1, 1)

        # __splitterv1.setObjectName("splitterv1");
        # __splitterv1.setStyleSheet("QSplitter#splitterv1{ background:white;}");

        __mainlayout = QVBoxLayout()
        __mainlayout.setContentsMargins(0, 10, 0, 0)

        __mainlayout.addWidget(__splitterv1)

        self.setLayout(__mainlayout)

        self.ClearDesc()
        self.ClearMsg()
        self.ClearContainer()
        self.ClearDetail()

        self.__splitterh2.setSizes([200, 600])
        self.__splitterh1.setSizes([200, 600])

    def __moveSplitter(self, pos, index):
        splt = self.__splitterh1 if self.sender() == self.__splitterh2 else self.__splitterh2
        splt.blockSignals(True)
        splt.moveSplitter(pos, index)
        splt.blockSignals(False)

    '''
    def __UpdateTreeView_Test(self):
        qWidget_Detail = QWidget()
        vLayout = QVBoxLayout()
        vLayout.setAlignment(Qt.AlignTop)
        vLayout.setContentsMargins(2,2,2,2);
        vLayout.addLayout(AREditorDetailItemQHBoxLayout(AREditorDetailItemType.STRING,"ShortNameAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB",labelminwidth=250))
        vLayout.addLayout(AREditorDetailItemQHBoxLayout(AREditorDetailItemType.REFERENCE,"IsUsed",labelminwidth=250))
        vLayout.addLayout(AREditorDetailItemQHBoxLayout(AREditorDetailItemType.NUMBER,"IsUsed",labelminwidth=250))
        vLayout.addLayout(AREditorDetailItemQHBoxLayout(AREditorDetailItemType.ENUM,"IsUsed",labelminwidth=250))
        vLayout.addLayout(AREditorDetailItemQHBoxLayout(AREditorDetailItemType.BOOL,"IsUsed",labelminwidth=250))
        qWidget_Detail.setLayout(vLayout)
        self.qScrollArea_Detail.setWidget(qWidget_Detail)
    '''

    def ClearDetail(self):
        __vLayout_Detail_Empty = QVBoxLayout()
        __vLayout_Detail_Empty.setContentsMargins(0, 0, 0, 0)
        __qWidget_Detail_Empty = QWidget()
        __qWidget_Detail_Empty.setLayout(__vLayout_Detail_Empty)
        self.qScrollArea_Detail.setWidget(__qWidget_Detail_Empty)

    def ClearDesc(self):
        self.qTextEdit_Desc.setText('')

    def ClearMsg(self):
        self.qTextEdit_Msg.setText('')

    def ClearContainer(self):
        self.qTreeWidget_Container.clear()

    def Clear(self):
        self.ClearDetail()
        self.ClearDesc()
        self.ClearMsg()
        self.ClearContainer()

'''
class AREditorDetailItemType(Enum):
    STRING = 1
    NUMBER = 2
    ENUM = 5
    REFERENCE = 6
    BOOL = 7


class AREditorDetailItemBoxLayout(QVBoxLayout):
    def __init__(self, itemtype: AREditorDetailItemType, name='', value='', labelminwidth=200):
        super().__init__()
        self.__itemtype = itemtype

        self.HBoxLayout = QHBoxLayout()
        self.addLayout(self.HBoxLayout)

        space0 = QWidget()
        space0.setFixedHeight(1)
        self.addWidget(space0)

        self.__Lable = QLabel(name)
        if labelminwidth < 200:
            labelminwidth = 200
        self.__Lable.setFixedWidth(labelminwidth)
        self.HBoxLayout.addWidget(self.__Lable)
        self.HBoxLayout.setStretch(0, 0)
        if itemtype == AREditorDetailItemType.STRING:
            self.__TextEditor = QLineEdit()
            self.HBoxLayout.addWidget(self.__TextEditor)
            self.HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            self.HBoxLayout.addWidget(space)
            self.HBoxLayout.setStretch(2, 0)
        elif itemtype == AREditorDetailItemType.NUMBER:
            self.__TextEditor = QLineEdit()
            self.HBoxLayout.addWidget(self.__TextEditor)
            self.HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            self.HBoxLayout.addWidget(space)
            self.HBoxLayout.setStretch(2, 0)
        elif itemtype == AREditorDetailItemType.ENUM:
            self.__EnumComboBox = QComboBox()
            self.__EnumComboBox.setEditable(True)
            self.HBoxLayout.addWidget(self.__EnumComboBox)
            self.HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            self.HBoxLayout.addWidget(space)
            self.HBoxLayout.setStretch(2, 0)
        elif itemtype == AREditorDetailItemType.BOOL:
            self.__BoolCheckBox = QCheckBox()
            self.HBoxLayout.addWidget(self.__BoolCheckBox)
            self.HBoxLayout.setStretch(1, 0)
            self.HBoxLayout.addStretch(1)
        elif itemtype == AREditorDetailItemType.REFERENCE:
            self.__TextEditor = QLineEdit()
            self.HBoxLayout.addWidget(self.__TextEditor)
            self.HBoxLayout.setStretch(1, 1)
            self.__BtnRef = QPushButton('.')
            self.__BtnRef.setFixedWidth(20)
            self.HBoxLayout.addWidget(self.__BtnRef)
            self.HBoxLayout.setStretch(2, 0)
        # self.setValue(value)

    def setValue(self, value):
        self.__TextEditor.setText(value)

    def getValue(self):
        return self.__TextEditor.getText()
'''

