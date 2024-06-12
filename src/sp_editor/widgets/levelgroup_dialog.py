# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'levelgroup_dialog.ui'
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
    QLineEdit, QListView, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_group_dialog(object):
    def setupUi(self, group_dialog):
        if not group_dialog.objectName():
            group_dialog.setObjectName(u"group_dialog")
        group_dialog.resize(672, 679)
        font = QFont()
        font.setPointSize(12)
        group_dialog.setFont(font)
        self.gridLayout = QGridLayout(group_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(group_dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pb_addGroup = QPushButton(self.frame)
        self.pb_addGroup.setObjectName(u"pb_addGroup")

        self.gridLayout_2.addWidget(self.pb_addGroup, 0, 3, 1, 1)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_3 = QFrame(self.groupBox)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.lview_storyName = QListView(self.frame_3)
        self.lview_storyName.setObjectName(u"lview_storyName")
        self.lview_storyName.setFrameShape(QFrame.Shape.Box)
        self.lview_storyName.setFrameShadow(QFrame.Shadow.Sunken)
        self.lview_storyName.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.lview_storyName.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.verticalLayout_2.addWidget(self.lview_storyName)


        self.horizontalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.groupBox)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_4)

        self.lview_pierName = QListView(self.frame_4)
        self.lview_pierName.setObjectName(u"lview_pierName")

        self.verticalLayout_3.addWidget(self.lview_pierName)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setFrameShape(QFrame.Shape.NoFrame)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_3)

        self.lview_groupName = QListView(self.frame_4)
        self.lview_groupName.setObjectName(u"lview_groupName")
        self.lview_groupName.setFrameShape(QFrame.Shape.Box)
        self.lview_groupName.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.lview_groupName)


        self.horizontalLayout.addWidget(self.frame_4)


        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 4)

        self.le_groupName = QLineEdit(self.frame)
        self.le_groupName.setObjectName(u"le_groupName")

        self.gridLayout_2.addWidget(self.le_groupName, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(group_dialog)

        QMetaObject.connectSlotsByName(group_dialog)
    # setupUi

    def retranslateUi(self, group_dialog):
        group_dialog.setWindowTitle(QCoreApplication.translate("group_dialog", u"Level Groups", None))
        self.pb_addGroup.setText(QCoreApplication.translate("group_dialog", u"Add", None))
        self.groupBox.setTitle(QCoreApplication.translate("group_dialog", u"Level Groups", None))
        self.label.setText(QCoreApplication.translate("group_dialog", u"Story Name", None))
        self.label_4.setText(QCoreApplication.translate("group_dialog", u"Pier Name", None))
        self.label_3.setText(QCoreApplication.translate("group_dialog", u"Groups Name", None))
        self.label_2.setText(QCoreApplication.translate("group_dialog", u"Name: ", None))
    # retranslateUi

