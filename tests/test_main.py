from typing import Any

import pandas as pd
from pandas import DataFrame

from core.connect_etabs import show_warning, connect_to_etabs


def get_section_designer_shape_infor(sap_model: Any, etabs_object: Any) -> DataFrame:
    SapModel = sap_model
    EtabsObject = etabs_object
    table_key = 'Section Designer Shapes - Concrete Polygon'

    # Get the database table
    SDS_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName='')
    if SDS_db[-1] != 0:
        error_message = (f"<b>Failed to get table for display.<b> "
                         f"<p>PLease make sure you defined general pier sections. <p>"
                         f"<p> Return code: {SDS_db[-1]}.<p>")
        show_warning(error_message)
        return pd.DataFrame()

    # Extract header and data
    header = SDS_db[2]
    data_values = SDS_db[4]

    # Group the data values into rows
    rows = [data_values[i:i + len(header)] for i in range(0, len(data_values), len(header))]

    # Create the DataFrame
    df = pd.DataFrame(rows, columns=header)
    df_selected = df[['SectionType', 'SectionName', 'ShapeName', 'X', 'Y']]

    return df_selected


if __name__ == '__main__':
    sap_model, etabs_object = connect_to_etabs(model_is_open=True)
    df = get_section_designer_shape_infor(sap_model, etabs_object)
    print(df)
