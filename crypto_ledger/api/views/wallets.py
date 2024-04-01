from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.permissions import IsAuthenticated
from utils.custom_drf_permissions import IsObjectOwner, IsVerified

from api.models import UserProfile, Wallets, WalletsSort, WalletToken, CryptoCompareAssets
from api.serializers.wallets import WalletSerializer, WalletSortSerializer, WalletTokenSerializer

from rest_framework.response import Response

from utils.custom_functions import checkETH, checkBTC, checkMATIC

from django.core.exceptions import ValidationError

import pandas as pd
from decimal import Decimal

from utils.transaction_format import get_Tx_type
from utils.wallet_format import getTransactions
import requests

class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer

    permission_classes =  [IsAuthenticated, IsVerified]
    filter_backends = [DjangoFilterBackend, IsObjectOwner]


    def get_queryset(self):
        return Wallets.objects.all().prefetch_related('wallettoken_set')

    
    def create(self, request, *args, **kwargs):
        userProfile = UserProfile.objects.get(user=request.user)
        request.data['user'] = userProfile.id

        data = request.data
        blockchain = data['blockchain']
        
        try:
            if blockchain == 'ETH':
                checkETH(data['address'])
            elif blockchain == 'BTC':
                checkBTC(data['address'])
            elif blockchain == 'MATIC':
                checkMATIC(data['address'])
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        data['address'] = data['address'].lower()
        new_response_wallet = super().create(request, *args, **kwargs)
        print("new wallet=======", new_response_wallet.data)

        if new_response_wallet.status_code == 201:
            try:
                df_transactions = pd.DataFrame()

                # get all transactions from selected wallets
                walletAddress = new_response_wallet.data['address']

                try:
                    df_transactions = getTransactions(walletAddress, 'ETH')
                except Exception as e:
                    print("failed to get transaction for wallet: ", walletAddress)
                    print(e)
                    return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                df_transactions = df_transactions.rename(columns={'timeStamp': 'time', 'value': 'amount'})
                df_transactions['time'] = pd.to_datetime(df_transactions['time'], unit='s')
                df_transactions['time'] = df_transactions['time'].dt.tz_localize('UTC')

                print("got block explorer data")

            except Exception as e:
                print("failed to get transactions")
                print(e)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            # try:
            # token_names = df_transactions['tokenSymbol'].unique()
            contract_address = df_transactions['contractAddress'].unique()
            for address in contract_address:
                if address is None or address == 'None' or address == '':
                    continue
                token_name = df_transactions[df_transactions['contractAddress'] == address]['tokenName'].iloc[0]
                print("address", address)
                print("token_name", token_name)
                count = df_transactions['contractAddress'].value_counts()[address]
                if len(token_name) > 50:
                    token_name = token_name[:50]
                #check if token_name is in the CryptoCompareAssets asset_name or symbole
                if address not in CryptoCompareAssets.objects.values_list('contract_address', flat=True):
                    is_asset_price = False
                else:
                    is_asset_price = True
                WalletToken.objects.create(
                    user = userProfile,
                    wallet = Wallets.objects.get(id=new_response_wallet.data['id']),
                    token = token_name,
                    count = count,
                    contract_address = address,
                    is_asset_price = is_asset_price,
                )
            count = df_transactions['tokenSymbol'].isnull().sum()

            WalletToken.objects.create(
                user = userProfile,
                wallet = Wallets.objects.get(id=new_response_wallet.data['id']),
                token = blockchain,
                count = count,
                is_asset_price = True,
            )
            # except Exception as e:
            #     print("failed to get token symbols")
            #     print(e)
            #     return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            for index, row in df_transactions.iterrows():
                user = userProfile
                wallet = Wallets.objects.get(id=new_response_wallet.data['id'])
                blockchain = row['blockchain']


                if row['tokenSymbol'] is None:
                    row['amount'] = Decimal(row['amount']) / Decimal('1e18')
                else:
                    row['amount'] = Decimal(row['amount']) / Decimal('10')**int(row['tokenDecimal'])
                row['transactionFee'] = Decimal(row['transactionFee']) / Decimal('1e18')

                block_number = row['blockNumber']
                time = row['time']
                hash = row['hash']
                source = row['source']
                exchange = row['exchange']
                amount = row['amount']  
                token_name = row['tokenName'] 
                contract_address = row['contractAddress']
                if token_name is None:
                    token_name = blockchain
                    contract_address = None

                if row['isError'] == '1':
                    isError = True
                else:
                    isError = False
                gasfee = row['transactionFee']
                gas = row['gas']
                sender = row['from']
                receiver = row['to']
                hash = row['hash']
                token_symbol = row['tokenSymbol']
                token_decimal = row['tokenDecimal']

                try:
                    WalletsSort.objects.create(
                        user = user,
                        order = index,
                        blockchain = blockchain,
                        block_number = block_number,
                        source = source,
                        time = time,
                        amount = amount,
                        isError = isError,
                        gas = gas,
                        sender = sender,
                        receiver = receiver,
                        hash = hash,
                        token_symbol = token_symbol,
                        token_decimal = token_decimal,
                        wallet = wallet,
                        gasfee = gasfee,
                        exchange = exchange,
                        token_name = token_name,
                        contract_address = contract_address,
                    )


                except Exception as e:
                    print("failed to create Wallet data")
                    print(e)
                    return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)   
            return new_response_wallet
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class WalletSortViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSortSerializer

    permission_classes =  [IsAuthenticated, IsVerified]
    filter_backends = [DjangoFilterBackend, IsObjectOwner]

    def get_queryset(self):
        wallet_id = self.request.query_params.get('wallet_id')
        if wallet_id:
            return WalletsSort.objects.filter(wallet=wallet_id)

        return WalletsSort.objects.none()
    
class WalletTokenViewSet(viewsets.ModelViewSet):
    serializer_class = WalletTokenSerializer

    permission_classes = [IsAuthenticated, IsVerified]
    filter_backends = [DjangoFilterBackend, IsObjectOwner]


    def get_queryset(self):
        wallet_id = self.request.query_params.get('wallet_id', None)
        if wallet_id is not None:
            get_crypto_data()
            return WalletToken.objects.filter(wallet=wallet_id)
        else:
            return WalletToken.objects.all()
        

def get_crypto_data():
        api_key = 'cca15a1dc19a548b0da18c3b56a4fab68b6a8ea2b7acc4376c8bfdd7a84da332'
        url = f'https://min-api.cryptocompare.com/data/blockchain/list?api_key={api_key}'
        response = requests.get(url)
        data = response.json()

        if data['Response'] == 'Error':
            raise Exception(data['Message'])

        (data)
