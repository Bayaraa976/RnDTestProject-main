import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, medfilt

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

def remove_outliers_median(data, kernel_size=3):
    """
    Applies a median filter to remove spike noise.
    
    Args:
        data (np.array): 1D array of data.
        kernel_size (int): Size of the window (must be odd).
        
    Returns:
        np.array: Filtered data.
    """
    if kernel_size % 2 == 0:
        kernel_size += 1
    return medfilt(data, kernel_size)

def filter_dataframe(df, cutoff=6.0, fs=100.0, order=4, columns_to_filter=None):
    """
    Applies outlier removal (median) and low-pass filter to specified columns in a DataFrame.
    
    Strategy:
    1. Median Filter (to kill spikes)
    2. Butterworth Low-Pass (to smooth)
    
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
            continue 
            
        try:
            # 1. Median Filter for Outliers
            # Using a small kernel size to remove single-frame spikes without distorting movement too much
            data_despiked = remove_outliers_median(df[col].values, kernel_size=5)
            
            # 2. Low-Pass Filter for Smoothing
            df_filtered[col] = butter_lowpass_filter(data_despiked, cutoff, fs, order)
        except Exception as e:
            print(f"Warning: Could not filter column {col}: {e}")
            
    return df_filtered
