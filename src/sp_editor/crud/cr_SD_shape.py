import pandas as pd
from pandas import DataFrame
from sqlalchemy import func

from sqlmodel import Session, select
from sp_editor.database.models import SectionDesignerShape, SDCoordinates_CTI

from sp_editor.core.find_pier import restructure_sdshapeDF, spColumn_CTI_PierPoint
from sqlalchemy.engine.base import Engine

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
    
    sd_coordinates_dict_todb = {}
    
    for SDname in lst_PierSDName:
        formatted_coordinates_str = spColumn_CTI_PierPoint(lst_PierSDShape, SDname)
        sd_coordinates_dict_todb[SDname] =formatted_coordinates_str
    
    df_pier_coordinates = pd.DataFrame(list(sd_coordinates_dict_todb.items()), columns=['SDName', 'Coordinates'])
    df_pier_coordinates.to_sql(TB_SDSHAPE_CTI, con=engine, if_exists='replace', index=False)
