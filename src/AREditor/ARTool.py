import sys

import re
import os

from enum import Enum
import pathlib

import copy

from Autosar_xsd import AUTOSAR_00049_STRICT_COMPACT


class ARUtils:
    def __init__(self):
        pass

    @staticmethod
    def IsStrEmpty(s: str) -> bool:
        if not s:
            return True
        elif len(s) == 0:
            return True
        elif s.isspace():
            return True
        else:
            return False

    @staticmethod
    def Read(FileName: str):
        AUTOSAR_00049_STRICT_COMPACT.UseCapturedNS_ = False
        return AUTOSAR_00049_STRICT_COMPACT.parse(FileName, True)

    @staticmethod
    def Write(FileName: str, ARObject):
        AUTOSAR_00049_STRICT_COMPACT.UseCapturedNS_ = False
        if not isinstance(ARObject, AUTOSAR_00049_STRICT_COMPACT.GeneratedsSuper):
            return
        # end
        outfile = open(FileName, 'w')
        outfile.write('<?xml version="1.0" ?>\n')
        ARObject.export(outfile, 0)
        outfile.close()
        return

    @staticmethod
    def Merge(ARObject1, ARObject2):
        if (ARObject1) & (not ARObject2):
            return copy.deepcopy(ARObject1)
        elif (not ARObject1) & (ARObject2):
            return copy.deepcopy(ARObject2)
        elif (not ARObject1) & (not ARObject2):
            return None
        elif type(ARObject1) != type(ARObject2):
            # type not match,return none
            print("Error: Type not match {} {}\n", type(ARObject1), type(ARObject2))
            return None

        if not isinstance(ARObject2, AUTOSAR_00049_STRICT_COMPACT.GeneratedsSuper):
            return copy.deepcopy(ARObject2)

        if not hasattr(ARObject2, 'member_data_items_'):
            # nothing to copy
            print("Error: No Member member_data_items_\n")
            return None

        ret = copy.deepcopy(ARObject1)

        member_data_items_ = getattr(ARObject2, 'member_data_items_')
        for key in member_data_items_.keys():
            MemberSpec = member_data_items_[key]

            if MemberSpec.name == 'S':
                continue
            elif MemberSpec.name == 'T':
                continue

            attrval1 = getattr(ret, MemberSpec.name)
            attrval2 = getattr(ARObject2, MemberSpec.name)

            if not attrval2:
                continue
            elif not attrval1:
                setattr(ret, MemberSpec.name, copy.deepcopy(attrval2))
                continue

            # attrval1 and attrval2 not None here

            if isinstance(attrval1, list) & isinstance(attrval2, list):
                # list combine
                setattr(ret, MemberSpec.name, attrval1 + attrval2)
                continue
            else:
                setattr(ret, MemberSpec.name, ARUtils.Merge(attrval1, attrval2))
        return ret

    @staticmethod
    def IsARObjectType(name: str) -> bool:
        if not getattr(AUTOSAR_00049_STRICT_COMPACT, '__dict__', {}).get(name):
            return False
        else:
            return True

    @staticmethod
    def GetAllArxmlsInDirNoRecursive(dirpath: str):
        p = pathlib.Path(dirpath)
        return p.glob("*.arxml")

    @staticmethod
    def GetAllArxmlsInDirRecursive(dirpath: str):
        p = pathlib.Path(dirpath)
        return p.rglob("*.arxml")


class ARXmlFile:
    Autosar = None
    FileName = None

    def __init__(self):
        pass

    def Load(self):
        if not self.FileName:
            self.Autosar = None
            return
        else:
            self.Autosar = ARUtils.Read(self.FileName)
            return
        pass

    def Save(self):
        ARUtils.Write(self.FileName, self.Autosar)


class ARTool:
    ARXmlFiles = list()
    TypeToObjectsDict = dict()
    PathToObjectsDict = dict()
    ObjectToPathDict = dict()

    def __init__(self):
        self.ARXmlFiles = list()
        self.TypeToObjectsDict = dict()
        self.PathToObjectsDict = dict()
        self.ObjectToPathDict = dict()
        return

    def _LoadFile(self, filename: str):
        aRXmlFile = ARXmlFile()
        aRXmlFile.FileName = filename
        aRXmlFile.Load()
        self.ARXmlFiles.append(aRXmlFile)
        self._SortARObjectForSearch(aRXmlFile.Autosar)
        return

    def _LoadFiles(self, filenames: list):
        if not filenames:
            return
        for filename in filenames:
            self._LoadFile(filename)
        return

    def LoadFile(self, filename: str):
        self._LoadFile(filename)
        return

    def LoadFiles(self, filenames: list):
        self._LoadFiles(filenames)
        return

    def LoadDirNoRecursive(self, dirpath: str):
        self._LoadFiles(ARUtils.GetAllArxmlsInDirNoRecursive(dirpath))
        return

    def LoadDirRecursive(self, dirpath: str):
        self._LoadFiles(ARUtils.GetAllArxmlsInDirRecursive(dirpath))
        return

    def SaveAll(self):
        for aRXmlFile in self.ARXmlFiles:
            aRXmlFile.Save()
            pass
        return

    def Clear(self):
        self.ARXmlFiles = list()
        self.TypeToObjectsDict = dict()
        self.PathToObjectsDict = dict()
        self.ObjectToPathDict = dict()
        return

    def AddARObject(self, ARObject, ARObjectParent=None):
        if not ARObject:
            return
        if isinstance(ARObject, AUTOSAR_00049_STRICT_COMPACT.AUTOSAR):
            # self._SortARObjectForSearch(ARObject)
            return
        elif not ARObjectParent:
            # error
            return
        else:
            pass
        return

    def DeleteARObject(self, ARObject):
        return

    def _SortARObjectForSearch(self, ARObject, ARObjectParent=None):
        if (not isinstance(ARObject, AUTOSAR_00049_STRICT_COMPACT.AUTOSAR)) & (not ARObjectParent):
            # error
            return
        elif isinstance(ARObject, AUTOSAR_00049_STRICT_COMPACT.AUTOSAR):
            self.__SortARObjectForSearch(ARObject)
        else:
            pass
        return

    def __SortARObjectForSearch(self, ARObject, ParentPath=''):
        if not isinstance(ARObject, AUTOSAR_00049_STRICT_COMPACT.GeneratedsSuper):
            return
        if not hasattr(ARObject, 'member_data_items_'):
            # nothing
            print("Error: No Member member_data_items_\n")
            return

        ShortName = self.__GetARObjectShortName(ARObject)
        ShortDefRef = self.__GetARObjectShortDefRef(ARObject)

        ThisName = None
        if ShortName:
            ThisName = ShortName
        elif ShortDefRef:
            ThisName = ShortDefRef

        ThisPath = ParentPath
        if ThisName:
            ThisPath = ParentPath + '/' + ThisName

            # path to object
            if self.PathToObjectsDict.__contains__(ThisPath):
                self.PathToObjectsDict.get(ThisPath).append(ARObject)
            else:
                self.PathToObjectsDict[ThisPath] = [ARObject]
            # object to path
            if not self.ObjectToPathDict.__contains__(ARObject):
                self.ObjectToPathDict[ARObject] = ThisPath

        if ShortName:
            # type to object
            if self.TypeToObjectsDict.__contains__(type(ARObject)):
                self.TypeToObjectsDict.get(type(ARObject)).append(ARObject)
            else:
                self.TypeToObjectsDict[type(ARObject)] = [ARObject]

        if ThisName:
            # print(ThisPath)
            pass

        member_data_items_ = getattr(ARObject, 'member_data_items_')
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
                # list combine
                for attrvali in attrval:
                    self.__SortARObjectForSearch(attrvali, ThisPath)
                continue
            else:
                self.__SortARObjectForSearch(attrval, ThisPath)

    def GetARObjectShortName(self, ARObject) -> str:
        return self.__GetARObjectShortName(ARObject)

    @staticmethod
    def __GetARObjectShortName(ARObject) -> str:
        if not isinstance(ARObject, AUTOSAR_00049_STRICT_COMPACT.GeneratedsSuper):
            return None
        elif not hasattr(ARObject, 'member_data_items_'):
            return None

        member_data_items_ = getattr(ARObject, 'member_data_items_')

        if not member_data_items_.__contains__('SHORT_NAME'):
            return None

        SHORT_NAME = getattr(ARObject, 'SHORT_NAME')

        if not SHORT_NAME:
            return None

        if not hasattr(SHORT_NAME, 'get_valueOf_'):
            return None

        return SHORT_NAME.get_valueOf_()

    def GetARObjectShortDefRef(self, ARObject) -> str:
        return self.__GetARObjectShortDefRef(ARObject)

    @staticmethod
    def __GetARObjectShortDefRef(ARObject) -> str:
        ret = ARTool.__GetARObjectDefRef(ARObject)
        if not ret:
            return None
        return os.path.split(ret)[-1]

    def GetARObjectDefRef(self, ARObject) -> str:
        return self.__GetARObjectDefRef(ARObject)

    @staticmethod
    def __GetARObjectDefRef(ARObject) -> str:
        if not isinstance(ARObject, AUTOSAR_00049_STRICT_COMPACT.GeneratedsSuper):
            return None
        elif not hasattr(ARObject, 'member_data_items_'):
            return None

        member_data_items_ = getattr(ARObject, 'member_data_items_')

        if not member_data_items_.__contains__('DEFINITION_REF'):
            return None

        DEFINITION_REF = getattr(ARObject, 'DEFINITION_REF')

        if not DEFINITION_REF:
            return None

        if not hasattr(DEFINITION_REF, 'get_valueOf_'):
            return None

        return DEFINITION_REF.get_valueOf_()

    def GetPath(self, ARObject):
        if self.ObjectToPathDict.__contains__(ARObject):
            return self.ObjectToPathDict[ARObject]
        else:
            return None
