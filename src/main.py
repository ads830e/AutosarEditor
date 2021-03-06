
from AREditor.AREditorWindow import *

'''
def PrintARAttrs(ARObject):
    if not isinstance(ARObject, AUTOSAR_00049_STRICT_COMPACT.GeneratedsSuper):
        return

    if not hasattr(ARObject, 'member_data_items_'):
        return

    print(type(ARObject).__name__)
    print(ARUtils.IsARObjectType(type(ARObject).__name__))

    member_data_items_ = getattr(ARObject, 'member_data_items_')

    for key in member_data_items_.keys():
        MemberSpec = member_data_items_[key];

        if MemberSpec.name == 'S':
            continue
        elif MemberSpec.name == 'T':
            continue

    for key in member_data_items_.keys():
        MemberSpec = member_data_items_[key];

        if MemberSpec.name == 'S':
            continue
        elif MemberSpec.name == 'T':
            continue

        attrval = getattr(ARObject, MemberSpec.name)

        if attrval != None:
            printtype = False
            if isinstance(attrval, list):
                if attrval:
                    printtype = True
                # end
            else:
                printtype = True

            if printtype:
                print("\tname:" + MemberSpec.name)
                if isinstance(MemberSpec.data_type, list):
                    for data_typei in MemberSpec.data_type:
                        print("\ttype:" + re.sub(r"[\W]", "_", re.sub(r"^AR:", "", data_typei)))
                    # end
                else:
                    print("\ttype:" + re.sub(r"[\W]", "_", re.sub(r"^AR:", "", MemberSpec.data_type)))

            if isinstance(attrval, list):
                if attrval:
                    for attrvali in attrval:
                        PrintARAttrs(attrvali)
                        if isinstance(attrvali, AUTOSAR_00049_STRICT_COMPACT.GeneratedsSuper):
                            PrintARAttrs(attrvali)
                        else:
                            pass
                            # print("\tvalue:"+attrvali)
            else:
                if isinstance(attrval, AUTOSAR_00049_STRICT_COMPACT.GeneratedsSuper):
                    PrintARAttrs(attrval)
                else:
                    pass
                    # print("\tvalue:"+attrval)
'''

if __name__ == '__main__':
    # ??????pyqt5???????????????????????????????????????????????????sys.argv???????????????????????????????????????????????????
    app = QApplication(sys.argv)

    w = AREditorWindow()

    w.move(100, 100)

    w.show()

    # ??????exit()???????????????????????????????????????
    # ???exec_()??????????????????????????????????????????Python?????????????????????exec_()??????
    sys.exit(app.exec_())
    
