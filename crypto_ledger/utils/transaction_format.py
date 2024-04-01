import pandas as pd

def sortData(df):
    df = df.sort_values(by=['time', 'amount'], ascending=True)

    return df


def find_transfere(df):
    for i, row in df[df['transaction_type'] == 'withdrawal'].iterrows():
        df.at[i, 'is_transfer'] = True
        for j, transfer_row in df.iloc[i+1:].iterrows():
            if (transfer_row['amount'] == -row['amount']) and (transfer_row['source'] == 'Etherscan') and (not transfer_row['is_transfer']):
                df.at[j, 'is_transfer'] = True
                break
    
    return df


def get_Tx_type(df, wallets):
    # Define a function to check if 'from' and 'to' are in the wallet
    def check_internal(row):
        if (row['sender'] in wallets) and (row['receiver'] in wallets):
            return 'internal'
        elif (row['sender'] in wallets) and (row['receiver'] not in wallets):
            return 'outer'
        elif (row['sender'] not in wallets) and (row['receiver'] in wallets):
            return 'inner'
        else:
            return 'unknown'

    df['tx_type'] = df.apply(check_internal, axis=1)
    return df