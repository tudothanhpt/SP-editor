# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'combos_selected_dialog.ui'
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
    QListView, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_combosSelection_dialog(object):
    def setupUi(self, combosSelection_dialog):
        if not combosSelection_dialog.objectName():
            combosSelection_dialog.setObjectName(u"combosSelection_dialog")
        combosSelection_dialog.resize(621, 524)
        font = QFont()
        font.setPointSize(12)
        combosSelection_dialog.setFont(font)
        self.gridLayout = QGridLayout(combosSelection_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(combosSelection_dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pb_ok = QPushButton(self.frame)
        self.pb_ok.setObjectName(u"pb_ok")

        self.gridLayout_2.addWidget(self.pb_ok, 1, 1, 1, 1)

        self.pb_cancel = QPushButton(self.frame)
        self.pb_cancel.setObjectName(u"pb_cancel")

        self.gridLayout_2.addWidget(self.pb_cancel, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
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

        self.lview_combos = QListView(self.frame_2)
        self.lview_combos.setObjectName(u"lview_combos")
        self.lview_combos.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.lview_combos.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.verticalLayout.addWidget(self.lview_combos)


        self.horizontalLayout.addWidget(self.frame_2)

        self.frame_4 = QFrame(self.groupBox)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pb_select = QPushButton(self.frame_4)
        self.pb_select.setObjectName(u"pb_select")
        icon = QIcon(QIcon.fromTheme(u"go-next"))
        self.pb_select.setIcon(icon)
        self.pb_select.setIconSize(QSize(24, 24))

        self.verticalLayout_3.addWidget(self.pb_select)

        self.pb_deselect = QPushButton(self.frame_4)
        self.pb_deselect.setObjectName(u"pb_deselect")
        icon1 = QIcon(QIcon.fromTheme(u"go-previous"))
        self.pb_deselect.setIcon(icon1)
        self.pb_deselect.setIconSize(QSize(24, 24))

        self.verticalLayout_3.addWidget(self.pb_deselect)


        self.horizontalLayout.addWidget(self.frame_4)

        self.frame_3 = QFrame(self.groupBox)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.lview_selectedCombos = QListView(self.frame_3)
        self.lview_selectedCombos.setObjectName(u"lview_selectedCombos")

        self.verticalLayout_2.addWidget(self.lview_selectedCombos)


        self.horizontalLayout.addWidget(self.frame_3)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 3)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lview_combos, self.pb_deselect)
        QWidget.setTabOrder(self.pb_deselect, self.pb_select)
        QWidget.setTabOrder(self.pb_select, self.lview_selectedCombos)
        QWidget.setTabOrder(self.lview_selectedCombos, self.pb_ok)
        QWidget.setTabOrder(self.pb_ok, self.pb_cancel)

        self.retranslateUi(combosSelection_dialog)

        QMetaObject.connectSlotsByName(combosSelection_dialog)
    # setupUi

    def retranslateUi(self, combosSelection_dialog):
        combosSelection_dialog.setWindowTitle(QCoreApplication.translate("combosSelection_dialog", u"Design Load Combinations Selection", None))
        self.pb_ok.setText(QCoreApplication.translate("combosSelection_dialog", u"OK", None))
        self.pb_cancel.setText(QCoreApplication.translate("combosSelection_dialog", u"Cancel", None))
        self.groupBox.setTitle(QCoreApplication.translate("combosSelection_dialog", u"Choose Combinations", None))
        self.label.setText(QCoreApplication.translate("combosSelection_dialog", u"List of Combinations", None))
        self.pb_select.setText("")
        self.pb_deselect.setText("")
        self.label_2.setText(QCoreApplication.translate("combosSelection_dialog", u"Design Combinattion", None))
    # retranslateUi

