from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg


class Ui_BatchProcessorDialog(object):
    def setupUi(self, BatchProcessorDialog):
        BatchProcessorDialog.setObjectName("BatchProcessorDialog")
        BatchProcessorDialog.resize(500, 400)
        BatchProcessorDialog.setMinimumSize(qtc.QSize(500, 400))
        BatchProcessorDialog.setMaximumSize(qtc.QSize(500, 400))

        self.verticalLayout = qtw.QVBoxLayout(BatchProcessorDialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.frame = qtw.QFrame(BatchProcessorDialog)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(qtw.QFrame.Shape.Box)
        self.frame.setFrameShadow(qtw.QFrame.Shadow.Plain)
        self.frame.setLineWidth(1)
        self.frame_layout = qtw.QVBoxLayout(self.frame)

        self.t_resultTextEdit = qtw.QTextEdit(self.frame)
        self.t_resultTextEdit.setObjectName("t_resultTextEdit")
        self.t_resultTextEdit.setReadOnly(True)
        self.t_resultTextEdit.setFont(qtg.QFont("Segoe UI", 11))
        self.frame_layout.addWidget(self.t_resultTextEdit)

        self.verticalLayout.addWidget(self.frame)

        self.verticalSpacer = qtw.QSpacerItem(20, 20, qtw.QSizePolicy.Policy.Minimum, qtw.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = qtw.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pb_startButton = qtw.QPushButton(BatchProcessorDialog)
        self.pb_startButton.setObjectName("pb_startButton")
        self.pb_startButton.setFont(qtg.QFont("Segoe UI", 12))
        self.horizontalLayout.addWidget(self.pb_startButton)

        self.pb_showButton = qtw.QPushButton(BatchProcessorDialog)
        self.pb_showButton.setObjectName("pb_showButton")
        self.pb_showButton.setFont(qtg.QFont("Segoe UI", 12))
        self.horizontalLayout.addWidget(self.pb_showButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(BatchProcessorDialog)
        qtc.QMetaObject.connectSlotsByName(BatchProcessorDialog)

    def retranslateUi(self, BatchProcessorDialog):
        _translate = qtc.QCoreApplication.translate
        BatchProcessorDialog.setWindowTitle(_translate("BatchProcessorDialog", "Batch Processor"))
        self.pb_startButton.setText(_translate("BatchProcessorDialog", "Batch Proccesing"))
        self.pb_showButton.setText(_translate("BatchProcessorDialog", "Show Result"))
