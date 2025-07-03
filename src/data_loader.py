import pandas as pd
import os

def read_file(file_name, file_type):
    """
    Reads a CSV or Excel file and returns a DataFrame.
    
    :file_name: Name of the file to read
    :file_type: Type of the file ('csv' or 'excel')
    :return: DataFrame containing the data from the CSV file
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir.endswith('src'):
        parent_path = os.path.dirname(current_dir)
    else:
        parent_path = current_dir
    data_path = os.path.join(parent_path, 'project_dataset')

    try:
        if file_type == 'csv':
            file_path = f"{data_path}/{file_name}.csv"
            df = pd.read_csv(file_path)
        else:
            file_path = f"{data_path}/{file_name}.xlsx"
            df = pd.read_excel(file_path, sheet_name=None)
        return df
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

# calculate frequency of service charge
def create_year_month(df, date_col):
    """
    Creates 'year' and 'month' columns from a date column in the DataFrame.
    
    :df: DataFrame containing the data
    :date_col: Name of the date column to extract year and month from
    :return: DataFrame with 'year' and 'month' columns added
    """
    df['created_year'] = pd.to_datetime(df[date_col]).dt.year
    df['created_month'] = pd.to_datetime(df[date_col]).dt.month
    return df

def load_data(orig=True):
    """
    Loads the cash request and fee data, processes it, and returns the processed DataFrames.
    
    :return: Tuple of processed cash request and fee DataFrames
    """
    cash_req = read_file('extract - cash request - data analyst', 'csv')
    fee = read_file('extract - fees - data analyst - ', 'csv')
    
    if cash_req is None or fee is None:
        return None, None
    
    if orig==False:
        cash_req = create_year_month(cash_req, 'created_at')
        fee = create_year_month(fee, 'created_at')
    
    return cash_req, fee
    

