# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'generalInfor_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QGridLayout, QGroupBox, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_d_GeneralInfor(object):
    def setupUi(self, d_GeneralInfor):
        if not d_GeneralInfor.objectName():
            d_GeneralInfor.setObjectName(u"d_GeneralInfor")
        d_GeneralInfor.resize(400, 300)
        font = QFont()
        font.setPointSize(12)
        d_GeneralInfor.setFont(font)
        self.gridLayout = QGridLayout(d_GeneralInfor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pb_OK = QPushButton(d_GeneralInfor)
        self.pb_OK.setObjectName(u"pb_OK")

        self.gridLayout.addWidget(self.pb_OK, 1, 1, 1, 1)

        self.pb_Cancel = QPushButton(d_GeneralInfor)
        self.pb_Cancel.setObjectName(u"pb_Cancel")

        self.gridLayout.addWidget(self.pb_Cancel, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.groupBox = QGroupBox(d_GeneralInfor)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        self.groupBox.setFont(font1)
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.cb_DesignCode = QComboBox(self.groupBox)
        self.cb_DesignCode.addItem("")
        self.cb_DesignCode.addItem("")
        self.cb_DesignCode.addItem("")
        self.cb_DesignCode.setObjectName(u"cb_DesignCode")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cb_DesignCode)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.cb_UnitSystem = QComboBox(self.groupBox)
        self.cb_UnitSystem.addItem("")
        self.cb_UnitSystem.addItem("")
        self.cb_UnitSystem.setObjectName(u"cb_UnitSystem")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cb_UnitSystem)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.cb_BarSet = QComboBox(self.groupBox)
        self.cb_BarSet.addItem("")
        self.cb_BarSet.addItem("")
        self.cb_BarSet.addItem("")
        self.cb_BarSet.setObjectName(u"cb_BarSet")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cb_BarSet)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.cb_Confinement = QComboBox(self.groupBox)
        self.cb_Confinement.addItem("")
        self.cb_Confinement.addItem("")
        self.cb_Confinement.setObjectName(u"cb_Confinement")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.cb_Confinement)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.cb_SectionCapacity = QComboBox(self.groupBox)
        self.cb_SectionCapacity.addItem("")
        self.cb_SectionCapacity.addItem("")
        self.cb_SectionCapacity.setObjectName(u"cb_SectionCapacity")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.cb_SectionCapacity)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)


        self.retranslateUi(d_GeneralInfor)

        QMetaObject.connectSlotsByName(d_GeneralInfor)
    # setupUi

    def retranslateUi(self, d_GeneralInfor):
        d_GeneralInfor.setWindowTitle(QCoreApplication.translate("d_GeneralInfor", u"SP-editor", None))
        self.pb_OK.setText(QCoreApplication.translate("d_GeneralInfor", u"OK", None))
        self.pb_Cancel.setText(QCoreApplication.translate("d_GeneralInfor", u"Cancel", None))
        self.groupBox.setTitle(QCoreApplication.translate("d_GeneralInfor", u"General", None))
        self.label.setText(QCoreApplication.translate("d_GeneralInfor", u"Design code", None))
        self.cb_DesignCode.setItemText(0, QCoreApplication.translate("d_GeneralInfor", u"ACI 318-19", None))
        self.cb_DesignCode.setItemText(1, QCoreApplication.translate("d_GeneralInfor", u"ACI 318-14", None))
        self.cb_DesignCode.setItemText(2, QCoreApplication.translate("d_GeneralInfor", u"ACI 318-11", None))

        self.label_2.setText(QCoreApplication.translate("d_GeneralInfor", u"Unit system", None))
        self.cb_UnitSystem.setItemText(0, QCoreApplication.translate("d_GeneralInfor", u"English", None))
        self.cb_UnitSystem.setItemText(1, QCoreApplication.translate("d_GeneralInfor", u"Metric", None))

        self.label_3.setText(QCoreApplication.translate("d_GeneralInfor", u"Bar set", None))
        self.cb_BarSet.setItemText(0, QCoreApplication.translate("d_GeneralInfor", u"ASTM A615", None))
        self.cb_BarSet.setItemText(1, QCoreApplication.translate("d_GeneralInfor", u"ASTM A615M", None))
        self.cb_BarSet.setItemText(2, QCoreApplication.translate("d_GeneralInfor", u"prEN 10080", None))

        self.label_4.setText(QCoreApplication.translate("d_GeneralInfor", u"Confinement", None))
        self.cb_Confinement.setItemText(0, QCoreApplication.translate("d_GeneralInfor", u"Tied", None))
        self.cb_Confinement.setItemText(1, QCoreApplication.translate("d_GeneralInfor", u"Spiral", None))

        self.label_5.setText(QCoreApplication.translate("d_GeneralInfor", u"Section capacity", None))
        self.cb_SectionCapacity.setItemText(0, QCoreApplication.translate("d_GeneralInfor", u"Critical capacity", None))
        self.cb_SectionCapacity.setItemText(1, QCoreApplication.translate("d_GeneralInfor", u"Moment capacity", None))

    # retranslateUi

