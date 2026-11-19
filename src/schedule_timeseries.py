import pandas as pd
import numpy as np

def compute_evm_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Earned Value Management (EVM) parameters across work packages:
    - Cost Variance (CV) = EV - AC
    - Schedule Variance (SV) = EV - PV
    - Cost Performance Index (CPI) = EV / AC
    - Schedule Performance Index (SPI) = EV / PV
    - Estimate At Completion (EAC) = BAC / CPI
    """
    df = df.copy()
    df['CV'] = df['EV'] - df['AC']
    df['SV'] = df['EV'] - df['PV']
    df['CPI'] = np.where(df['AC'] > 0, df['EV'] / df['AC'], 1.0)
    df['SPI'] = np.where(df['PV'] > 0, df['EV'] / df['PV'], 1.0)
    df['EAC'] = np.where(df['CPI'] > 0, df['BAC'] / df['CPI'], df['BAC'])
    return df
