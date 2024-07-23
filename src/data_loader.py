import pandas as pd
from .config import CSV_FILES

def load_csv_data():
    dataframes = {}
    for table_name, file_path in CSV_FILES.items():
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Strip any leading/trailing whitespace from columns
        dataframes[table_name] = df
    return dataframes
