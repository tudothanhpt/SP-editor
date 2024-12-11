import pandas as pd
import numpy as np
from sp_editor.crud.cr_pier_force import read_pierdesign_forceDB
from sp_editor.crud.cr_level_group import read_groupDB
from sqlmodel import create_engine
from sqlalchemy.engine import Engine


# ENSURE THE 2 GIVEN DATAFRAMES' HEADERS TO BE ADDRESSED CORRECTLY FOLLOWING THE BELOW CONVENTION


def set_units_in_etabs_model(sap_model):
    """
    Set the units in an ETABS model.

    Parameters:
    sap_model (comtypes.client._compointer): The ETABS model object.
    unit_system (int): The unit system to set.

    Returns:
    str: Success message or error message.
    """
    # Set the present units
    ret = sap_model.SetPresentUnits(3)

    # Check if the units were successfully set
    if ret == 0:
        return "Units successfully set."
    else:
        return "Error setting units."


def create_force_filter_df(
    df_PierForces: pd.DataFrame, df_Tier: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge two DataFrames on the 'Story' column, create new columns based on certain operations,
    and return the resulting DataFrame.

    Parameters:
    df1 (pd.DataFrame): Pier Forces DataFrame
    df2 (pd.DataFrame): Group Definition DataFrame

    Returns:
    df3 (pd.DataFrame: The merged DataFrame with new columns.
    """
    df_FilteredForces = df_PierForces.merge(df_Tier, on="Story", how="left")
    df_FilteredForces["Tier"] = df_FilteredForces["Tier"].fillna("")

    df_FilteredForces["ID2"] = df_FilteredForces.apply(
        lambda row: row["Tier"] + "_" + row["Pier"]
        if row["Tier"] != "None"
        else "None",
        axis=1,
    )

    df_FilteredForces["ID3"] = (
        df_FilteredForces["Story"]
        + df_FilteredForces["Pier"]
        + df_FilteredForces["Combo"]
        + df_FilteredForces["Location"]
    )

    df_FilteredForces["P_SPCol"] = np.round(df_FilteredForces["P"], 0).astype(float) * (
        -1
    )
    df_FilteredForces["Mx_SPCol"] = np.round(df_FilteredForces["M2"], 0).astype(float)
    df_FilteredForces["My_SPCol"] = np.round(df_FilteredForces["M3"], 0).astype(float)
    df_FilteredForces = df_FilteredForces[
        ["ID2", "Tier", "Pier", "ID3", "P_SPCol", "Mx_SPCol", "My_SPCol"]
    ]
    return df_FilteredForces


def force_filter_SPformat(df3: pd.DataFrame, group_value: str) -> tuple:
    """
    Merge two DataFrames on the 'Story' column, create new columns based on certain operations,
    filter rows based on specific conditions, and generate a formatted result string.

    Parameters:
    df3 (pd.DataFrame: The merged DataFrame with new columns.
    pier_value (str): The value to filter the 'Pier' column
    tier (str): The value to filter the 'Force Grouping' column

    Returns:
    tuple: A tuple containing the result string and the filtered DataFrame.
    """

    # Filter rows based on specific conditions
    filter_cond = df3["ID2"] == group_value
    filter_df = df3.loc[filter_cond, ["P_SPCol", "Mx_SPCol", "My_SPCol"]]

    # Create the 'Combined_Col' column by concatenating 'P_SPCol', 'Mx_SPCol', 'My_SPCol'
    filter_df["Combined_Col"] = filter_df.apply(
        lambda row: f"{row['P_SPCol']},{row['Mx_SPCol']},{row['My_SPCol']}", axis=1
    )

    # Get the total number of filtered rows
    total_rows = filter_df.shape[0]

    # Convert the 'Combined_Col' column values to a list
    combined_values = filter_df["Combined_Col"].to_list()

    # Join the list into a single string with each value on a new line
    load_string = "\n".join(combined_values)

    # Create the result string
    result_string = f"{total_rows}\n{load_string}"

    return result_string, total_rows


def get_pierforces_CTI_todb(engine: Engine):
    df_PierForces = read_pierdesign_forceDB(engine)
    df_Tier = read_groupDB(engine)

    df_FilteredForces = create_force_filter_df(df_PierForces, df_Tier)

    list_PierInEachTier = df_FilteredForces["ID2"].unique().tolist()
    list_PierInEachTier = [item for item in list_PierInEachTier if item != "None"]

    lst_result_string = []
    lst_total_rows = []
    lst_tier = []
    lst_pier = []

    for PierInEachTier in list_PierInEachTier:
        result_string, total_rows = force_filter_SPformat(
            df_FilteredForces, PierInEachTier
        )
        tier, pier = PierInEachTier.split("_")
        lst_tier.append(tier)
        lst_pier.append(pier)
        lst_result_string.append(result_string)
        lst_total_rows.append(total_rows)

    dict_pierforces_cti_db = {
        "ID2": list_PierInEachTier,
        "Tier": lst_tier,
        "Pier": lst_pier,
        "filteredForces": lst_result_string,
        "totalCombos": lst_total_rows,
    }
    df_pierforces_cti_db = pd.DataFrame(dict_pierforces_cti_db)
    df_pierforces_cti_db.to_sql(
        "pierforces_cti", con=engine, if_exists="replace", index=False
    )


if __name__ == "__main__":
    engine_temppath = r"tests\TestBM\demo1.spe"
    engine: Engine = create_engine(f"sqlite:///{engine_temppath}")
    get_pierforces_CTI_todb(engine)
