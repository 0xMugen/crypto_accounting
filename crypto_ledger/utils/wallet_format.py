import pandas as pd
import numpy as np
import requests



def getTransactions(wallet, blockchain):
    all_transactions = pd.DataFrame()  

    if blockchain == 'ETH':
        API_KEY = "7S299F1ZMY2PB33PJ4Q2ZGZYKZWQZUM48A"

        eth_response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}")
        eth_transactions = eth_response.json()["result"]

        token_response = requests.get(f"https://api.etherscan.io/api?module=account&action=tokentx&address={wallet}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}")
        token_transactions = token_response.json()["result"]        

        # only convert to dataframe and compute transaction fees if there is data
        if eth_transactions:
            eth_df = pd.DataFrame(eth_transactions)
            eth_df["transactionFee"] = eth_df["gasUsed"].astype(int) * eth_df["gasPrice"].astype(int)
            eth_df['value'] = eth_df['value'].apply(lambda x: int(x))
            eth_df['tokenSymbol'] = pd.Series(dtype='str') 
            all_transactions = pd.concat([all_transactions, eth_df], ignore_index=True)
            

        if token_transactions:
            token_df = pd.DataFrame(token_transactions)
            token_df["transactionFee"] = token_df["gasUsed"].astype(int) * token_df["gasPrice"].astype(int) 
            token_df['value'] = token_df['value'].apply(lambda x: int(x)) 
            all_transactions = pd.concat([all_transactions, token_df], ignore_index=True)

        if not all_transactions.empty:
            all_transactions["blockNumber"] = all_transactions["blockNumber"].astype(int)
            all_transactions = all_transactions.sort_values("blockNumber")

        all_transactions['exchange'] = 'etherscan'
        all_transactions['blockchain'] = 'ETH'
        all_transactions['source'] = 'blockexplorer'

    if blockchain == 'MATIC':
        API_KEY = "DMQH2CCBZUY1S1HAHFQE3E5WXHM7UHHJP2"
        url = f'https://api.polygonscan.com/api?module=account&action=balance&address={wallet}&tag=latest&apikey={API_KEY}'

    if not all_transactions.empty:
        all_transactions = all_transactions.replace({np.nan: None})

    return all_transactions





def calcGas(df):
    df['value'] = pd.to_numeric(df['value'])
    df['value'] = df['value'] / 10**18
    df['value'] = df['value'].apply(lambda x: round(x, 20))


    df['gasPrice'] = df['gasPrice'].astype(int) 
    df['gasUsed'] = df['gasUsed'].astype(int) 
    df['gas'] = (df.gasPrice * df.gasUsed) / 10**18
    df['gas'] = df['gas'].apply(lambda x: round(x, 20))
    return df


def filterTransactions(df):
    filtered_df = df.drop(columns=['blockHash', 'nonce', 'transactionIndex', 'gasPrice', 'txreceipt_status',	'input', 'contractAddress',	'cumulativeGasUsed', 'gasUsed', 'confirmations', 'methodId', 'functionName'], axis=1)
    filtered_df = filtered_df.rename(columns={'timeStamp': 'time',})

    #Create new dataframe
    column_names = ['Source', 'time', 'asset', 'type', 'value', 'isError', 'fee', 'gas', 'balance', 'etherscan_bal', 'total_bal', 'token_price', 'PMP', 'PV','from','to', 'tx_type', 'hash', 'blockNumber']
    df_simplified = pd.DataFrame(columns=column_names)

    #Merge
    frames = [filtered_df, df_simplified]
    result = pd.concat(frames, join='outer', ignore_index=False)
    result['Source'] = result['Source'].fillna('BlockExplorer')

    #Change datetime format
    result['time'] = pd.to_datetime(result['time'], unit='s')

    return result