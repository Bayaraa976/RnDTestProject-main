import pandas as pd
import numpy as np

def load_data(filepath):
    """
    Loads motion capture data from an Excel file.
    
    Args:
        filepath (str): Path to the .xlsx file.
        
    Returns:
        pd.DataFrame: Loaded data.
    """
    try:
        # Load the data, assuming header is on the first row
        df = pd.read_excel(filepath)
        return df
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        raise

def preprocess_data(df):
    """
    Preprocesses the data: interpolates missing values.
    
    Args:
        df (pd.DataFrame): Raw dataframe.
        
    Returns:
        pd.DataFrame: Preprocessed dataframe.
    """
    # Linear interpolation for small gaps
    df_interp = df.interpolate(method='linear', limit_direction='both')
    return df_interp
