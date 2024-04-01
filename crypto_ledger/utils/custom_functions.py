from django.core.exceptions import ValidationError

import requests
from decimal import Decimal


def full_name(first_name, last_name, email):
    user_name = ""
    if first_name:
        user_name = first_name
    if last_name:
        if user_name:
            user_name = user_name + " " + last_name
        else:
            user_name = last_name
    if not user_name:
        user_name = email

    return user_name


def checkETH(address):
    API_KEY = "7S299F1ZMY2PB33PJ4Q2ZGZYKZWQZUM48A"
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={API_KEY}'

    response = requests.get(url)
    data = response.json()

    if data['status'] == '1':
        valid = True
    elif data['status'] == '0':
        valid = False
    else:
        valid = False

    if not valid:
        raise ValidationError('Invalid ETH address')

def checkBTC():
    valid = False
    
    if not valid:
        raise ValidationError('Invalid BTC address')

def checkMATIC(address):
    API_KEY = "DMQH2CCBZUY1S1HAHFQE3E5WXHM7UHHJP2"
    url = f'https://api.polygonscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey={API_KEY}'

    response = requests.get(url)
    data = response.json()

    if data['status'] == '1':
        valid = True
    elif data['status'] == '0':
        valid = False
    else:
        valid = False
    
    if not valid:
        raise ValidationError('Invalid MATIC address')
    

def calculate_PMP(df, asset):
    if df.at[0, 'source'] == 'blockexplorer':
        df.at[0, 'average_buy_price'] = df.at[0, 'asset_price']
    else:
        df.at[0, 'average_buy_price'] = 0

    for index, row in df[1:].iterrows():  # Start from the second row
        average_buy_price_prev = df.at[index-1, 'average_buy_price']
        total_bal_prev = df.at[index-1, 'total_balance']

        if row['tx_type'] == 'inner':
            amount_i = row['amount']
            asset_price_i = row['asset_price']
            df.at[index, 'average_buy_price'] = (Decimal(average_buy_price_prev) * total_bal_prev + amount_i * asset_price_i) / row['total_balance']
        elif row['transaction_type'] in ['trade', 'receive'] and row['asset'] == asset:
            amount_prev = df.at[index-1, 'amount']
            df.at[index, 'average_buy_price'] = (Decimal(average_buy_price_prev) * total_bal_prev - amount_prev) / row['total_balance']
        else:
            df.at[index, 'average_buy_price'] = average_buy_price_prev

    return df

def calculate_pv(df):
    for index, row in df.iterrows():
        if row['tx_type'] == 'outer':
            appreciation = (row['asset_price'] - row['average_buy_price']) * row['amount']
            df.loc[index, 'appreciation'] = appreciation
        else:
            df.loc[index, 'appreciation'] = 0
    return df