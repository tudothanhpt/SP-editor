import os
import read_excel
from core import spcolumn_cti


def main_multi(excelPath):
    # Read the requirements.txt file
    # requirements_file = "requirements.txt"
    # os.system(f"pip install -r requirements.txt")

    # excelPath = r"C:\Users\abui\Desktop\SPeditor\data\Excel\_TempSPManagement.xlsm"
    (
        spcolumn_filenames,
        numForceCombo,
        forceSet,
        acad_paths,
        lst_fc,
        lst_ec,
        lst_fy,
        lst_es,
    ) = read_excel.get_SPRequiredData_fromExcel(excelPath)
    print(".........READING DATA FROM EXCEL.........")
    # Define the folder name
    folder_name = "automated_cti"

    # Define the path to create the folder
    folder_path = os.path.join(os.getcwd(), folder_name)

    # Create the folder
    os.makedirs(folder_path, exist_ok=True)

    # Change the current working directory to the newly created folder
    os.chdir(folder_path)

    # Create a CTIfile object
    for i in range(len(spcolumn_filenames)):
        CTIfile = spcolumn_cti.CTIfile()
        CTIfile.set_immutable_CTIfields()
        CTIfile.set_project_name("Name")
        CTIfile.set_column_id(spcolumn_filenames[i])
        CTIfile.set_engineer("ABui")
        # CTIfile.set_user_options(numForceCombo[i])
        CTIfile.set_material_properties(
            lst_fc[i] / 1000, lst_ec[i], lst_fy[i], lst_es[i]
        )
        print(".........READING AUTOCADS.........")
        CTIfile.set_external_points_cad(acad_paths[i])
        CTIfile.set_reinforcement_bars_cad(acad_paths[i])
        CTIfile.set_factored_loads(forceSet[i])
        # Write information about CTIfile to a text file
        CTIfile.write_CTIfile_to_file(str(spcolumn_filenames[i]) + ".cti")
        print(
            "Information about CTIfile "
            + str(spcolumn_filenames[i])
            + " has been written"
        )


if __name__ == "__main__":
    main_multi()
