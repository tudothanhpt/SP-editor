import pandas as pd
from pandas import DataFrame
from sqlalchemy import func

from sqlmodel import Session, select
from sp_editor.database.models import SectionDesignerShape, SDCoordinates_CTI

from sp_editor.core.find_pier import restructure_sdshapeDF, spColumn_CTI_PierPoint, shape_area
from sqlalchemy.engine.base import Engine
from sqlmodel import create_engine

TB_SDSHAPE_ETABS = str(SectionDesignerShape.__name__).lower()
TB_SDSHAPE_CTI = str(SDCoordinates_CTI.__name__).lower()

def read_sdsDB(engine):
    # Read SQL table into a DataFrame
    df_SD = pd.read_sql_table(
        table_name=TB_SDSHAPE_ETABS,  # The table to read
        con=engine                     # The SQLAlchemy engine
    )
    return df_SD

def get_SDCoordinates_CTI_todb(engine: Engine):
    
    """
    Convert Section designer shape from ETABS to CTI format and store in database
    """

    df_sd= read_sdsDB(engine)
    
    lst_PierSDShape=restructure_sdshapeDF(df_sd)
    lst_PierSDName = [list(PierSDShape.keys())[0] for PierSDShape in lst_PierSDShape]
    
    lst_formatted_coordinates_str = []
    lst_area =[]
    
    for SDname in lst_PierSDName:
        formatted_coordinates_str = spColumn_CTI_PierPoint(lst_PierSDShape, SDname)
        area=shape_area(lst_PierSDShape, SDname)
        lst_formatted_coordinates_str.append(formatted_coordinates_str)
        lst_area.append(area)
    
    sd_coordinates_dict_todb = {'SDName': lst_PierSDName, 'Coordinates': lst_formatted_coordinates_str, 'Area': lst_area}    
    
    df_pier_coordinates = pd.DataFrame(sd_coordinates_dict_todb)
    df_pier_coordinates.to_sql(TB_SDSHAPE_CTI, con=engine, if_exists='replace', index=False)

def read_area(engine, SDname: str):
    df_SD = pd.read_sql_table(
        table_name=TB_SDSHAPE_CTI,  # The table to read
        con=engine                     # The SQLAlchemy engine
    )
    
    area =float(df_SD.loc[df_SD['SDName'] == SDname, 'Area'].values[0])
    return area

if __name__ == "__main__":
    engine_temppath = r"tests\TestBM\demo3.spe"
    engine: Engine = create_engine(f"sqlite:///{engine_temppath}")
    example_sdname = "TIER1_P1"
    a = read_area(engine,example_sdname)
    print(a)