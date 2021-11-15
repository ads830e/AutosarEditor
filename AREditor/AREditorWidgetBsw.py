import sys

from enum import Enum

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .AREditorWidgetBase import *

from .ARTool import ARTool, ARUtils
from Autosar_xsd import AUTOSAR_00049_STRICT_COMPACT


class AREditorWidgetBsw(AREditorWidgetBase):
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
        if not isinstance(selecteditem, BswContainerTreeWidgetItem):
            self.ClearDesc()
            self.ClearDetail()
            return

        if isinstance(selecteditem.moddef, AUTOSAR_00049_STRICT_COMPACT.ECUC_MODULE_DEF):
            self.ClearDesc()
            self.ClearDetail()
            return
        elif isinstance(selecteditem.moddef, AUTOSAR_00049_STRICT_COMPACT.ECUC_PARAM_CONF_CONTAINER_DEF):
            if not selecteditem.modcfgs:
                self.ClearDesc()
                self.ClearDetail()
                return
            '''
            if self.IsModDefMultiplicityInfinite(selecteditem.moddef):
                self.ClearDesc()
                self.ClearDetail()
                return
                '''
            self.UpdateDetailWidget(selecteditem.moddef, selecteditem.modcfgs)
            return
        elif isinstance(selecteditem.moddef, AUTOSAR_00049_STRICT_COMPACT.ECUC_CHOICE_CONTAINER_DEF):
            if not selecteditem.modcfgs:
                self.ClearDesc()
                self.ClearDetail()
                return
            self.UpdateDetailWidget(selecteditem.moddef, selecteditem.modcfgs)
            return
        else:
            self.ClearDesc()
            self.ClearDetail()
            return
        pass

    def GetCfgValObj(self, cfgdef, modcfgs):
        if modcfgs:
            if isinstance(modcfgs, list):
                for modcfgi in modcfgs:
                    ret = self.GetCfgValObj(cfgdef, modcfgi)
                    if ret:
                        return ret
                    pass
                return None
            else:
                defrefpath: str = self.aRTool.GetPath(cfgdef)
                modcfg = modcfgs

                if modcfg.PARAMETER_VALUES:
                    if modcfg.PARAMETER_VALUES.ECUC_ADD_INFO_PARAM_VALUE:
                        for cfgval in modcfg.PARAMETER_VALUES.ECUC_ADD_INFO_PARAM_VALUE:
                            if self.aRTool.GetARObjectDefRef(cfgval) == defrefpath:
                                return cfgval
                            pass
                        pass
                    if modcfg.PARAMETER_VALUES.ECUC_NUMERICAL_PARAM_VALUE:
                        for cfgval in modcfg.PARAMETER_VALUES.ECUC_NUMERICAL_PARAM_VALUE:
                            if self.aRTool.GetARObjectDefRef(cfgval) == defrefpath:
                                return cfgval
                            pass
                        pass
                    if modcfg.PARAMETER_VALUES.ECUC_TEXTUAL_PARAM_VALUE:
                        for cfgval in modcfg.PARAMETER_VALUES.ECUC_TEXTUAL_PARAM_VALUE:
                            if self.aRTool.GetARObjectDefRef(cfgval) == defrefpath:
                                return cfgval
                            pass
                        pass
                    pass
                if modcfg.REFERENCE_VALUES:
                    if modcfg.REFERENCE_VALUES.ECUC_INSTANCE_REFERENCE_VALUE:
                        for refval in modcfg.REFERENCE_VALUES.ECUC_INSTANCE_REFERENCE_VALUE:
                            if self.aRTool.GetARObjectDefRef(refval) == defrefpath:
                                return refval
                            pass
                        pass
                    if modcfg.REFERENCE_VALUES.ECUC_REFERENCE_VALUE:
                        for refval in modcfg.REFERENCE_VALUES.ECUC_REFERENCE_VALUE:
                            if self.aRTool.GetARObjectDefRef(refval) == defrefpath:
                                return refval
                            pass
                        pass
                    pass

                '''
                if isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_ADD_INFO_PARAM_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_BOOLEAN_PARAM_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_ENUMERATION_PARAM_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_FLOAT_PARAM_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_FUNCTION_NAME_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_INTEGER_PARAM_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_LINKER_SYMBOL_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_MULTILINE_STRING_PARAM_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_STRING_PARAM_DEF):
                    pass
                ##############################################################
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_CHOICE_REFERENCE_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_FOREIGN_REFERENCE_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_INSTANCE_REFERENCE_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_REFERENCE_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_SYMBOLIC_NAME_REFERENCE_DEF):
                    pass
                elif isinstance(cfgdef, AUTOSAR_00049_STRICT_COMPACT.ECUC_URI_REFERENCE_DEF):
                    pass
                '''
                pass
            pass
        return None

    def GetCfgVal(self, valobj):
        try:
            if isinstance(valobj, AUTOSAR_00049_STRICT_COMPACT.ECUC_ADD_INFO_PARAM_VALUE):
                return valobj.VALUE.valueOf_
            elif isinstance(valobj, AUTOSAR_00049_STRICT_COMPACT.ECUC_NUMERICAL_PARAM_VALUE):
                return valobj.VALUE.valueOf_
            elif isinstance(valobj, AUTOSAR_00049_STRICT_COMPACT.ECUC_TEXTUAL_PARAM_VALUE):
                return valobj.VALUE.valueOf_
            #################################
            elif isinstance(valobj, AUTOSAR_00049_STRICT_COMPACT.ECUC_INSTANCE_REFERENCE_VALUE):
                return valobj.VALUE_IREF.TARGET_REF.valueOf_
            elif isinstance(valobj, AUTOSAR_00049_STRICT_COMPACT.ECUC_REFERENCE_VALUE):
                return valobj.VALUE_REF.valueOf_
            else:
                return None
        except BaseException:
            return None


    def UpdateDetailWidget(self, moddef, modcfgs: list):
        qWidget_Detail = QWidget()
        vLayout = QVBoxLayout()
        vLayout.setAlignment(Qt.AlignTop)
        vLayout.setContentsMargins(2, 2, 2, 2)
        qWidget_Detail.setLayout(vLayout)
        self.qScrollArea_Detail.setWidget(qWidget_Detail)

        shortname = ''
        if modcfgs:
            if isinstance(modcfgs, list):
                shortname = self.aRTool.GetARObjectShortName(modcfgs[0])
                pass
            else:
                shortname = self.aRTool.GetARObjectShortName(modcfgs)
                pass

        vLayout.addLayout(BswDetailItem(BswDetailItemType.STRING,
                                        name='ShortName',
                                        value=shortname,
                                        labelminwidth=250))

        if moddef.PARAMETERS:
            if moddef.PARAMETERS.ECUC_ADD_INFO_PARAM_DEF:
                for parmdef in moddef.PARAMETERS.ECUC_ADD_INFO_PARAM_DEF:
                    valobj = self.GetCfgValObj(parmdef, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.STRING,
                                                    self.aRTool.GetARObjectShortName(parmdef),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            if moddef.PARAMETERS.ECUC_BOOLEAN_PARAM_DEF:
                for parmdef in moddef.PARAMETERS.ECUC_BOOLEAN_PARAM_DEF:
                    valobj = self.GetCfgValObj(parmdef, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.BOOL,
                                                    self.aRTool.GetARObjectShortName(parmdef),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            if moddef.PARAMETERS.ECUC_ENUMERATION_PARAM_DEF:
                for parmdef in moddef.PARAMETERS.ECUC_ENUMERATION_PARAM_DEF:
                    valobj = self.GetCfgValObj(parmdef, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.ENUM,
                                                    self.aRTool.GetARObjectShortName(parmdef),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            if moddef.PARAMETERS.ECUC_FLOAT_PARAM_DEF:
                for parmdef in moddef.PARAMETERS.ECUC_FLOAT_PARAM_DEF:
                    valobj = self.GetCfgValObj(parmdef, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.FLOAT,
                                                    self.aRTool.GetARObjectShortName(parmdef),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            if moddef.PARAMETERS.ECUC_FUNCTION_NAME_DEF:
                for parmdef in moddef.PARAMETERS.ECUC_FUNCTION_NAME_DEF:
                    valobj = self.GetCfgValObj(parmdef, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.STRING,
                                                    self.aRTool.GetARObjectShortName(parmdef),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            if moddef.PARAMETERS.ECUC_INTEGER_PARAM_DEF:
                for parmdef in moddef.PARAMETERS.ECUC_INTEGER_PARAM_DEF:
                    valobj = self.GetCfgValObj(parmdef, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.INTEGER,
                                                    self.aRTool.GetARObjectShortName(parmdef),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            if moddef.PARAMETERS.ECUC_LINKER_SYMBOL_DEF:
                for parmdef in moddef.PARAMETERS.ECUC_LINKER_SYMBOL_DEF:
                    valobj = self.GetCfgValObj(parmdef, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.STRING,
                                                    self.aRTool.GetARObjectShortName(parmdef),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            if moddef.PARAMETERS.ECUC_MULTILINE_STRING_PARAM_DEF:
                for parmdef in moddef.PARAMETERS.ECUC_MULTILINE_STRING_PARAM_DEF:
                    valobj = self.GetCfgValObj(parmdef, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.STRING,
                                                    self.aRTool.GetARObjectShortName(parmdef),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            if moddef.PARAMETERS.ECUC_STRING_PARAM_DEF:
                for parmdef in moddef.PARAMETERS.ECUC_STRING_PARAM_DEF:
                    valobj = self.GetCfgValObj(parmdef, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.STRING,
                                                    self.aRTool.GetARObjectShortName(parmdef),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass

            pass
        #################################################################
        if moddef.REFERENCES:
            if moddef.REFERENCES.ECUC_CHOICE_REFERENCE_DEF:
                for ref in moddef.REFERENCES.ECUC_CHOICE_REFERENCE_DEF:
                    valobj = self.GetCfgValObj(ref, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.REFERENCE,
                                                    self.aRTool.GetARObjectShortName(ref),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            pass
            if moddef.REFERENCES.ECUC_FOREIGN_REFERENCE_DEF:
                for ref in moddef.REFERENCES.ECUC_FOREIGN_REFERENCE_DEF:
                    valobj = self.GetCfgValObj(ref, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.REFERENCE,
                                                    self.aRTool.GetARObjectShortName(ref),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            pass
            if moddef.REFERENCES.ECUC_INSTANCE_REFERENCE_DEF:
                for ref in moddef.REFERENCES.ECUC_INSTANCE_REFERENCE_DEF:
                    valobj = self.GetCfgValObj(ref, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.REFERENCE,
                                                    self.aRTool.GetARObjectShortName(ref),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            pass
            if moddef.REFERENCES.ECUC_REFERENCE_DEF:
                for ref in moddef.REFERENCES.ECUC_REFERENCE_DEF:
                    valobj = self.GetCfgValObj(ref, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.REFERENCE,
                                                    self.aRTool.GetARObjectShortName(ref),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            pass
            if moddef.REFERENCES.ECUC_SYMBOLIC_NAME_REFERENCE_DEF:
                for ref in moddef.REFERENCES.ECUC_SYMBOLIC_NAME_REFERENCE_DEF:
                    valobj = self.GetCfgValObj(ref, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.REFERENCE,
                                                    self.aRTool.GetARObjectShortName(ref),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            pass
            if moddef.REFERENCES.ECUC_URI_REFERENCE_DEF:
                for ref in moddef.REFERENCES.ECUC_URI_REFERENCE_DEF:
                    valobj = self.GetCfgValObj(ref, modcfgs)
                    val = self.GetCfgVal(valobj)
                    vLayout.addLayout(BswDetailItem(BswDetailItemType.REFERENCE,
                                                    self.aRTool.GetARObjectShortName(ref),
                                                    value=val,
                                                    labelminwidth=250))
                    pass
                pass
            pass

        pass

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

        modcfgs = list()
        if self.aRTool.TypeToObjectsDict.__contains__(AUTOSAR_00049_STRICT_COMPACT.ECUC_MODULE_CONFIGURATION_VALUES):
            modcfgs = self.aRTool.TypeToObjectsDict[AUTOSAR_00049_STRICT_COMPACT.ECUC_MODULE_CONFIGURATION_VALUES]

        for moddef in moddefs:
            ret = ret + self.GenBswTreeWidgetItemsRecursive(moddef, modcfgs)
        return ret

    def FilterModCfgsByDefRef(self, modcfgs: list, moddef) -> list:
        if not modcfgs:
            return list()
        ret = list()
        moddefpath = self.aRTool.GetPath(moddef)
        for modcfg in modcfgs:
            if self.aRTool.GetARObjectDefRef(modcfg) == moddefpath:
                ret.append(modcfg)
        return ret

    def GenBswTreeWidgetItemsRecursive(self, ModDef, AllModCfgs: list) -> list:
        ret = list()

        ModCfgs = self.FilterModCfgsByDefRef(AllModCfgs, ModDef)

        if isinstance(ModDef, AUTOSAR_00049_STRICT_COMPACT.ECUC_MODULE_DEF):
            EcuCModDef = ModDef

            thisnode = BswContainerTreeWidgetItem(EcuCModDef, ModCfgs,
                                                  name=self.aRTool.GetARObjectShortName(EcuCModDef))
            ret.append(thisnode)

            children = list()

            cfgchildren = list()
            for ModCfg in ModCfgs:
                cfgchildren = cfgchildren + self.GetBswCfgSubContainers(ModCfg)
                pass

            for container in EcuCModDef.get_CONTAINERS().ECUC_CHOICE_CONTAINER_DEF:
                children = children + self.GenBswTreeWidgetItemsRecursive(container, cfgchildren)
                pass
            for container in EcuCModDef.get_CONTAINERS().ECUC_PARAM_CONF_CONTAINER_DEF:
                children = children + self.GenBswTreeWidgetItemsRecursive(container, cfgchildren)
                pass

            for child in children:
                thisnode.addChild(child)
            pass
        elif isinstance(ModDef, AUTOSAR_00049_STRICT_COMPACT.ECUC_PARAM_CONF_CONTAINER_DEF):
            EcuCParmContainerDef = ModDef

            UPPER_MULTIPLICITY_INFINITE = self.IsModDefMultiplicityInfinite(EcuCParmContainerDef)

            if not UPPER_MULTIPLICITY_INFINITE:
                thisnode = BswContainerTreeWidgetItem(EcuCParmContainerDef, ModCfgs,
                                                      name=self.aRTool.GetARObjectShortName(EcuCParmContainerDef))
                ret.append(thisnode)
                children = list()

                cfgchildren = list()
                for ModCfg in ModCfgs:
                    cfgchildren = cfgchildren + self.GetBswCfgSubContainers(ModCfg)
                    pass
                if EcuCParmContainerDef.get_SUB_CONTAINERS():
                    if EcuCParmContainerDef.get_SUB_CONTAINERS().ECUC_CHOICE_CONTAINER_DEF:
                        for container in EcuCParmContainerDef.get_SUB_CONTAINERS().ECUC_CHOICE_CONTAINER_DEF:
                            children = children + self.GenBswTreeWidgetItemsRecursive(container, cfgchildren)
                            pass

                if EcuCParmContainerDef.get_SUB_CONTAINERS():
                    if EcuCParmContainerDef.get_SUB_CONTAINERS().ECUC_PARAM_CONF_CONTAINER_DEF:
                        for container in EcuCParmContainerDef.get_SUB_CONTAINERS().ECUC_PARAM_CONF_CONTAINER_DEF:
                            children = children + self.GenBswTreeWidgetItemsRecursive(container, cfgchildren)
                            pass

                for child in children:
                    thisnode.addChild(child)
                pass
            else:
                thisnode = QTreeWidgetItem()
                thisnode.setText(0, self.aRTool.GetARObjectShortName(EcuCParmContainerDef))

                ret.append(thisnode)

                for ModCfg in ModCfgs:
                    subnode = BswContainerTreeWidgetItem(EcuCParmContainerDef, [ModCfg],
                                                         name=self.aRTool.GetARObjectShortName(ModCfg))
                    thisnode.addChild(subnode)

                    children = list()
                    cfgchildren = self.GetBswCfgSubContainers(ModCfg)

                    if EcuCParmContainerDef.get_SUB_CONTAINERS():
                        if EcuCParmContainerDef.get_SUB_CONTAINERS().ECUC_CHOICE_CONTAINER_DEF:
                            for container in EcuCParmContainerDef.get_SUB_CONTAINERS().ECUC_CHOICE_CONTAINER_DEF:
                                children = children + self.GenBswTreeWidgetItemsRecursive(container, cfgchildren)
                                pass

                    if EcuCParmContainerDef.get_SUB_CONTAINERS():
                        if EcuCParmContainerDef.get_SUB_CONTAINERS().ECUC_PARAM_CONF_CONTAINER_DEF:
                            for container in EcuCParmContainerDef.get_SUB_CONTAINERS().ECUC_PARAM_CONF_CONTAINER_DEF:
                                children = children + self.GenBswTreeWidgetItemsRecursive(container, cfgchildren)
                                pass

                    for child in children:
                        subnode.addChild(child)
                    pass

                pass

            pass
        elif isinstance(ModDef, AUTOSAR_00049_STRICT_COMPACT.ECUC_CHOICE_CONTAINER_DEF):
            pass
        else:
            pass

        return ret

    def IsModDefMultiplicityInfinite(self, moddef) -> bool:
        UPPER_MULTIPLICITY_INFINITE = False
        if moddef.UPPER_MULTIPLICITY_INFINITE:
            if moddef.UPPER_MULTIPLICITY_INFINITE.valueOf_:
                valstr = moddef.UPPER_MULTIPLICITY_INFINITE.valueOf_
                if valstr == 'True':
                    UPPER_MULTIPLICITY_INFINITE = True
                elif valstr == 'TRUE':
                    UPPER_MULTIPLICITY_INFINITE = True
                elif valstr == 'true':
                    UPPER_MULTIPLICITY_INFINITE = True
        return UPPER_MULTIPLICITY_INFINITE

    def GetBswCfgSubContainers(self, ARObject):
        if isinstance(ARObject, AUTOSAR_00049_STRICT_COMPACT.ECUC_MODULE_CONFIGURATION_VALUES):
            ModCfg = ARObject
            if not ModCfg.CONTAINERS:
                return list()
            elif not ModCfg.CONTAINERS.ECUC_CONTAINER_VALUE:
                return list()
            else:
                return ModCfg.CONTAINERS.ECUC_CONTAINER_VALUE
            pass
        elif isinstance(ARObject, AUTOSAR_00049_STRICT_COMPACT.ECUC_CONTAINER_VALUE):
            Container = ARObject
            if not Container.SUB_CONTAINERS:
                return list()
            elif not Container.SUB_CONTAINERS.ECUC_CONTAINER_VALUE:
                return list()
            else:
                return Container.SUB_CONTAINERS.ECUC_CONTAINER_VALUE
            pass
        else:
            pass
        return list()


class BswContainerTreeWidgetItem(QTreeWidgetItem):
    moddef = None
    modcfgs = list()

    def __init__(self, moddef=None, modcfgs: list = list(), name: str = ''):
        super().__init__()
        self.setText(0, name)
        self.moddef = moddef
        self.modcfgs = modcfgs


class BswDetailItemType(Enum):
    STRING = 1
    FLOAT = 2
    INTEGER = 3
    ENUM = 4
    REFERENCE = 5
    BOOL = 6


class BswDetailItem(QVBoxLayout):
    def __init__(self,
                 itemtype: BswDetailItemType,
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
        if itemtype == BswDetailItemType.STRING:
            self.__TextEditor = QLineEdit()
            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(2, 0)
        elif itemtype == BswDetailItemType.FLOAT:
            self.__TextEditor = QLineEdit()
            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(2, 0)
        elif itemtype == BswDetailItemType.INTEGER:
            self.__TextEditor = QLineEdit()
            HBoxLayout.addWidget(self.__TextEditor)
            HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(2, 0)
        elif itemtype == BswDetailItemType.ENUM:
            self.__EnumComboBox = QComboBox()
            self.__EnumComboBox.setEditable(True)
            HBoxLayout.addWidget(self.__EnumComboBox)
            HBoxLayout.setStretch(1, 1)
            space = QFrame()
            space.setFixedWidth(20)
            HBoxLayout.addWidget(space)
            HBoxLayout.setStretch(2, 0)
        elif itemtype == BswDetailItemType.BOOL:
            self.__BoolCheckBox = QCheckBox()
            HBoxLayout.addWidget(self.__BoolCheckBox)
            HBoxLayout.setStretch(1, 0)
            HBoxLayout.addStretch(1)
        elif itemtype == BswDetailItemType.REFERENCE:
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
        if self.itemtype == BswDetailItemType.STRING:
            self.__TextEditor.setText(value)
        elif self.itemtype == BswDetailItemType.FLOAT:
            self.__TextEditor.setText(value)
        elif self.itemtype == BswDetailItemType.INTEGER:
            self.__TextEditor.setText(value)
        elif self.itemtype == BswDetailItemType.ENUM:
            self.__EnumComboBox.setCurrentText(value)
        elif self.itemtype == BswDetailItemType.BOOL:
            if value is None:
                self.__BoolCheckBox.setChecked(False)
            elif value.upper() == 'TRUE':
                self.__BoolCheckBox.setChecked(True)
            elif value.upper() == '1':
                self.__BoolCheckBox.setChecked(True)
            else:
                self.__BoolCheckBox.setChecked(False)
        elif self.itemtype == BswDetailItemType.REFERENCE:
            self.__TextEditor.setText(value)
        self.isvaluesetting = False

    def getValue(self) -> str:
        if self.itemtype == BswDetailItemType.STRING:
            return self.__TextEditor.getText()
        elif self.itemtype == BswDetailItemType.FLOAT:
            return self.__TextEditor.getText()
        elif self.itemtype == BswDetailItemType.INTEGER:
            return self.__TextEditor.getText()
        elif self.itemtype == BswDetailItemType.ENUM:
            return self.__EnumComboBox.currentText()
        elif self.itemtype == BswDetailItemType.BOOL:
            if self.__BoolCheckBox.isChecked():
                return "true"
            else:
                return "false"
        elif self.itemtype == BswDetailItemType.REFERENCE:
            return self.__TextEditor.getText()
        return ''
