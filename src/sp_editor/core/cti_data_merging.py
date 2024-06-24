import pandas as pd
import sys
import os
from sp_editor.database.models import SectionDesignerShape, SDCoordinates_CTI, PierForce, CalculationCase, CTISummary
from PySide6.QtWidgets import QMessageBox

from sp_editor.core.find_uniform_bars import get_rebarCoordinates_str2
from sp_editor.core.engineering_funcs import calculate_beta1
from sp_editor.crud.cr_general_infor import get_infor
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import make_url
from sp_editor.core.global_variables import *

from sqlmodel import create_engine, Session, select
from sp_editor.core.spcolumn_cti import CTIfile
from PySide6.QtWidgets import QApplication, QMessageBox

TB_CTISUMMARY = str(CTISummary.__name__).lower()
TB_CALCULATIONCASE = str(CalculationCase.__name__).lower()
TB_SDSHAPE_ETABS = str(SectionDesignerShape.__name__).lower()
TB_SDSHAPE_CTI = str(SDCoordinates_CTI.__name__).lower()
TB_PIERFORCE = str(PierForce.__name__).lower()


def get_engine_path(engine):
    # Parse the engine's URL using SQLAlchemy's make_url
    url = make_url(engine.url)

    # Extract the path (for SQLite, the path starts with '/', so we strip the first character)
    db_path = url.database if url.drivername == 'sqlite' else url.database
    # Extract the folder that stores the database
    db_folder = os.path.dirname(db_path)

    return db_folder


def create_file_and_notify(content):
    # Display notification
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setText(content)
    msg_box.setWindowTitle("Notification")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()


def show_warning_force():
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setWindowTitle("Warning")
    msg_box.setText("Please load forces from ETABS")
    msg_box.setInformativeText("No forces found")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()


def read_sdsCTI_DB(engine):
    # Read SQL table into a DataFrame
    df_SD = pd.read_sql_table(
        table_name=TB_SDSHAPE_CTI,  # The table to read
        con=engine  # The SQLAlchemy engine
    )
    return df_SD


def read_calculationCase_DB(engine):
    # Read SQL table into a DataFrame
    df_Case = pd.read_sql_table(
        table_name=TB_CALCULATIONCASE,  # The table to read
        con=engine,  # The SQLAlchemy engine
        columns=['tier', 'pier', 'sds', 'barArea', 'barSpacing', 'barCover',
                 'materialEc', 'materialFc', 'materialFy', 'materialEs', 'casePath']
    )
    return df_Case


def read_pierdesignCTI_forceDB(engine):
    """
    """
    # Read SQL table into a DataFrame
    df = pd.read_sql_table(
        table_name="pierforces_cti",  # The table to read
        con=engine  # The SQLAlchemy engine
    )
    return df  # The DataFrame containing the table data


def read_summaryCTI_DB(engine):
    """
    """
    # Read SQL table into a DataFrame
    df = pd.read_sql_table(
        table_name=TB_CTISUMMARY,  # The table to read
        con=engine  # The SQLAlchemy engine
    )
    return df  # The DataFrame containing the table data


def create_cti_summary_df(engine):
    df_SD = read_sdsCTI_DB(engine)
    df_loadcalculationCase = read_calculationCase_DB(engine)

    try:
        df_designforce = read_pierdesignCTI_forceDB(engine)
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

        merged_df['totalBars'] = lst_totalbarsCTI
        merged_df['rebarCoordinates'] = lst_rebarcoordinatesCTI
        merged_df['pathAfterCreation'] = None

        df_summaryCTI = merged_df[["ID2", "Tier", "Pier",
                                   "materialEc", "materialFc", "materialFy", "materialEs",
                                   "SDName", "coordinates",
                                   "totalBars", "rebarCoordinates",
                                   "totalCombos", "filteredForces",
                                   'casePath', "pathAfterCreation"]]

        df_summaryCTI.to_sql(TB_CTISUMMARY, con=engine, if_exists='replace')

    except Exception as e:
        show_warning_force()


def CTI_creation(engine):
    df_summaryCTI = read_summaryCTI_DB(engine)
    general_infor = get_infor(engine)

    d_code = DesignCode.from_string(general_infor.design_code).value
    u_sys = UnitSystem.from_string(general_infor.unit_system).value
    b_set = BarGroupType.from_string(general_infor.bar_set).value
    confi = ConfinementType.from_string(general_infor.confinement).value
    s_capacity = SectionCapacityMethod.from_string(general_infor.section_capacity).value

    for index, row in df_summaryCTI.iterrows():
        Col_id = row['ID2']
        ec = row['materialEc']
        fc = row['materialFc']
        beta1 = calculate_beta1(float(fc))
        fy = row['materialFy']
        ey = row['materialEs']
        SDCoordinates = row['Coordinates']
        totalbars = row['totalBars']
        rebarcoordinates = row['rebarCoordinates']
        Total_Combos = row['totalCombos']
        Filtered_Forces = row['filteredForces']
        case_path = os.path.normpath(row["casePath"])

        newCTIfile = CTIfile()
        newCTIfile.set_project_name("SP-Editor_Automation")
        newCTIfile.set_engineer("SP-Editor")
        newCTIfile.set_column_id(Col_id)

        newCTIfile.set_material_properties(f_c=fc, E_c=ec, beta1=beta1,
                                           fy=fy, Ey=ey)

        newCTIfile.set_user_options(unit_system=u_sys, design_code=d_code,
                                    confinement=confi,
                                    num_irregular_bars=totalbars, num_factored_loads=Total_Combos,
                                    section_capacity_method=s_capacity)

        newCTIfile.set_external_points(SDCoordinates)
        newCTIfile.set_reinforcement_bars(rebarcoordinates)
        newCTIfile.set_factored_loads(Filtered_Forces)
        newCTIfile.set_bar_group_type(bar_group_type=b_set)
        newCTIfile.write_CTIfile_to_file(case_path, Col_id)

    create_file_and_notify(f"{len(df_summaryCTI)} CTI files created successfully!")


def CTI_creation_from_list(engine, listCTIfile: list):
    df_summaryCTI = read_summaryCTI_DB(engine)

    df_summaryCTI_filtered = df_summaryCTI[df_summaryCTI['ID2'].isin(listCTIfile)]

    general_infor = get_infor(engine)
    engine_path = os.path.abspath(get_engine_path(engine))

    d_code = DesignCode.from_string(general_infor.design_code).value
    u_sys = UnitSystem.from_string(general_infor.unit_system).value
    b_set = BarGroupType.from_string(general_infor.bar_set).value
    confi = ConfinementType.from_string(general_infor.confinement).value
    s_capacity = SectionCapacityMethod.from_string(general_infor.section_capacity).value

    lst_CTIfile_fullpath = []
    for index, row in df_summaryCTI_filtered.iterrows():
        Col_id = row['ID2']
        ec = row['materialEc']
        fc = row['materialFc']
        beta1 = calculate_beta1(float(fc))
        fy = row['materialFy']
        ey = row['materialEs']
        SDCoordinates = row['coordinates']
        totalbars = row['totalBars']
        rebarcoordinates = row['rebarCoordinates']
        Total_Combos = row['totalCombos']
        Filtered_Forces = row['filteredForces']

        case_path = row["casePath"]  # relative case path

        full_path = os.path.join(engine_path, case_path)

        newCTIfile = CTIfile()
        newCTIfile.set_project_name("SP-Editor_Automation")
        newCTIfile.set_engineer("SP-Editor")
        newCTIfile.set_column_id(Col_id)

        newCTIfile.set_material_properties(f_c=fc, E_c=ec, beta1=beta1,
                                           fy=fy, Ey=ey)

        newCTIfile.set_user_options(unit_system=u_sys, design_code=d_code,
                                    confinement=confi,
                                    num_irregular_bars=totalbars, num_factored_loads=Total_Combos,
                                    section_capacity_method=s_capacity)

        newCTIfile.set_external_points(SDCoordinates)
        newCTIfile.set_reinforcement_bars(rebarcoordinates)
        newCTIfile.set_factored_loads(Filtered_Forces)
        newCTIfile.set_bar_group_type(bar_group_type=b_set)
        newCTIfile.write_CTIfile_to_file(full_path, Col_id)

        newCTI_path_after_creation = os.path.join(full_path, Col_id + ".cti")

        lst_CTIfile_fullpath.append(newCTI_path_after_creation)
        df_summaryCTI.loc[df_summaryCTI['ID2'] == Col_id, "pathAfterCreation"] = newCTI_path_after_creation

    df_summaryCTI.to_sql(TB_CTISUMMARY, engine, if_exists="replace", index=False)

    return lst_CTIfile_fullpath


if __name__ == "__main__":
    engine_temppath = r"tests\2.spe"
    engine: Engine = create_engine(f"sqlite:///{engine_temppath}")
