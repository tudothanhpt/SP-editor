import subprocess
import os
from sp_editor.core.cti_data_merging import read_summaryCTI_DB
from sqlmodel import Session,create_engine
from sqlalchemy.engine.base import Engine
from sp_editor.utils import  get_engine_path
# Define the constant path to spColumn.CLI.exe
SPCOLUMN_PATH = r"C:\Program Files (x86)\StructurePoint\spColumn\spColumn.CLI.exe"



batch_file_path = r"C:\Users\abui\Desktop\Git\Repo\SP-editor\run_spColumn.bat"
def create_batch_file(input_files, batch_file_path, options=None):
    # Ensure options is a list
    if options is None:
        options = ["/rpdf", "/rcsv"]

    with open(batch_file_path, 'w') as batch_file:
        for input_file in input_files:
            # Determine the directory of the input file
            input_dir = os.path.dirname(input_file)

            batch_file.write(f'"{SPCOLUMN_PATH}" /i:"{input_file}" /o:"{input_dir}" ' + ' '.join(options)+ '\n' ) 

# Example usage



if __name__ == "__main__":
    engine_temppath = r"C:\Users\abui\Desktop\Git\Repo\SP-editor\12345.spe"
    engine: Engine = create_engine(f"sqlite:///{engine_temppath}")
    
    engine_path = get_engine_path(engine)
    batch_file_path = os.path.join(engine_path,"run_spColumn.bat")
    df_CTIsummary = read_summaryCTI_DB(engine)
    input_files=df_CTIsummary["PathAfterCreation"].unique().tolist()


    # Run the solver for each input file and generate the summary output
    create_batch_file(input_files,batch_file_path)