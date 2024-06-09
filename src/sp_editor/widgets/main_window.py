# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QStatusBar,
    QToolBar,
    QWidget,
)
import icons_rc


class Ui_mw_Main(object):
    def setupUi(self, mw_Main):
        if not mw_Main.objectName():
            mw_Main.setObjectName("mw_Main")
        mw_Main.resize(1366, 768)
        mw_Main.setMinimumSize(QSize(1366, 768))
        font = QFont()
        font.setPointSize(12)
        mw_Main.setFont(font)
        mw_Main.setIconSize(QSize(24, 24))
        mw_Main.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.action_New = QAction(mw_Main)
        self.action_New.setObjectName("action_New")
        icon = QIcon(QIcon.fromTheme("document-new"))
        self.action_New.setIcon(icon)
        self.action_New.setFont(font)
        self.action_Open = QAction(mw_Main)
        self.action_Open.setObjectName("action_Open")
        icon1 = QIcon(QIcon.fromTheme("document-open"))
        self.action_Open.setIcon(icon1)
        self.action_Open.setFont(font)
        self.action_Save = QAction(mw_Main)
        self.action_Save.setObjectName("action_Save")
        icon2 = QIcon(QIcon.fromTheme("document-save"))
        self.action_Save.setIcon(icon2)
        self.action_Save.setFont(font)
        self.action_Quit = QAction(mw_Main)
        self.action_Quit.setObjectName("action_Quit")
        icon3 = QIcon(QIcon.fromTheme("window-close"))
        self.action_Quit.setIcon(icon3)
        self.action_Quit.setFont(font)
        self.a_GeneralInfor = QAction(mw_Main)
        self.a_GeneralInfor.setObjectName("a_GeneralInfor")
        icon4 = QIcon(QIcon.fromTheme("document-properties"))
        self.a_GeneralInfor.setIcon(icon4)
        self.a_Groups = QAction(mw_Main)
        self.a_Groups.setObjectName("a_Groups")
        icon5 = QIcon()
        icon5.addFile(":/Btn/Group_edit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.a_Groups.setIcon(icon5)
        self.a_Cases = QAction(mw_Main)
        self.a_Cases.setObjectName("a_Cases")
        icon6 = QIcon()
        icon6.addFile(":/Btn/Calculation_Case.png", QSize(), QIcon.Normal, QIcon.Off)
        self.a_Cases.setIcon(icon6)
        self.a_GetAllForce = QAction(mw_Main)
        self.a_GetAllForce.setObjectName("a_GetAllForce")
        icon7 = QIcon()
        icon7.addFile(":/Btn/Force.png", QSize(), QIcon.Normal, QIcon.Off)
        self.a_GetAllForce.setIcon(icon7)
        self.a_MakeSPcolumn = QAction(mw_Main)
        self.a_MakeSPcolumn.setObjectName("a_MakeSPcolumn")
        icon8 = QIcon()
        icon8.addFile(":/Btn/spcolumn-icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.a_MakeSPcolumn.setIcon(icon8)
        self.a_BatchProcessor = QAction(mw_Main)
        self.a_BatchProcessor.setObjectName("a_BatchProcessor")
        icon9 = QIcon()
        icon9.addFile(":/Btn/parallel.png", QSize(), QIcon.Normal, QIcon.Off)
        self.a_BatchProcessor.setIcon(icon9)
        self.a_Doc = QAction(mw_Main)
        self.a_Doc.setObjectName("a_Doc")
        icon10 = QIcon(QIcon.fromTheme("help-browser"))
        self.a_Doc.setIcon(icon10)
        self.a_About = QAction(mw_Main)
        self.a_About.setObjectName("a_About")
        icon11 = QIcon(QIcon.fromTheme("help-about"))
        self.a_About.setIcon(icon11)
        self.a_ImportEtabs = QAction(mw_Main)
        self.a_ImportEtabs.setObjectName("a_ImportEtabs")
        icon12 = QIcon()
        icon12.addFile(":/Btn/etabs logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.a_ImportEtabs.setIcon(icon12)
        self.a_ImportEtabs.setFont(font)
        self.a_Print = QAction(mw_Main)
        self.a_Print.setObjectName("a_Print")
        icon13 = QIcon(QIcon.fromTheme("document-print"))
        self.a_Print.setIcon(icon13)
        self.a_Print.setFont(font)
        self.a_MaterialProp = QAction(mw_Main)
        self.a_MaterialProp.setObjectName("a_MaterialProp")
        icon14 = QIcon()
        icon14.addFile(":/Btn/material_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.a_MaterialProp.setIcon(icon14)
        self.a_MaterialProp.setFont(font)
        self.a_BarSet = QAction(mw_Main)
        self.a_BarSet.setObjectName("a_BarSet")
        icon15 = QIcon()
        icon15.addFile(":/Btn/rebar_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.a_BarSet.setIcon(icon15)
        self.a_BarSet.setFont(font)
        self.centralwidget = QWidget(mw_Main)
        self.centralwidget.setObjectName("centralwidget")
        mw_Main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mw_Main)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1366, 33))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_File.setFont(font)
        self.m_Define = QMenu(self.menubar)
        self.m_Define.setObjectName("m_Define")
        self.m_Define.setFont(font)
        self.m_Analyze = QMenu(self.menubar)
        self.m_Analyze.setObjectName("m_Analyze")
        self.m_Analyze.setFont(font)
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuHelp.setFont(font)
        mw_Main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mw_Main)
        self.statusbar.setObjectName("statusbar")
        mw_Main.setStatusBar(self.statusbar)
        self.tb_File = QToolBar(mw_Main)
        self.tb_File.setObjectName("tb_File")
        mw_Main.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tb_File)
        self.tb_Define = QToolBar(mw_Main)
        self.tb_Define.setObjectName("tb_Define")
        mw_Main.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tb_Define)
        self.tb_Analyze = QToolBar(mw_Main)
        self.tb_Analyze.setObjectName("tb_Analyze")
        mw_Main.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tb_Analyze)
        self.tb_Help = QToolBar(mw_Main)
        self.tb_Help.setObjectName("tb_Help")
        mw_Main.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tb_Help)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.m_Define.menuAction())
        self.menubar.addAction(self.m_Analyze.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menu_File.addAction(self.action_New)
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.a_ImportEtabs)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.a_Print)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.m_Define.addAction(self.a_GeneralInfor)
        self.m_Define.addSeparator()
        self.m_Define.addAction(self.a_MaterialProp)
        self.m_Define.addAction(self.a_BarSet)
        self.m_Define.addSeparator()
        self.m_Define.addAction(self.a_Groups)
        self.m_Define.addAction(self.a_Cases)
        self.m_Analyze.addAction(self.a_GetAllForce)
        self.m_Analyze.addAction(self.a_MakeSPcolumn)
        self.m_Analyze.addAction(self.a_BatchProcessor)
        self.menuHelp.addAction(self.a_Doc)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.a_About)
        self.tb_File.addAction(self.action_New)
        self.tb_File.addAction(self.action_Open)
        self.tb_File.addAction(self.action_Save)
        self.tb_File.addAction(self.a_Print)
        self.tb_File.addSeparator()
        self.tb_File.addAction(self.a_ImportEtabs)
        self.tb_Define.addAction(self.a_GeneralInfor)
        self.tb_Define.addSeparator()
        self.tb_Define.addAction(self.a_MaterialProp)
        self.tb_Define.addAction(self.a_BarSet)
        self.tb_Define.addSeparator()
        self.tb_Define.addAction(self.a_Groups)
        self.tb_Define.addAction(self.a_Cases)
        self.tb_Analyze.addAction(self.a_GetAllForce)
        self.tb_Analyze.addSeparator()
        self.tb_Analyze.addAction(self.a_MakeSPcolumn)
        self.tb_Analyze.addAction(self.a_BatchProcessor)
        self.tb_Help.addAction(self.a_Doc)
        self.tb_Help.addAction(self.a_About)

        self.retranslateUi(mw_Main)

        QMetaObject.connectSlotsByName(mw_Main)

    # setupUi

    def retranslateUi(self, mw_Main):
        mw_Main.setWindowTitle(QCoreApplication.translate("mw_Main", "SP-editor", None))
        self.action_New.setText(QCoreApplication.translate("mw_Main", "&New", None))
        # if QT_CONFIG(shortcut)
        self.action_New.setShortcut(
            QCoreApplication.translate("mw_Main", "Ctrl+N", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_Open.setText(QCoreApplication.translate("mw_Main", "&Open", None))
        # if QT_CONFIG(shortcut)
        self.action_Open.setShortcut(
            QCoreApplication.translate("mw_Main", "Ctrl+O", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_Save.setText(QCoreApplication.translate("mw_Main", "&Save", None))
        # if QT_CONFIG(shortcut)
        self.action_Save.setShortcut(
            QCoreApplication.translate("mw_Main", "Ctrl+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.action_Quit.setText(QCoreApplication.translate("mw_Main", "&Quit", None))
        # if QT_CONFIG(shortcut)
        self.action_Quit.setShortcut(
            QCoreApplication.translate("mw_Main", "Ctrl+Q", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.a_GeneralInfor.setText(
            QCoreApplication.translate("mw_Main", "&General Information", None)
        )
        self.a_Groups.setText(QCoreApplication.translate("mw_Main", "&Groups", None))
        # if QT_CONFIG(shortcut)
        self.a_Groups.setShortcut(QCoreApplication.translate("mw_Main", "Ctrl+G", None))
        # endif // QT_CONFIG(shortcut)
        self.a_Cases.setText(QCoreApplication.translate("mw_Main", "Load Cases", None))
        self.a_GetAllForce.setText(
            QCoreApplication.translate("mw_Main", "Get Forces", None)
        )
        self.a_MakeSPcolumn.setText(
            QCoreApplication.translate("mw_Main", "Generate SpCol Files", None)
        )
        self.a_BatchProcessor.setText(
            QCoreApplication.translate("mw_Main", "Batch Processor", None)
        )
        self.a_Doc.setText(QCoreApplication.translate("mw_Main", "Documentation", None))
        # if QT_CONFIG(shortcut)
        self.a_Doc.setShortcut(QCoreApplication.translate("mw_Main", "F1", None))
        # endif // QT_CONFIG(shortcut)
        self.a_About.setText(
            QCoreApplication.translate("mw_Main", "About SP-editor", None)
        )
        self.a_ImportEtabs.setText(
            QCoreApplication.translate("mw_Main", "Import", None)
        )
        # if QT_CONFIG(shortcut)
        self.a_ImportEtabs.setShortcut(
            QCoreApplication.translate("mw_Main", "Ctrl+E", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.a_Print.setText(QCoreApplication.translate("mw_Main", "Print", None))
        # if QT_CONFIG(shortcut)
        self.a_Print.setShortcut(QCoreApplication.translate("mw_Main", "Ctrl+P", None))
        # endif // QT_CONFIG(shortcut)
        self.a_MaterialProp.setText(
            QCoreApplication.translate("mw_Main", "&Material Properties", None)
        )
        self.a_BarSet.setText(QCoreApplication.translate("mw_Main", "Bar Sets", None))
        self.menu_File.setTitle(QCoreApplication.translate("mw_Main", "&File", None))
        self.m_Define.setTitle(QCoreApplication.translate("mw_Main", "&Define", None))
        self.m_Analyze.setTitle(QCoreApplication.translate("mw_Main", "Analyze", None))
        self.menuHelp.setTitle(QCoreApplication.translate("mw_Main", "Help", None))
        self.tb_File.setWindowTitle(QCoreApplication.translate("mw_Main", "File", None))
        self.tb_Define.setWindowTitle(
            QCoreApplication.translate("mw_Main", "Define", None)
        )
        self.tb_Analyze.setWindowTitle(
            QCoreApplication.translate("mw_Main", "Analyze", None)
        )
        self.tb_Help.setWindowTitle(QCoreApplication.translate("mw_Main", "Help", None))

    # retranslateUi
