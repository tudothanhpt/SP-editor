# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'importEtabs_dialog.ui'
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
    QApplication,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)
import icons_rc


class Ui_d_ImportEtabs(object):
    def setupUi(self, d_ImportEtabs):
        if not d_ImportEtabs.objectName():
            d_ImportEtabs.setObjectName("d_ImportEtabs")
        d_ImportEtabs.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(d_ImportEtabs.sizePolicy().hasHeightForWidth())
        d_ImportEtabs.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        d_ImportEtabs.setFont(font)
        icon = QIcon()
        icon.addFile(":/Btn/etabs logo.png", QSize(), QIcon.Normal, QIcon.Off)
        d_ImportEtabs.setWindowIcon(icon)
        self.gridLayout = QGridLayout(d_ImportEtabs)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_Select = QPushButton(d_ImportEtabs)
        self.pb_Select.setObjectName("pb_Select")

        self.gridLayout.addWidget(self.pb_Select, 1, 1, 1, 1)

        self.pb_OpenModel = QPushButton(d_ImportEtabs)
        self.pb_OpenModel.setObjectName("pb_OpenModel")

        self.gridLayout.addWidget(self.pb_OpenModel, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.groupBox = QGroupBox(d_ImportEtabs)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName("label")
        font1 = QFont()
        font1.setPointSize(18)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setTextFormat(Qt.TextFormat.PlainText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.lb_ActiveModel = QLabel(self.groupBox)
        self.lb_ActiveModel.setObjectName("lb_ActiveModel")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.lb_ActiveModel.sizePolicy().hasHeightForWidth()
        )
        self.lb_ActiveModel.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.lb_ActiveModel)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)

        self.retranslateUi(d_ImportEtabs)

        QMetaObject.connectSlotsByName(d_ImportEtabs)

    # setupUi

    def retranslateUi(self, d_ImportEtabs):
        d_ImportEtabs.setWindowTitle(
            QCoreApplication.translate("d_ImportEtabs", "Import Etabs", None)
        )
        self.pb_Select.setText(
            QCoreApplication.translate("d_ImportEtabs", "Select", None)
        )
        self.pb_OpenModel.setText(
            QCoreApplication.translate("d_ImportEtabs", "Open Model", None)
        )
        self.groupBox.setTitle("")
        self.label.setText(
            QCoreApplication.translate("d_ImportEtabs", "ACTIVE MODEL", None)
        )
        self.lb_ActiveModel.setText("")
        self.label_3.setText(
            QCoreApplication.translate(
                "d_ImportEtabs", "Select active model or Open another model!", None
            )
        )

    # retranslateUi
