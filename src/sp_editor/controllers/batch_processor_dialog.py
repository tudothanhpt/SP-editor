import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw

from sp_editor.core.spcol_batch_processor import BatchProcessorThread
from sp_editor.core.read_batch_processor_outputs import make_df_from_outputs, check_output_paths_exist, \
    get_o_xlsx_paths_from_cti_paths, max_dcr_from_outputs
from sp_editor.widgets.batch_processor_dialog_ui import Ui_BatchProcessorDialog
from sqlalchemy.engine.base import Engine
from sqlmodel import Session, create_engine
from sp_editor.crud.cr_cti_summary import read_summaryCTI_DB
from sp_editor.crud.cr_load_case import update_dcr_by_spcolumnfile
from sp_editor.database.models import CTISummary, BatchProcessingOutput
from sp_editor.utils import get_attribute_names

REP = 31
STARTTEXT = "-" * REP + "START" + "-" * REP
ENDTEXT = "-" * REP + "END" + "-" * REP

# Get the class attributes
CTISummary_attribute_names = get_attribute_names(CTISummary)

# assign class attributes to tuple variables)
TB_BATCHPROCESSINGOUTPUT = BatchProcessingOutput.__name__.lower()
(id2, tier, pier, material_ec, material_fc, material_fy, material_es,
 sd_name, coordinates, total_bars, rebar_coordinates, total_combos,
 filtered_forces, case_path, path_after_creation) = CTISummary_attribute_names


class BatchProcessorDialog(qtw.QDialog, Ui_BatchProcessorDialog):
    read_results_create = qtc.Signal()

    def __init__(self, engine: Engine, parent: qtw.QWidget = None):
        super().__init__(parent)
        self.setupUi(self)

        self.engine = engine
        self.input_files = read_summaryCTI_DB(self.engine)[path_after_creation].tolist()
        self.output_xlsx_paths = None
        self.pb_showButton.setEnabled(True)
        self.pb_startButton.clicked.connect(self.start_thread)
        self.pb_showButton.clicked.connect(self.read_result)

    def start_thread(self):

        self.pb_startButton.setEnabled(False)  # Disable the start button when running
        self.pb_showButton.setEnabled(False)  # Disable the read button when running
        self.t_resultTextEdit.clear()  # Clear previous output

        self.t_resultTextEdit.setText(f"<b>{STARTTEXT}<b>")
        ui_options = self.get_selected_output_options()
        self.thread = BatchProcessorThread(self.engine, self.input_files, options=ui_options)
        self.thread.error.connect(self.show_error)
        self.thread.success.connect(self.show_success)
        self.thread.output.connect(self.update_output)
        self.thread.success.connect(self.enable_start_button)  # Re-enable the start button when the thread finishes
        self.thread.start()

    def get_selected_output_options(self):
        options = []
        if self.cb_excel.isChecked():
            options.append("/rxls")
        if self.cb_word.isChecked():
            options.append("/rdoc")
        if self.cb_pdf.isChecked():
            options.append("/rpdf")
        if self.cb_text.isChecked():
            options.append("/txt")
        if self.cb_csv.isChecked():
            options.append("/rcsv")
        if self.cb_dxf.isChecked():
            options.append("/dxf")
        return options
    
    def show_error(self, message):
        qtw.QMessageBox.critical(self, "Error", message)
        self.pb_startButton.setEnabled(True)  # Re-enable the start button in case of error

    def show_success(self, message):
        self.t_resultTextEdit.append(message)
        self.t_resultTextEdit.append(f"<b>{ENDTEXT}<b>")
        self.pb_startButton.setEnabled(True)  # Re-enable the start button
        self.pb_showButton.setEnabled(True)

    def update_output(self, output):
        self.t_resultTextEdit.append(output)

    def enable_start_button(self):
        self.pb_startButton.setEnabled(True)  # Ensure the start button is enabled

    def read_result(self):
        self.output_xlsx_paths = get_o_xlsx_paths_from_cti_paths(self.input_files)
        check_output_paths_exist(self.output_xlsx_paths)

        try:
            df = make_df_from_outputs(self.output_xlsx_paths)
            df.to_sql(name=TB_BATCHPROCESSINGOUTPUT, con=self.engine, if_exists='replace', index=False)
            df_max_dcr_per_spColumn = max_dcr_from_outputs(df)

            print(df_max_dcr_per_spColumn)

            for index, row in df_max_dcr_per_spColumn.iterrows():
                id = row['No.']
                spColumnFile = row['spColumnFile']
                dcr = row['DCR']
                update_dcr_by_spcolumnfile(self.engine, spColumnFile, dcr, id)
                self.read_results_create.emit()

            self.t_resultTextEdit.setText("DONE")
            self.close()
        except Exception as e:
            print(f"Error occurred: {e}")


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    engine_temppath = r"C:\Users\AnhBui\Desktop\123.spe"
    engine = create_engine(f"sqlite:///{engine_temppath}")
    window = BatchProcessorDialog(engine)
    window.show()
    sys.exit(app.exec())
