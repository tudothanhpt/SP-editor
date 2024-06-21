import pandas as pd
import sys

from sp_editor.database.models import SectionDesignerShape, SDCoordinates_CTI, PierForce
from PySide6.QtWidgets import QApplication, QFileDialog
from sp_editor.core.find_pier import restructure_sdshapeDF, spColumn_CTI_PierPoint, shape_area
from sp_editor.core.find_uniform_bars import get_rebarCoordinates_str2
from sqlalchemy.engine.base import Engine
from sqlmodel import create_engine

from spcolumn_cti import CTIfile

TB_SDSHAPE_ETABS = str(SectionDesignerShape.__name__).lower()
TB_SDSHAPE_CTI = str(SDCoordinates_CTI.__name__).lower()
TB_PIERFORCE = str(PierForce.__name__).lower()

data = {
    "tier": ["Tier2", "Tier1", "Tier1", "Tier1", "Tier1", "Tier1", "Tier1"],
    "pier": ["P7", "P1", "P2", "P3", "P4", "P5", "P6"],
    "sds": ["T2_P7", "T1_P1", "T1_P2", "T1_P3", "T1_P4", "T1_P5", "T1_P6"],
    "barArea": [0.5, 1, 0.5, 1, 0.75, 0.5, 1],
    "barSpacing": [6, 8, 12, 10, 6, 6, 6],
    "barCover": [1, 1, 1, 1, 1, 1, 1],
    "barSpacing": [12, 12, 12, 12, 12, 12, 12],
    "ec": [5719.1269, 5104.4513, 5719.1269, 5104.4513, 5719.1269, 5104.4513, 5719.1269],
    "fc": [10, 8, 10, 8, 10, 8, 10],
    "beta1": [0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65],
    "fy": [80, 80, 80, 80, 80, 80, 80],
    "ey": [29000, 29000, 29000, 29000, 29000, 29000, 29000]
}


def read_sdsCTI_DB(engine):
    # Read SQL table into a DataFrame
    df_SD = pd.read_sql_table(
        table_name=TB_SDSHAPE_CTI,  # The table to read
        con=engine  # The SQLAlchemy engine
    )
    return df_SD


def read_pierdesignCTI_forceDB(engine):
    """
    Reads the SQL table `TB_PIERFORCE` into a pandas DataFrame.

    Parameters:
    engine (sqlalchemy.engine.Engine): The SQLAlchemy engine connected to the database.

    Returns:
    pd.DataFrame: The DataFrame containing the table data.
    """
    # Read SQL table into a DataFrame
    df = pd.read_sql_table(
        table_name="pierforces_cti",  # The table to read
        con=engine  # The SQLAlchemy engine
    )

    return df  # The DataFrame containing the table data


def Test1():
    engine_temppath = r"tests\TestBM\demono1.spe"
    engine: Engine = create_engine(f"sqlite:///{engine_temppath}")

    df_SD = read_sdsCTI_DB(engine)
    df_designforce = read_pierdesignCTI_forceDB(engine)
    df_loadcalculationCase = pd.DataFrame(data)  # tobereplaced

    merged_df = pd.merge(df_loadcalculationCase, df_SD, how='left',
                         left_on='sds', right_on='SDName')
    merged_df = pd.merge(merged_df, df_designforce, how='left',
                         left_on=['tier', 'pier'], right_on=['Tier', 'Pier'])

    lst_totalbarsCTI = []
    lst_rebarcoordinatesCTI = []

    for index, row in merged_df.iterrows():
        cover = row['barCover']
        bar_area = row['barArea']
        spacing = row['barSpacing']
        SDname = row['SDName']

        totalbars, rebarcoordinatesCTI = get_rebarCoordinates_str2(engine, cover, bar_area, spacing, SDname)
        lst_totalbarsCTI.append(totalbars)
        lst_rebarcoordinatesCTI.append(rebarcoordinatesCTI)

    merged_df['totalbars'] = lst_totalbarsCTI
    merged_df['rebarcoordinates'] = lst_rebarcoordinatesCTI

    merged_df = merged_df[["ID2", "Tier", "Pier",
                           "ec", "fc", "beta1", "fy", "ey",
                           "SDName", "Coordinates",
                           "totalbars", "rebarcoordinates",
                           "Total Combos", "Filtered Forces"]]

    pd.set_option('display.max_colwidth', 20)

    return merged_df


def get_folder_path() -> str:
    app = QApplication(sys.argv)

    # Open folder selection dialog
    folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")

    app.exit()
    return folder_path


def main():
    merged_df = Test1()
    folder_path = get_folder_path()
    for index, row in merged_df.iterrows():
        Col_id = row['ID2']
        ec = row['ec']
        fc = row['fc']
        beta1 = row['beta1']
        fy = row['fy']
        ey = row['ey']
        SDCoordinates = row['Coordinates']
        totalbars = row['totalbars']
        rebarcoordinates = row['rebarcoordinates']
        Total_Combos = row['Total Combos']
        Filtered_Forces = row['Filtered Forces']

        newCTIfile = CTIfile()
        newCTIfile.set_project_name("SP-Editor")
        newCTIfile.set_engineer("ABui")
        newCTIfile.set_column_id(Col_id)

        newCTIfile.set_material_properties(f_c=fc, E_c=ec, beta1=beta1,
                                           fy=fy, Ey=ey)

        newCTIfile.set_user_options(unit_system=0, design_code=8,
                                    confinement=0,
                                    num_irregular_bars=totalbars, num_factored_loads=Total_Combos,
                                    section_capacity_method=0)
        newCTIfile.set_external_points(SDCoordinates)
        newCTIfile.set_reinforcement_bars(rebarcoordinates)
        newCTIfile.set_factored_loads(Filtered_Forces)
        newCTIfile.set_bar_group_type(bar_group_type=1)
        newCTIfile.write_CTIfile_to_file(folder_path, Col_id)

        print("Information about CTIfile " + Col_id + " has been written")


if __name__ == "__main__":
    main()
