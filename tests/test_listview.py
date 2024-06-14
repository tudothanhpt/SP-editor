from typing import Any

import pandas as pd
from core.connect_etabs import connect_to_etabs

sapmodel, etabsobject = connect_to_etabs()


def get_pier_label_infor(sap_model: Any, etabs_object: Any) -> DataFrame:
    """
        returns: DataFrame

        Return dataframe of list level

        """
    SapModel = sap_model
    EtabsObject = etabs_object
    # get the table
    table_key: str = 'Area Assignments - Pier Labels'

    # get the database table
    story_db = SapModel.DatabaseTables.GetTableForDisplayArray(table_key, GroupName='')
    # Extract header and data
    header = story_db[2]
    data_values = story_db[4]

    # Group the data values into rows
    rows = [data_values[i:i + len(header)] for i in range(0, len(data_values), len(header))]

    # Create the DataFrame
    df = pd.DataFrame(rows, columns=header)

    # Select only the 'Story' and 'Height' columns
    df_selected = df[['Story', 'Height']]
    return df_selected


if __name__ == '__main__':
    get_pier_label_infor()
