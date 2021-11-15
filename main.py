
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
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)

    w = AREditorWindow()

    w.move(100, 100)

    w.show()

    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())
    
