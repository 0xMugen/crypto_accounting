from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from django.conf import settings

from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime


from rest_framework.response import Response

from accounts.models import UserProfile

from api.models import Ledgers, Wallets, Reports, Transactions, ExchangeAPIKey, LedgerSort
from api.serializers.ledgers import LedgerSerializer, ExchangeApiKeySerializer, LedgerSortSerializer
from api.serializers.wallets import WalletSerializer

from utils.custom_drf_permissions import IsObjectOwner, IsVerified
from utils.custom_functions import checkETH, checkBTC, checkMATIC
from utils.ledger_format import format_binance_ledger, format_coinbase_ledger, format_kraken_ledger

import pandas as pd

class LedgerViewSet(viewsets.ModelViewSet):
    serializer_class = LedgerSerializer

    permission_classes =  [IsAuthenticated, IsVerified]
    filter_backends = [DjangoFilterBackend, IsObjectOwner]

    def get_queryset(self):
        return Ledgers.objects.all()
    
    def create(self, request, *args, **kwargs):

        file = request.data['file']
        if file is None or not file.name.endswith('.csv'):
            return Response(
                {'file': ["A CSV file is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            filepd = pd.read_csv(file)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
        # file.name = "ledgers/" + request.data['name'] + ".csv"
        # request.data['file'] = file

        userProfile = UserProfile.objects.get(user=request.user)
        request.data['user'] = userProfile.id

        new_ledger_response = super().create(request, *args, **kwargs)
        print('new_ledger========', new_ledger_response.data)
        if (new_ledger_response.status_code == 201):
            try:
                
                new_ledger = Ledgers.objects.get(id=new_ledger_response.data['id'])

                exchange = request.data['exchange']

                if exchange == 'BINANCE':
                    ledgerdf = format_binance_ledger(filepd)
                elif exchange == 'COINBASE':
                    ledgerdf = format_coinbase_ledger(filepd)
                elif exchange == 'KRAKEN':
                    ledgerdf = format_kraken_ledger(filepd)
                else:
                    return Response({"detail": "Exchange not supported"}, status=status.HTTP_400_BAD_REQUEST)

                source = exchange

                for index, row in ledgerdf.iterrows():
                    refid = row['refid']
                    time_naive = datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S')
                    time = timezone.make_aware(time_naive)
                    transaction_type = row['type']
                    asset = row['asset']
                    amount = row['amount']
                    fee = row['fee']
                    balance = row['balance']
                    source = source
                    

                    LedgerSort.objects.create(
                        user = userProfile,
                        order=index,
                        ledger=new_ledger,
                        refid=refid,
                        time=time,
                        transaction_type=transaction_type,
                        asset=asset,
                        amount=amount,
                        fee=fee,
                        balance=balance
                    )

            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return new_ledger_response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LedgerSortViewSet(viewsets.ModelViewSet):
    serializer_class = LedgerSortSerializer
    permission_classes =  [IsAuthenticated, IsVerified]
    filter_backends = [DjangoFilterBackend, IsObjectOwner]

    def get_queryset(self):
        ledger_id = self.request.query_params.get('ledger_id')
        if ledger_id:
            return LedgerSort.objects.filter(ledger=ledger_id)

        return LedgerSort.objects.none()





    

class ExchangeApiKeyViewSet(viewsets.ModelViewSet):
    serializer_class = ExchangeApiKeySerializer
    permission_classes =  [IsAuthenticated, IsVerified]
    filter_backends = [DjangoFilterBackend, IsObjectOwner]

    def get_queryset(self):
        return ExchangeAPIKey.objects.all()

    
    def create(self, request, *args, **kwargs):
        userProfile = UserProfile.objects.get(user=request.user)

        hashed_key = make_password(request.data['api_key'])
        hashed_secret = make_password(request.data['api_secret'])

        key = urlsafe_b64encode(settings.SECRET_KEY.encode()[:32])
        cipher_suite = Fernet(key)

        encrypted_key = cipher_suite.encrypt(hashed_key.encode()).decode()
        encrypted_secret = cipher_suite.encrypt(hashed_secret.encode()).decode()


        request.data['api_key'] = encrypted_key
        request.data['api_secret'] = encrypted_secret
        request.data['user'] = userProfile.id


        return super().create(request, *args, **kwargs)