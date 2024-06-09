
import pandas as pd

def read_json_file(file_path):
    """
    Reads a JSON file and returns a DataFrame.
    
    Parameters:
    file_path (str): The path to the JSON file.
    
    Returns:
    pd.DataFrame: The DataFrame containing the data from the JSON file.
    """
    df = pd.read_json(file_path)
    return df

# Example usage
file_path = r"C:\Users\abui\Documents\BM\git\repo\SP-editor\src\SP-editor\database\material_table\tb_ACI_Concrete.json"
df = read_json_file(file_path)
print(df)