# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'batch_processor_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_BatchProcessorDialog(object):
    def setupUi(self, BatchProcessorDialog):
        if not BatchProcessorDialog.objectName():
            BatchProcessorDialog.setObjectName(u"BatchProcessorDialog")
        BatchProcessorDialog.resize(500, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BatchProcessorDialog.sizePolicy().hasHeightForWidth())
        BatchProcessorDialog.setSizePolicy(sizePolicy)
        BatchProcessorDialog.setMinimumSize(QSize(500, 600))
        BatchProcessorDialog.setMaximumSize(QSize(500, 600))
        self.verticalLayout = QVBoxLayout(BatchProcessorDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_tracking_screen = QLabel(BatchProcessorDialog)
        self.label_tracking_screen.setObjectName(u"label_tracking_screen")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(12)
        font.setBold(True)
        self.label_tracking_screen.setFont(font)
        self.label_tracking_screen.setFrameShape(QFrame.Shape.Box)
        self.label_tracking_screen.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_tracking_screen)

        self.frame = QFrame(BatchProcessorDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Plain)
        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(1)
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setObjectName(u"frame_layout")
        self.t_resultTextEdit = QTextEdit(self.frame)
        self.t_resultTextEdit.setObjectName(u"t_resultTextEdit")
        self.t_resultTextEdit.setMinimumSize(QSize(0, 0))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(11)
        self.t_resultTextEdit.setFont(font1)
        self.t_resultTextEdit.setFrameShape(QFrame.Shape.Panel)
        self.t_resultTextEdit.setFrameShadow(QFrame.Shadow.Sunken)
        self.t_resultTextEdit.setLineWidth(0)
        self.t_resultTextEdit.setTabChangesFocus(False)
        self.t_resultTextEdit.setReadOnly(True)

        self.frame_layout.addWidget(self.t_resultTextEdit)


        self.verticalLayout.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.typeGroupBox = QGroupBox(BatchProcessorDialog)
        self.typeGroupBox.setObjectName(u"typeGroupBox")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(12)
        self.typeGroupBox.setFont(font2)
        self.typeLayout = QGridLayout(self.typeGroupBox)
        self.typeLayout.setObjectName(u"typeLayout")
        self.cb_excel = QCheckBox(self.typeGroupBox)
        self.cb_excel.setObjectName(u"cb_excel")
        self.cb_excel.setEnabled(False)
        self.cb_excel.setChecked(True)

        self.typeLayout.addWidget(self.cb_excel, 0, 0, 1, 1)

        self.cb_word = QCheckBox(self.typeGroupBox)
        self.cb_word.setObjectName(u"cb_word")

        self.typeLayout.addWidget(self.cb_word, 0, 1, 1, 1)

        self.cb_pdf = QCheckBox(self.typeGroupBox)
        self.cb_pdf.setObjectName(u"cb_pdf")

        self.typeLayout.addWidget(self.cb_pdf, 0, 2, 1, 1)

        self.cb_text = QCheckBox(self.typeGroupBox)
        self.cb_text.setObjectName(u"cb_text")

        self.typeLayout.addWidget(self.cb_text, 1, 0, 1, 1)

        self.cb_csv = QCheckBox(self.typeGroupBox)
        self.cb_csv.setObjectName(u"cb_csv")

        self.typeLayout.addWidget(self.cb_csv, 1, 1, 1, 1)

        self.cb_dxf = QCheckBox(self.typeGroupBox)
        self.cb_dxf.setObjectName(u"cb_dxf")

        self.typeLayout.addWidget(self.cb_dxf, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.typeGroupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_startButton = QPushButton(BatchProcessorDialog)
        self.pb_startButton.setObjectName(u"pb_startButton")
        self.pb_startButton.setFont(font2)

        self.horizontalLayout.addWidget(self.pb_startButton)

        self.pb_showButton = QPushButton(BatchProcessorDialog)
        self.pb_showButton.setObjectName(u"pb_showButton")
        self.pb_showButton.setFont(font2)

        self.horizontalLayout.addWidget(self.pb_showButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(BatchProcessorDialog)

        QMetaObject.connectSlotsByName(BatchProcessorDialog)
    # setupUi

    def retranslateUi(self, BatchProcessorDialog):
        BatchProcessorDialog.setWindowTitle(QCoreApplication.translate("BatchProcessorDialog", u"Batch Processor", None))
        self.label_tracking_screen.setText(QCoreApplication.translate("BatchProcessorDialog", u"TRACKING SCREEN", None))
        self.typeGroupBox.setTitle(QCoreApplication.translate("BatchProcessorDialog", u"Output Type", None))
        self.cb_excel.setText(QCoreApplication.translate("BatchProcessorDialog", u"Excel", None))
        self.cb_word.setText(QCoreApplication.translate("BatchProcessorDialog", u"Word", None))
        self.cb_pdf.setText(QCoreApplication.translate("BatchProcessorDialog", u"PDF", None))
        self.cb_text.setText(QCoreApplication.translate("BatchProcessorDialog", u"Text", None))
        self.cb_csv.setText(QCoreApplication.translate("BatchProcessorDialog", u"CSV", None))
        self.cb_dxf.setText(QCoreApplication.translate("BatchProcessorDialog", u"DXF", None))
        self.pb_startButton.setText(QCoreApplication.translate("BatchProcessorDialog", u"Batch Processing", None))
        self.pb_showButton.setText(QCoreApplication.translate("BatchProcessorDialog", u"Show Result", None))
    # retranslateUi

