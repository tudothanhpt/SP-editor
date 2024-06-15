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
        group_dialog.resize(710, 756)
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


        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 3)

        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.pb_OK = QPushButton(self.frame_5)
        self.pb_OK.setObjectName(u"pb_OK")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_OK.sizePolicy().hasHeightForWidth())
        self.pb_OK.setSizePolicy(sizePolicy)
        self.pb_OK.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.pb_OK)

        self.pb_cancel = QPushButton(self.frame_5)
        self.pb_cancel.setObjectName(u"pb_cancel")
        self.pb_cancel.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.pb_cancel)


        self.gridLayout_2.addWidget(self.frame_5, 2, 0, 1, 1)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.le_groupName = QLineEdit(self.frame_2)
        self.le_groupName.setObjectName(u"le_groupName")
        self.le_groupName.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_2.addWidget(self.le_groupName)

        self.pb_addGroup = QPushButton(self.frame_2)
        self.pb_addGroup.setObjectName(u"pb_addGroup")
        self.pb_addGroup.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.pb_addGroup)


        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 3)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(group_dialog)

        QMetaObject.connectSlotsByName(group_dialog)
    # setupUi

    def retranslateUi(self, group_dialog):
        group_dialog.setWindowTitle(QCoreApplication.translate("group_dialog", u"Level Groups", None))
        self.groupBox.setTitle(QCoreApplication.translate("group_dialog", u"Level Groups", None))
        self.label.setText(QCoreApplication.translate("group_dialog", u"Story Name", None))
        self.label_4.setText(QCoreApplication.translate("group_dialog", u"Pier Name", None))
        self.label_3.setText(QCoreApplication.translate("group_dialog", u"Groups Name", None))
        self.pb_OK.setText(QCoreApplication.translate("group_dialog", u"OK", None))
        self.pb_cancel.setText(QCoreApplication.translate("group_dialog", u"Cancel", None))
        self.label_2.setText(QCoreApplication.translate("group_dialog", u"Name: ", None))
        self.pb_addGroup.setText(QCoreApplication.translate("group_dialog", u"Add", None))
    # retranslateUi

