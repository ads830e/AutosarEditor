from configparser import ConfigParser

from .AREditorWidgetAdaptive import *
from .AREditorWidgetClassic import *
from .AREditorWidgetArxml import *
from .AREditorWidgetBsw import *
from .ARTool import ARTool, ARUtils


class AREditorWindow(QMainWindow):
    aRTool = ARTool()
    CfgParser = ConfigParser()
    CfgParserFileName = "AREditor.ini"
    projdir = None

    def __init__(self):
        super().__init__()

        self.CfgParser.read(self.CfgParserFileName)

        QToolTip.setFont(QFont('SansSerif', 10))

        self.resize(1000, 700)
        self.setMinimumSize(320, 240)

        self.move(0, 0)

        self.setWindowTitle('Autosar Editor')

        # self.setToolTip('This is a AREditorWindow')

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        self.menubar = self.menuBar()

        self.fileMenu = self.menubar.addMenu('&File')

        openAction = QAction('&Open Project Directory', self)
        openAction.triggered.connect(self.openActiontriggered)
        self.fileMenu.addAction(openAction)

        saveAction = QAction('&Save', self)
        saveAction.triggered.connect(self.saveActiontriggered)
        self.fileMenu.addAction(saveAction)

        reloadAction = QAction('&Reload', self)
        reloadAction.triggered.connect(self.reloadActiontriggered)
        self.fileMenu.addAction(reloadAction)

        closeAction = QAction('&Close', self)
        closeAction.triggered.connect(self.closeActiontriggered)
        self.fileMenu.addAction(closeAction)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitActiontriggered)
        self.fileMenu.addAction(exitAction)

        toolsMenu = self.menubar.addMenu('&Tools')

        helpMenu = self.menubar.addMenu('&Help')

        aboutAction = QAction('&About', self)
        aboutAction.triggered.connect(self.aboutActiontriggered)
        helpMenu.addAction(aboutAction)

        self.widget_arxml = AREditorWidgetArxml()
        self.widget_arxml.SetARTool(self.aRTool)
        self.widget_arxml.ReloadUI()
        self.widget_arxml.unSavedSignal.connect(self.IndicateUnSaveByTitle)

        self.widget_ap = AREditorWidgetAdaptive()
        self.widget_ap.SetARTool(self.aRTool)
        self.widget_ap.ReloadUI()
        self.widget_ap.unSavedSignal.connect(self.IndicateUnSaveByTitle)

        self.widget_cp = AREditorWidgetClassic()
        self.widget_cp.SetARTool(self.aRTool)
        self.widget_cp.ReloadUI()
        self.widget_cp.unSavedSignal.connect(self.IndicateUnSaveByTitle)

        self.widget_bsw = AREditorWidgetBsw()
        self.widget_bsw.SetARTool(self.aRTool)
        self.widget_bsw.ReloadUI()
        self.widget_bsw.unSavedSignal.connect(self.IndicateUnSaveByTitle)

        __tabs = QTabWidget()

        __tabs.addTab(self.widget_arxml, "Arxml")
        __tabs.addTab(self.widget_ap, "Adaptive")
        __tabs.addTab(self.widget_cp, "Classic")
        __tabs.addTab(self.widget_bsw, "Module Configuration")

        self.setCentralWidget(__tabs)

        self.ClearStatusBar()

        self.widget_arxml.ReloadUI()
        self.widget_ap.ReloadUI()
        self.widget_cp.ReloadUI()
        self.widget_bsw.ReloadUI()

    def ClearStatusBar(self):
        self.statusbar.showMessage('')

    def aboutActiontriggered(self):
        QMessageBox.information(self, "About", "Autosar Editor Developed By TuoQiang！", QMessageBox.Yes)
        return

    def openActiontriggered(self):
        if not ARUtils.IsStrEmpty(self.projdir):
            ret = QMessageBox.information(self, "open", "Are you sure to open another dictionary? All things will be lost!",
                                      QMessageBox.Yes | QMessageBox.No)
            if QMessageBox.Yes != ret:
                return
            pass

        #close
        self.aRTool.Clear()
        self.projdir=None
        self.setWindowTitle("Autosar Editor")
        self.widget_arxml.ReloadUI()
        self.widget_ap.ReloadUI()
        self.widget_cp.ReloadUI()
        self.widget_bsw.ReloadUI()

        #select dir
        lastdir = self._ReadSetting('AREditorWindow', 'OpenProjectDirectory')
        self.projdir = QFileDialog.getExistingDirectory(self, 'Open file', lastdir)
        if ARUtils.IsStrEmpty(self.projdir):
            return
        self._WriteSetting('AREditorWindow', 'OpenProjectDirectory', self.projdir)

        #open
        self.aRTool.LoadDirRecursive(self.projdir)

        self.widget_arxml.ReloadUI()
        self.widget_ap.ReloadUI()
        self.widget_cp.ReloadUI()
        self.widget_bsw.ReloadUI()

        self.setWindowTitle(self.projdir+" - Autosar Editor")

        return

    def saveActiontriggered(self):
        if ARUtils.IsStrEmpty(self.projdir):
            return

        ret = QMessageBox.information(self, "Save", "Are you sure to Save? All thing will be written to disk!", QMessageBox.Yes | QMessageBox.No)
        if QMessageBox.Yes != ret:
            return
        self.aRTool.SaveAll()

        self.setWindowTitle(self.projdir + " - Autosar Editor")

        return

    def reloadActiontriggered(self):
        if ARUtils.IsStrEmpty(self.projdir):
            return

        ret = QMessageBox.information(self, "Reload", "Are you sure to Reload? All things will be lost!", QMessageBox.Yes | QMessageBox.No)
        if QMessageBox.Yes != ret:
            return

        self.aRTool.Clear()
        self.widget_arxml.ReloadUI()
        self.widget_ap.ReloadUI()
        self.widget_cp.ReloadUI()
        self.widget_bsw.ReloadUI()

        self.repaint()

        self.aRTool.LoadDirRecursive(self.projdir)

        self.setWindowTitle(self.projdir + " - Autosar Editor")
        self.widget_arxml.ReloadUI()
        self.widget_ap.ReloadUI()
        self.widget_cp.ReloadUI()
        self.widget_bsw.ReloadUI()
        return

    def closeActiontriggered(self):
        if ARUtils.IsStrEmpty(self.projdir):
            return

        ret = QMessageBox.information(self, "Close", "Are you sure to Close? All things will be lost!", QMessageBox.Yes | QMessageBox.No)
        if QMessageBox.Yes != ret:
            return

        self.projdir=None
        self.aRTool.Clear()

        self.setWindowTitle('Autosar Editor')

        self.widget_arxml.ReloadUI()
        self.widget_ap.ReloadUI()
        self.widget_cp.ReloadUI()
        self.widget_bsw.ReloadUI()
        return

    def exitActiontriggered(self):
        ret = QMessageBox.information(self, "Exit", "Are you sure to Exit? All things will be lost!", QMessageBox.Yes | QMessageBox.No)
        if QMessageBox.Yes != ret:
            return

        self.projdir = None
        self.setWindowTitle('Autosar Editor')
        #force quit without save
        qApp.quit()
        return

    def IndicateUnSaveByTitle(self):
        if ARUtils.IsStrEmpty(self.projdir):
            return
        self.setWindowTitle("*"+self.projdir + " - Autosar Editor")

    def _ReadSetting(self, section, option):
        ret = None
        try:
            ret = self.CfgParser.get(section, option)
        except Exception as e:
            ret = None
        finally:
            return ret

    def _WriteSetting(self, section, option, value: str):
        try:
            if not self.CfgParser.has_section(section):
                self.CfgParser.add_section(section)
            self.CfgParser.set(section, option, value)
            outfile = open(self.CfgParserFileName, 'w')
            self.CfgParser.write(outfile)
            outfile.close()
        except Exception as e:
            pass
        finally:
            pass
