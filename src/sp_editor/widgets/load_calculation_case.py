# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'load_calculation_case.ui'
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
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListView, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_calculationCase_dialog(object):
    def setupUi(self, calculationCase_dialog):
        if not calculationCase_dialog.objectName():
            calculationCase_dialog.setObjectName(u"calculationCase_dialog")
        calculationCase_dialog.resize(1080, 773)
        font = QFont()
        font.setPointSize(12)
        calculationCase_dialog.setFont(font)
        self.gridLayout = QGridLayout(calculationCase_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.frame_8 = QFrame(calculationCase_dialog)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.frame = QFrame(self.frame_8)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(6)
        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_4 = QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.cb_tier = QComboBox(self.groupBox)
        self.cb_tier.setObjectName(u"cb_tier")

        self.gridLayout_4.addWidget(self.cb_tier, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_5 = QGroupBox(self.frame_4)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_11 = QGridLayout(self.groupBox_5)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.cb_sectionDesignerShape = QComboBox(self.groupBox_5)
        self.cb_sectionDesignerShape.setObjectName(u"cb_sectionDesignerShape")

        self.gridLayout_11.addWidget(self.cb_sectionDesignerShape, 0, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_5)

        self.groupBox_4 = QGroupBox(self.frame_4)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_9 = QGridLayout(self.groupBox_4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.cb_pierdata = QComboBox(self.groupBox_4)
        self.cb_pierdata.setObjectName(u"cb_pierdata")

        self.gridLayout_9.addWidget(self.cb_pierdata, 0, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(self.frame_4)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_6 = QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.lview_level = QListView(self.groupBox_3)
        self.lview_level.setObjectName(u"lview_level")

        self.gridLayout_6.addWidget(self.lview_level, 0, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.verticalLayout_4.setStretch(2, 95)

        self.gridLayout_2.addWidget(self.frame_4, 2, 0, 1, 1)


        self.horizontalLayout.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox_2 = QGroupBox(self.frame_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_5 = QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.le_folderName = QLineEdit(self.groupBox_2)
        self.le_folderName.setObjectName(u"le_folderName")

        self.gridLayout_5.addWidget(self.le_folderName, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_3)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_6 = QGroupBox(self.frame_5)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.formLayout = QFormLayout(self.groupBox_6)
        self.formLayout.setObjectName(u"formLayout")
        self.cb_concrete = QComboBox(self.groupBox_6)
        self.cb_concrete.setObjectName(u"cb_concrete")
        self.cb_concrete.setMinimumSize(QSize(0, 28))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cb_concrete)

        self.cb_steel = QComboBox(self.groupBox_6)
        self.cb_steel.setObjectName(u"cb_steel")
        self.cb_steel.setMinimumSize(QSize(0, 28))

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cb_steel)

        self.label_23 = QLabel(self.groupBox_6)
        self.label_23.setObjectName(u"label_23")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_23)

        self.lb_Ec = QLabel(self.groupBox_6)
        self.lb_Ec.setObjectName(u"lb_Ec")
        self.lb_Ec.setMinimumSize(QSize(0, 28))
        self.lb_Ec.setFrameShape(QFrame.Shape.StyledPanel)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.lb_Ec)

        self.label_25 = QLabel(self.groupBox_6)
        self.label_25.setObjectName(u"label_25")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_25)

        self.lb_Es = QLabel(self.groupBox_6)
        self.lb_Es.setObjectName(u"lb_Es")
        self.lb_Es.setMinimumSize(QSize(0, 28))
        self.lb_Es.setFrameShape(QFrame.Shape.StyledPanel)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.lb_Es)

        self.lb_fc = QLabel(self.groupBox_6)
        self.lb_fc.setObjectName(u"lb_fc")
        self.lb_fc.setMinimumSize(QSize(0, 28))
        self.lb_fc.setFrameShape(QFrame.Shape.StyledPanel)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lb_fc)

        self.lb_fy = QLabel(self.groupBox_6)
        self.lb_fy.setObjectName(u"lb_fy")
        self.lb_fy.setMinimumSize(QSize(0, 28))
        self.lb_fy.setFrameShape(QFrame.Shape.StyledPanel)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.lb_fy)

        self.label_16 = QLabel(self.groupBox_6)
        self.label_16.setObjectName(u"label_16")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_16)

        self.label_17 = QLabel(self.groupBox_6)
        self.label_17.setObjectName(u"label_17")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_17)

        self.label_5 = QLabel(self.groupBox_6)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.label_2 = QLabel(self.groupBox_6)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)


        self.verticalLayout_5.addWidget(self.groupBox_6)

        self.groupBox_7 = QGroupBox(self.frame_5)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.formLayout_2 = QFormLayout(self.groupBox_7)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_22 = QLabel(self.groupBox_7)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_22)

        self.cb_barType = QComboBox(self.groupBox_7)
        self.cb_barType.addItem("")
        self.cb_barType.addItem("")
        self.cb_barType.setObjectName(u"cb_barType")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.cb_barType)

        self.label_19 = QLabel(self.groupBox_7)
        self.label_19.setObjectName(u"label_19")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_19)

        self.le_spacing = QLineEdit(self.groupBox_7)
        self.le_spacing.setObjectName(u"le_spacing")
        self.le_spacing.setMinimumSize(QSize(0, 28))
        self.le_spacing.setClearButtonEnabled(False)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.le_spacing)

        self.label_20 = QLabel(self.groupBox_7)
        self.label_20.setObjectName(u"label_20")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_20)

        self.lb_quantities = QLabel(self.groupBox_7)
        self.lb_quantities.setObjectName(u"lb_quantities")
        self.lb_quantities.setMinimumSize(QSize(0, 28))
        self.lb_quantities.setFrameShape(QFrame.Shape.StyledPanel)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.lb_quantities)

        self.stackW_bar = QStackedWidget(self.groupBox_7)
        self.stackW_bar.setObjectName(u"stackW_bar")
        self.stackW_bar.setEnabled(True)
        self.stackW_bar.setFrameShape(QFrame.Shape.NoFrame)
        self.stackW_bar.setLineWidth(0)
        self.barSize = QWidget()
        self.barSize.setObjectName(u"barSize")
        self.gridLayout_8 = QGridLayout(self.barSize)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 9, 0, 9)
        self.label_29 = QLabel(self.barSize)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_8.addWidget(self.label_29, 0, 0, 1, 1)

        self.cb_barSize = QComboBox(self.barSize)
        self.cb_barSize.setObjectName(u"cb_barSize")
        self.cb_barSize.setFrame(True)

        self.gridLayout_8.addWidget(self.cb_barSize, 0, 1, 1, 1)

        self.gridLayout_8.setColumnStretch(0, 40)
        self.gridLayout_8.setColumnStretch(1, 88)
        self.stackW_bar.addWidget(self.barSize)
        self.barArea = QWidget()
        self.barArea.setObjectName(u"barArea")
        self.gridLayout_10 = QGridLayout(self.barArea)
        self.gridLayout_10.setSpacing(6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 9, 0, 9)
        self.label_18 = QLabel(self.barArea)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_10.addWidget(self.label_18, 0, 0, 1, 1)

        self.le_barArea = QLineEdit(self.barArea)
        self.le_barArea.setObjectName(u"le_barArea")
        self.le_barArea.setMinimumSize(QSize(0, 28))

        self.gridLayout_10.addWidget(self.le_barArea, 0, 1, 1, 1)

        self.gridLayout_10.setColumnStretch(0, 40)
        self.gridLayout_10.setColumnStretch(1, 88)
        self.stackW_bar.addWidget(self.barArea)

        self.formLayout_2.setWidget(2, QFormLayout.SpanningRole, self.stackW_bar)


        self.verticalLayout_5.addWidget(self.groupBox_7)

        self.groupBox_9 = QGroupBox(self.frame_5)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.formLayout_3 = QFormLayout(self.groupBox_9)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_24 = QLabel(self.groupBox_9)
        self.label_24.setObjectName(u"label_24")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_24)

        self.label_26 = QLabel(self.groupBox_9)
        self.label_26.setObjectName(u"label_26")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_26)

        self.le_cover = QLineEdit(self.groupBox_9)
        self.le_cover.setObjectName(u"le_cover")
        self.le_cover.setMinimumSize(QSize(0, 28))

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.le_cover)

        self.label_3 = QLabel(self.groupBox_9)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.label_3)


        self.verticalLayout_5.addWidget(self.groupBox_9)

        self.pb_makeSection = QPushButton(self.frame_5)
        self.pb_makeSection.setObjectName(u"pb_makeSection")

        self.verticalLayout_5.addWidget(self.pb_makeSection)

        self.verticalLayout_5.setStretch(0, 3)
        self.verticalLayout_5.setStretch(1, 3)
        self.verticalLayout_5.setStretch(2, 2)

        self.gridLayout_3.addWidget(self.frame_5, 1, 0, 1, 1)

        self.gridLayout_3.setRowStretch(0, 1)
        self.gridLayout_3.setRowStretch(1, 9)

        self.horizontalLayout.addWidget(self.frame_3)

        self.frame_7 = QFrame(self.frame)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_7)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.f_3dview = QFrame(self.frame_7)
        self.f_3dview.setObjectName(u"f_3dview")
        self.f_3dview.setFrameShape(QFrame.Shape.StyledPanel)
        self.f_3dview.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_3.addWidget(self.f_3dview)

        self.groupBox_8 = QGroupBox(self.frame_7)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_7 = QGridLayout(self.groupBox_8)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_13 = QLabel(self.groupBox_8)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFrameShape(QFrame.Shape.NoFrame)

        self.gridLayout_7.addWidget(self.label_13, 3, 0, 1, 1)

        self.lb_unitAs = QLabel(self.groupBox_8)
        self.lb_unitAs.setObjectName(u"lb_unitAs")
        self.lb_unitAs.setFrameShape(QFrame.Shape.NoFrame)
        self.lb_unitAs.setMargin(0)
        self.lb_unitAs.setIndent(3)

        self.gridLayout_7.addWidget(self.lb_unitAs, 1, 2, 1, 1)

        self.label = QLabel(self.groupBox_8)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.Shape.NoFrame)

        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 1)

        self.lb_unitArea = QLabel(self.groupBox_8)
        self.lb_unitArea.setObjectName(u"lb_unitArea")
        self.lb_unitArea.setFrameShape(QFrame.Shape.NoFrame)
        self.lb_unitArea.setMargin(0)
        self.lb_unitArea.setIndent(3)

        self.gridLayout_7.addWidget(self.lb_unitArea, 0, 2, 1, 1)

        self.lb_maxCapacity = QLabel(self.groupBox_8)
        self.lb_maxCapacity.setObjectName(u"lb_maxCapacity")
        self.lb_maxCapacity.setFrameShape(QFrame.Shape.StyledPanel)
        self.lb_maxCapacity.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.lb_maxCapacity, 3, 1, 1, 1)

        self.label_15 = QLabel(self.groupBox_8)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFrameShape(QFrame.Shape.NoFrame)
        self.label_15.setMargin(0)
        self.label_15.setIndent(3)

        self.gridLayout_7.addWidget(self.label_15, 3, 2, 1, 1)

        self.lb_Rho = QLabel(self.groupBox_8)
        self.lb_Rho.setObjectName(u"lb_Rho")
        self.lb_Rho.setFrameShape(QFrame.Shape.StyledPanel)
        self.lb_Rho.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.lb_Rho, 2, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFrameShape(QFrame.Shape.NoFrame)

        self.gridLayout_7.addWidget(self.label_4, 1, 0, 1, 1)

        self.lb_grossArea = QLabel(self.groupBox_8)
        self.lb_grossArea.setObjectName(u"lb_grossArea")
        self.lb_grossArea.setFrameShape(QFrame.Shape.StyledPanel)
        self.lb_grossArea.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.lb_grossArea, 0, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_8)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFrameShape(QFrame.Shape.NoFrame)

        self.gridLayout_7.addWidget(self.label_7, 2, 0, 1, 1)

        self.lb_totalAs = QLabel(self.groupBox_8)
        self.lb_totalAs.setObjectName(u"lb_totalAs")
        self.lb_totalAs.setFrameShape(QFrame.Shape.StyledPanel)
        self.lb_totalAs.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.lb_totalAs, 1, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_8)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFrameShape(QFrame.Shape.NoFrame)
        self.label_9.setMargin(0)
        self.label_9.setIndent(3)

        self.gridLayout_7.addWidget(self.label_9, 2, 2, 1, 1)

        self.gridLayout_7.setColumnStretch(0, 5)
        self.gridLayout_7.setColumnStretch(1, 4)
        self.gridLayout_7.setColumnStretch(2, 1)
        self.gridLayout_7.setRowMinimumHeight(0, 5)
        self.gridLayout_7.setRowMinimumHeight(1, 3)
        self.gridLayout_7.setRowMinimumHeight(2, 3)

        self.verticalLayout_3.addWidget(self.groupBox_8)

        self.verticalLayout_3.setStretch(0, 6)
        self.verticalLayout_3.setStretch(1, 3)

        self.horizontalLayout.addWidget(self.frame_7)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 3)

        self.verticalLayout_2.addWidget(self.frame)

        self.frame_6 = QFrame(self.frame_8)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.label_27 = QLabel(self.frame_6)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout_2.addWidget(self.label_27)

        self.lb_globalUnit = QLabel(self.frame_6)
        self.lb_globalUnit.setObjectName(u"lb_globalUnit")

        self.horizontalLayout_2.addWidget(self.lb_globalUnit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.frame_6)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame_6)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout_2.addWidget(self.frame_6)


        self.gridLayout.addWidget(self.frame_8, 1, 0, 1, 1)


        self.retranslateUi(calculationCase_dialog)
        self.cb_barType.currentIndexChanged.connect(self.stackW_bar.setCurrentIndex)

        self.stackW_bar.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(calculationCase_dialog)
    # setupUi

    def retranslateUi(self, calculationCase_dialog):
        calculationCase_dialog.setWindowTitle(QCoreApplication.translate("calculationCase_dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("calculationCase_dialog", u"Tier", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("calculationCase_dialog", u"Section Designer Shape", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("calculationCase_dialog", u"Pier data", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("calculationCase_dialog", u"Level Information", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("calculationCase_dialog", u"Folder name", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("calculationCase_dialog", u"Material", None))
        self.label_23.setText(QCoreApplication.translate("calculationCase_dialog", u"Ec", None))
        self.lb_Ec.setText("")
        self.label_25.setText(QCoreApplication.translate("calculationCase_dialog", u"Es", None))
        self.lb_Es.setText("")
        self.lb_fc.setText("")
        self.lb_fy.setText("")
        self.label_16.setText(QCoreApplication.translate("calculationCase_dialog", u"Strength, f'c", None))
        self.label_17.setText(QCoreApplication.translate("calculationCase_dialog", u"Strength, fy", None))
        self.label_5.setText(QCoreApplication.translate("calculationCase_dialog", u"Steel", None))
        self.label_2.setText(QCoreApplication.translate("calculationCase_dialog", u"Concrete", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("calculationCase_dialog", u"Rebar", None))
        self.label_22.setText(QCoreApplication.translate("calculationCase_dialog", u"Bars by", None))
        self.cb_barType.setItemText(0, QCoreApplication.translate("calculationCase_dialog", u"Size", None))
        self.cb_barType.setItemText(1, QCoreApplication.translate("calculationCase_dialog", u"Area", None))

        self.label_19.setText(QCoreApplication.translate("calculationCase_dialog", u"Spacing", None))
        self.label_20.setText(QCoreApplication.translate("calculationCase_dialog", u"Quantities", None))
        self.lb_quantities.setText("")
        self.label_29.setText(QCoreApplication.translate("calculationCase_dialog", u"Bar size", None))
        self.label_18.setText(QCoreApplication.translate("calculationCase_dialog", u"Bar area", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("calculationCase_dialog", u"Cover (Longitudinal bars)", None))
        self.label_24.setText(QCoreApplication.translate("calculationCase_dialog", u"Type", None))
        self.label_26.setText(QCoreApplication.translate("calculationCase_dialog", u"Cover", None))
        self.label_3.setText(QCoreApplication.translate("calculationCase_dialog", u"Clear", None))
        self.pb_makeSection.setText(QCoreApplication.translate("calculationCase_dialog", u"Make Section", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("calculationCase_dialog", u"Properties", None))
        self.label_13.setText(QCoreApplication.translate("calculationCase_dialog", u"Max capacity ratio", None))
        self.lb_unitAs.setText("")
        self.label.setText(QCoreApplication.translate("calculationCase_dialog", u"Gross area", None))
        self.lb_unitArea.setText("")
        self.lb_maxCapacity.setText(QCoreApplication.translate("calculationCase_dialog", u"0.00", None))
        self.label_15.setText("")
        self.lb_Rho.setText(QCoreApplication.translate("calculationCase_dialog", u"0.00", None))
        self.label_4.setText(QCoreApplication.translate("calculationCase_dialog", u"Total As", None))
        self.lb_grossArea.setText(QCoreApplication.translate("calculationCase_dialog", u"0.00", None))
        self.label_7.setText(QCoreApplication.translate("calculationCase_dialog", u"Rho", None))
        self.lb_totalAs.setText(QCoreApplication.translate("calculationCase_dialog", u"0.00", None))
        self.label_9.setText(QCoreApplication.translate("calculationCase_dialog", u"%", None))
        self.label_27.setText(QCoreApplication.translate("calculationCase_dialog", u"Unit:", None))
        self.lb_globalUnit.setText("")
        self.pushButton.setText(QCoreApplication.translate("calculationCase_dialog", u"OK", None))
        self.pushButton_2.setText(QCoreApplication.translate("calculationCase_dialog", u"Cancel", None))
    # retranslateUi

