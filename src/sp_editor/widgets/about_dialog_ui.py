# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)
import icons_rc

class Ui_d_About(object):
    def setupUi(self, d_About):
        if not d_About.objectName():
            d_About.setObjectName(u"d_About")
        d_About.resize(360, 480)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(d_About.sizePolicy().hasHeightForWidth())
        d_About.setSizePolicy(sizePolicy)
        d_About.setMinimumSize(QSize(360, 480))
        d_About.setMaximumSize(QSize(360, 480))
        font = QFont()
        font.setPointSize(12)
        d_About.setFont(font)
        self.gridLayout = QGridLayout(d_About)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.pb_OK = QPushButton(d_About)
        self.pb_OK.setObjectName(u"pb_OK")

        self.gridLayout.addWidget(self.pb_OK, 1, 1, 1, 1)

        self.groupBox = QGroupBox(d_About)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(0, 420))
        self.groupBox.setMaximumSize(QSize(340, 420))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        self.groupBox.setFont(font1)
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(320, 380))
        self.frame.setMaximumSize(QSize(400, 380))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Plain)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 101, 81))
        self.label.setTextFormat(Qt.TextFormat.PlainText)
        self.label.setPixmap(QPixmap(u":/image and logo/SP-EDITOR_PNG.png"))
        self.label.setScaledContents(True)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 10, 180, 100))
        self.label_2.setMinimumSize(QSize(180, 100))
        self.label_2.setMaximumSize(QSize(180, 100))
        self.label_2.setSizeIncrement(QSize(100, 100))
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(False)
        self.label_2.setFont(font2)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignVCenter)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(15, 10, 91, 20))
        font3 = QFont()
        font3.setPointSize(8)
        font3.setBold(True)
        self.label_3.setFont(font3)
        self.label_3.setFrameShape(QFrame.Shape.NoFrame)
        self.label_3.setTextFormat(Qt.TextFormat.RichText)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 110, 301, 151))
        font4 = QFont()
        font4.setPointSize(8)
        font4.setBold(False)
        self.label_4.setFont(font4)
        self.label_4.setFrameShape(QFrame.Shape.NoFrame)
        self.label_4.setTextFormat(Qt.TextFormat.RichText)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(10, 90, 301, 20))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2 = QFrame(self.frame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(10, 260, 301, 20))
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 270, 301, 101))
        self.label_5.setFont(font4)
        self.label_5.setFrameShape(QFrame.Shape.NoFrame)
        self.label_5.setTextFormat(Qt.TextFormat.RichText)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.frame)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)


        self.retranslateUi(d_About)

        QMetaObject.connectSlotsByName(d_About)
    # setupUi

    def retranslateUi(self, d_About):
        d_About.setWindowTitle(QCoreApplication.translate("d_About", u"SP-editor", None))
        self.pb_OK.setText(QCoreApplication.translate("d_About", u"OK", None))
        self.groupBox.setTitle(QCoreApplication.translate("d_About", u"About", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("d_About", u"<html><head/><body><p><span style=\" font-size:8pt;\">Empowering Structural Engineers</span></p><p><span style=\" font-size:8pt;\">with seamless communication </span></p><p><span style=\" font-size:8pt;\">between SpColumn and ETABS</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("d_About", u"SP-Editor V0.1.0", None))
        self.label_4.setText(QCoreApplication.translate("d_About", u"<html><head/><body><p><span style=\" font-weight:700; text-decoration: underline;\">Description:</span></p><p>A shear wall design software that make connection </p><p>between ETABS and SpColumn</p><p><span style=\" font-weight:700; text-decoration: underline;\">Authors:</span></p><p>Do Thanh Tu, email: &quot;<span style=\" font-style:italic; text-decoration: underline;\">tado@thorntontomasetti.com</span>&quot;</p><p>Bui Quang Anh, email: &quot;<span style=\" font-style:italic; text-decoration: underline;\">abui@thorntontomasetti.com</span>&quot;</p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("d_About", u"<html><head/><body><p align=\"justify\"><span style=\" font-weight:700;\">THORNTON TOMASETTI VIETNAM </span></p><p><span style=\" font-weight:700;\">HO CHI MINH OFFICE</span></p><p><a href=\"https://www.thorntontomasetti.com/location/ho-chi-minh-city\"><span style=\" font-style:italic; text-decoration: underline; color:#0078d4;\">https://www.thorntontomasetti.com/location/ho-chi-minh-city</span></a></p><p>91 Pasteur, Ben Nghe Ward, District 1</p><p><br/></p></body></html>", None))
    # retranslateUi

