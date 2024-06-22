# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cti_file_making_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QListView, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_cti_making_dialog(object):
    def setupUi(self, cti_making_dialog):
        if not cti_making_dialog.objectName():
            cti_making_dialog.setObjectName(u"cti_making_dialog")
        cti_making_dialog.resize(500, 600)
        cti_making_dialog.setMinimumSize(QSize(500, 600))
        font = QFont()
        font.setPointSize(12)
        cti_making_dialog.setFont(font)
        cti_making_dialog.setWindowTitle(u"SPColumn File Generator")
        cti_making_dialog.setModal(False)
        self.gridLayout = QGridLayout(cti_making_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(cti_making_dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lb_status = QLabel(self.frame)
        self.lb_status.setObjectName(u"lb_status")
        self.lb_status.setAutoFillBackground(False)
        self.lb_status.setFrameShadow(QFrame.Shadow.Raised)
        self.lb_status.setTextFormat(Qt.TextFormat.PlainText)

        self.gridLayout_2.addWidget(self.lb_status, 2, 0, 1, 2)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 300))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_2 = QFrame(self.groupBox)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.lview_availCTI = QListView(self.frame_2)
        self.lview_availCTI.setObjectName(u"lview_availCTI")
        self.lview_availCTI.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.lview_availCTI.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.verticalLayout.addWidget(self.lview_availCTI)


        self.horizontalLayout.addWidget(self.frame_2)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 2)

        self.t_action = QTextEdit(self.frame)
        self.t_action.setObjectName(u"t_action")
        self.t_action.setEnabled(True)
        self.t_action.setMaximumSize(QSize(16777215, 200))
        self.t_action.setInputMethodHints(Qt.InputMethodHint.ImhMultiLine)
        self.t_action.setFrameShape(QFrame.Shape.Box)
        self.t_action.setFrameShadow(QFrame.Shadow.Sunken)
        self.t_action.setLineWidth(1)
        self.t_action.setReadOnly(True)

        self.gridLayout_2.addWidget(self.t_action, 3, 0, 1, 2)

        self.pb_makefile = QPushButton(self.frame)
        self.pb_makefile.setObjectName(u"pb_makefile")

        self.gridLayout_2.addWidget(self.pb_makefile, 1, 1, 1, 1)

        self.pb_selectall = QPushButton(self.frame)
        self.pb_selectall.setObjectName(u"pb_selectall")

        self.gridLayout_2.addWidget(self.pb_selectall, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(cti_making_dialog)

        QMetaObject.connectSlotsByName(cti_making_dialog)
    # setupUi

    def retranslateUi(self, cti_making_dialog):
        self.lb_status.setText(QCoreApplication.translate("cti_making_dialog", u"Status", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("cti_making_dialog", u"Available CTI files", None))
        self.t_action.setMarkdown("")
        self.t_action.setHtml(QCoreApplication.translate("cti_making_dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.t_action.setPlaceholderText(QCoreApplication.translate("cti_making_dialog", u"Tracking log", None))
        self.pb_makefile.setText(QCoreApplication.translate("cti_making_dialog", u"Make File(s)", None))
        self.pb_selectall.setText(QCoreApplication.translate("cti_making_dialog", u"Select All", None))
        pass
    # retranslateUi

