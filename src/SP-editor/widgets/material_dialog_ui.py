# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'material_dialog.ui'
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
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTabWidget, QTableView,
    QWidget)

class Ui_d_material(object):
    def setupUi(self, d_material):
        if not d_material.objectName():
            d_material.setObjectName(u"d_material")
        d_material.resize(538, 480)
        font = QFont()
        font.setPointSize(12)
        d_material.setFont(font)
        self.gridLayout = QGridLayout(d_material)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pb_load = QPushButton(d_material)
        self.pb_load.setObjectName(u"pb_load")

        self.gridLayout.addWidget(self.pb_load, 3, 0, 1, 1)

        self.frame_2 = QFrame(d_material)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.gridLayout_3 = QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pb_delete = QPushButton(self.frame_2)
        self.pb_delete.setObjectName(u"pb_delete")

        self.gridLayout_3.addWidget(self.pb_delete, 1, 0, 1, 1)

        self.lb_3 = QLabel(self.frame_2)
        self.lb_3.setObjectName(u"lb_3")

        self.gridLayout_3.addWidget(self.lb_3, 0, 4, 1, 1)

        self.lb_name = QLabel(self.frame_2)
        self.lb_name.setObjectName(u"lb_name")

        self.gridLayout_3.addWidget(self.lb_name, 0, 2, 1, 1)

        self.le_4 = QLineEdit(self.frame_2)
        self.le_4.setObjectName(u"le_4")

        self.gridLayout_3.addWidget(self.le_4, 1, 5, 1, 1)

        self.le_3 = QLineEdit(self.frame_2)
        self.le_3.setObjectName(u"le_3")

        self.gridLayout_3.addWidget(self.le_3, 1, 4, 1, 1)

        self.le_2 = QLineEdit(self.frame_2)
        self.le_2.setObjectName(u"le_2")

        self.gridLayout_3.addWidget(self.le_2, 1, 3, 1, 1)

        self.pb_add = QPushButton(self.frame_2)
        self.pb_add.setObjectName(u"pb_add")

        self.gridLayout_3.addWidget(self.pb_add, 0, 0, 1, 1)

        self.checkBox = QCheckBox(self.frame_2)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_3.addWidget(self.checkBox, 2, 0, 1, 1)

        self.le_name = QLineEdit(self.frame_2)
        self.le_name.setObjectName(u"le_name")

        self.gridLayout_3.addWidget(self.le_name, 1, 2, 1, 1)

        self.lb_4 = QLabel(self.frame_2)
        self.lb_4.setObjectName(u"lb_4")

        self.gridLayout_3.addWidget(self.lb_4, 0, 5, 1, 1)

        self.lb_2 = QLabel(self.frame_2)
        self.lb_2.setObjectName(u"lb_2")

        self.gridLayout_3.addWidget(self.lb_2, 0, 3, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 2)

        self.frame = QFrame(d_material)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tab_concrete = QWidget()
        self.tab_concrete.setObjectName(u"tab_concrete")
        self.gridLayout_4 = QGridLayout(self.tab_concrete)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tbview_concrete = QTableView(self.tab_concrete)
        self.tbview_concrete.setObjectName(u"tbview_concrete")

        self.gridLayout_4.addWidget(self.tbview_concrete, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_concrete, "")
        self.tab_steel = QWidget()
        self.tab_steel.setObjectName(u"tab_steel")
        self.gridLayout_5 = QGridLayout(self.tab_steel)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.tbview_steel = QTableView(self.tab_steel)
        self.tbview_steel.setObjectName(u"tbview_steel")

        self.gridLayout_5.addWidget(self.tbview_steel, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_steel, "")

        self.gridLayout_2.addWidget(self.tabWidget, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.frame, 2, 0, 1, 2)

        self.pb_apply = QPushButton(d_material)
        self.pb_apply.setObjectName(u"pb_apply")

        self.gridLayout.addWidget(self.pb_apply, 3, 1, 1, 1)

        QWidget.setTabOrder(self.pb_add, self.pb_delete)
        QWidget.setTabOrder(self.pb_delete, self.le_name)
        QWidget.setTabOrder(self.le_name, self.le_2)
        QWidget.setTabOrder(self.le_2, self.le_3)
        QWidget.setTabOrder(self.le_3, self.le_4)
        QWidget.setTabOrder(self.le_4, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.tbview_concrete)
        QWidget.setTabOrder(self.tbview_concrete, self.pb_load)
        QWidget.setTabOrder(self.pb_load, self.pb_apply)
        QWidget.setTabOrder(self.pb_apply, self.tbview_steel)

        self.retranslateUi(d_material)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(d_material)
    # setupUi

    def retranslateUi(self, d_material):
        d_material.setWindowTitle(QCoreApplication.translate("d_material", u"Material Properties", None))
        self.pb_load.setText(QCoreApplication.translate("d_material", u"Load Setting", None))
        self.pb_delete.setText(QCoreApplication.translate("d_material", u"Delete", None))
        self.lb_3.setText("")
        self.lb_name.setText(QCoreApplication.translate("d_material", u"Name", None))
        self.pb_add.setText(QCoreApplication.translate("d_material", u"Add", None))
        self.checkBox.setText(QCoreApplication.translate("d_material", u"Standard", None))
        self.lb_4.setText("")
        self.lb_2.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_concrete), QCoreApplication.translate("d_material", u"Concrete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_steel), QCoreApplication.translate("d_material", u"Steel", None))
        self.pb_apply.setText(QCoreApplication.translate("d_material", u"Apply", None))
    # retranslateUi

