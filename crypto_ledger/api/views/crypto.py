from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utils.custom_drf_permissions import IsVerified

from api.models import Crypto, DailyClosingPrice, CryptoCompareAssets
from api.serializers.crypto import CryptoSerializer, DailyClosingPriceSerializer, CryptoCompareAssetsSerializer

import requests
import time
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status


class CryptoViewSet(viewsets.ModelViewSet):
    serializer_class = CryptoSerializer
    permission_classes = [IsAuthenticated, IsVerified]

    def get_queryset(self):
        return Crypto.objects.all()
    


    
def create_crypto(name, currency):
    crypto = Crypto.objects.filter(name=name)
    if crypto:
        return Response({"detail": 'Crypto already exists'}, status=status.HTTP_400_BAD_REQUEST)
    crypto = Crypto.objects.create(name=name)

    print('new_crypto========', crypto)
    

    def process_data(time, closing_price):
        print(f'Date: {time}, Closing Price: {closing_price}')
        try:
            DailyClosingPrice.objects.create(crypto=crypto, date=time, closing_price=closing_price)
        except:
            print('Failed to add closing price to database')

    def get_crypto_data(crypto, currency, api_key, toTs):
        url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={crypto}&tsym={currency}&limit=2000&toTs={toTs}&api_key={api_key}'
        response = requests.get(url)
        data = response.json()

        if data['Response'] == 'Error':
            raise Exception(data['Message'])

        earliest_time = None
        for entry in reversed(data['Data']['Data']):
            closing_price = entry['close']
            if closing_price == 0:
                return None
            
            date = datetime.fromtimestamp(entry['time']).strftime('%Y-%m-%d')
            process_data(date, closing_price) 

            if earliest_time is None or entry['time'] < earliest_time:
                earliest_time = entry['time']

        return earliest_time
    
    toTs = int(time.time())  
    while True:
        earliest_time = get_crypto_data(crypto.name, currency, 'set your api key', toTs) # set your api key

        if earliest_time is not None:
            toTs = earliest_time - 1 

        else:
            break

    return crypto


          
class DailyClosingPriceViewSet(viewsets.ModelViewSet):
    serializer_class = DailyClosingPriceSerializer
    

    permission_classes =  [IsAuthenticated, IsVerified]

    def get_queryset(self):
        return DailyClosingPrice.objects.all()
    

class CryptoCompareAssetsViewSet(viewsets.ModelViewSet):
    serializer_class = CryptoCompareAssetsSerializer

    permission_classes =  [IsAuthenticated, IsVerified]

    def get_queryset(self):
        return CryptoCompareAssets.objects.all()
    
    def create(self, request, *args, **kwargs):
        
        #use this https://min-api.cryptocompare.com/data/all/coinlist request to get all the coins and store them in the database
        url = 'https://min-api.cryptocompare.com/data/all/coinlist'
        response = requests.get(url)
        data = response.json()
        for key, value in data['Data'].items():
            asset_name = value['Name']
            asset_symbol = value['Symbol']
            try:
                blockchain = value['BuiltOn']
            except:
                blockchain = None
                print('No blockchain')
            try:
                contract_address = value['SmartContractAddress']
                contract_address = contract_address.lower()
                print(contract_address)
            except:
                contract_address = None
                print('No contract address')

            CryptoCompareAssets.objects.create(
                asset_name=asset_name,
                asset_symbol=asset_symbol,
                blockchain=blockchain,
                contract_address=contract_address
            )
        
        return Response({"detail": 'CryptoCompareAssets created'}, status=status.HTTP_201_CREATED)
