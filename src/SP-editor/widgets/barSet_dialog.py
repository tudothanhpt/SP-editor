# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'barSet_dialog.ui'
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
    QAbstractItemView,
    QApplication,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHeaderView,
    QLabel,
    QSizePolicy,
    QTableView,
    QWidget,
)


class Ui_d_BarSet(object):
    def setupUi(self, d_BarSet):
        if not d_BarSet.objectName():
            d_BarSet.setObjectName("d_BarSet")
        d_BarSet.resize(570, 550)
        font = QFont()
        font.setPointSize(12)
        d_BarSet.setFont(font)
        self.gridLayout = QGridLayout(d_BarSet)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QFrame(d_BarSet)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.cb_BarSetList = QComboBox(self.groupBox)
        self.cb_BarSetList.setObjectName("cb_BarSetList")

        self.gridLayout_3.addWidget(self.cb_BarSetList, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName("label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.tbview_BarSet = QTableView(self.groupBox)
        self.tbview_BarSet.setObjectName("tbview_BarSet")
        self.tbview_BarSet.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbview_BarSet.setSortingEnabled(True)
        self.tbview_BarSet.horizontalHeader().setVisible(True)
        self.tbview_BarSet.verticalHeader().setVisible(False)

        self.gridLayout_3.addWidget(self.tbview_BarSet, 1, 0, 1, 3)

        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(d_BarSet)

        QMetaObject.connectSlotsByName(d_BarSet)

    # setupUi

    def retranslateUi(self, d_BarSet):
        d_BarSet.setWindowTitle(QCoreApplication.translate("d_BarSet", "Bar Set", None))
        self.groupBox.setTitle(
            QCoreApplication.translate("d_BarSet", "Reinforcement", None)
        )
        self.label.setText(QCoreApplication.translate("d_BarSet", "Bar set", None))

    # retranslateUi
