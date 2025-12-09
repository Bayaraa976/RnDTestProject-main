import numpy as np
from scipy.signal import butter, filtfilt

def butter_lowpass_filter(data, cutoff, fs, order=4):
    """
    Applies a zero-lag Butterworth low-pass filter to the data.
    
    Args:
        data (np.array): 1D array of data to filter.
        cutoff (float): Cutoff frequency in Hz.
        fs (float): Sampling frequency in Hz.
        order (int): Order of the filter.
        
    Returns:
        np.array: Filtered data.
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def filter_dataframe(df, cutoff=6.0, fs=100.0, order=4, columns_to_filter=None):
    """
    Applies the low-pass filter to specified columns in a DataFrame.
    
    Args:
        df (pd.DataFrame): Dataframe containing the data.
        cutoff (float): Cutoff frequency.
        fs (float): Sampling frequency.
        order (int): Filter order.
        columns_to_filter (list): List of column names to filter. If None, filters all numeric columns.
        
    Returns:
        pd.DataFrame: A new DataFrame with filtered data.
    """
    df_filtered = df.copy()
    
    if columns_to_filter is None:
        columns_to_filter = df.select_dtypes(include=[np.number]).columns
        
    for col in columns_to_filter:
        # Check for NaNs and handle them (simple check)
        if df[col].isnull().any():
            # Should have been interpolated before, but just in case
            continue 
            
        try:
            df_filtered[col] = butter_lowpass_filter(df[col].values, cutoff, fs, order)
        except Exception as e:
            print(f"Warning: Could not filter column {col}: {e}")
            
    return df_filtered
