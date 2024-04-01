import pandas as pd
import numpy as np


def format_binance_ledger(df_ledger):
    return df_ledger


def format_coinbase_ledger(df_ledger):
    return df_ledger


def format_kraken_ledger(df_ledger):
    df_ledger = df_ledger.groupby('refid').apply(remove_duplicates).reset_index(drop=True)
    df_ledger = sortKraken(df_ledger)

    print(df_ledger)

    return df_ledger


###########################################################################
def remove_duplicates(group):
    if group['type'].eq('withdrawal').any():
        duplicates = group[group.duplicated(subset=['refid', 'type'], keep='first')]
        if not duplicates.empty:
            last_duplicate = duplicates.iloc[-1]
            last_duplicate_index = duplicates.index[-1]
            last_duplicate_balance = last_duplicate['balance']
            group.loc[group.index != last_duplicate_index, 'balance'] = last_duplicate_balance
        return group[~group.duplicated(subset=['refid', 'type'], keep='first')]
    else:
        return group
     

def sortKraken(df):
    column_names = ['Source','refid', 'time', 'asset', 'balance', 'type']
    df_simplified = pd.DataFrame(columns=column_names)
    #Merge
    frames = [df, df_simplified]
    result = pd.concat(frames, join='outer', ignore_index=False)
    result['Source'] = result['Source'].fillna('Kraken')
    result['balance'] = result['balance'].fillna('0')
    return result



def filterToken(df, asset):
    df['asset'] = df['asset'].replace({'XETH': 'ETH', 'XXBT': 'BTC', 'XLTC': 'LTC', 'XXRP': 'XRP'})
      
    asset_rows = df[df['asset'] == asset]
    refids = asset_rows['refid'].tolist()
    filtered_df = df[df['refid'].isin(refids)]

    filtered_df = filtered_df.rename(columns={'C': 'Z'})
    
    return filtered_df