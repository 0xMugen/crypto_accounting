from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from api.serializers.reports import ReportSerializer, SubReportSerializer, TransactionSerializer

from rest_framework.permissions import IsAuthenticated
from utils.custom_drf_permissions import IsObjectOwner, IsVerified
from utils.wallet_format import getTransactions, calcGas
from django.shortcuts import get_object_or_404

from api.models import Reports, UserProfile, Wallets, Ledgers, Transactions, SubReports, LedgerSort, Crypto, DailyClosingPrice, WalletsSort, CryptoCompareAssets
from api.views.crypto import create_crypto

from rest_framework.response import Response

from utils.ledger_format import filterToken
from utils.transaction_format import find_transfere, sortData, get_Tx_type
from utils.custom_functions import calculate_PMP, calculate_pv

from django.utils import timezone
from datetime import datetime
import pandas as pd
from decimal import Decimal


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    permission_classes = [IsAuthenticated, IsVerified]
    filter_backends = [DjangoFilterBackend, IsObjectOwner]

    def get_queryset(self):
        return Reports.objects.all()
    
    def create(self, request, *args, **kwargs):
        postData = request.data

        userProfile = UserProfile.objects.get(user=request.user)
        request.data['user'] = userProfile.id

        walletsId = postData['wallets']
        request.data['wallets'] = walletsId

        ledgersId = postData.get('ledgers', [])

        selectedBlockchains = postData['blockchains']
        selectedTokenContracts = postData['contracts']
        currency = postData['currency']
     

        new_report_response = super().create(request, *args, **kwargs)
        print('new_report========', new_report_response.data)

        if (new_report_response.status_code == 201):

            df_ledger = pd.DataFrame()

            if ledgersId:  # Check if ledgersId is not empty
                try:
                    df_list = []  # List to store dataframes
                    for ledgerId in ledgersId:
                        ledger = Ledgers.objects.get(id=ledgerId)
                        ledgerExchange = ledger.exchange
                        ledgerSorts = LedgerSort.objects.filter(ledger=ledger)
                        # store in a list all ledgerSort dataframes
                        for ledgerSort in ledgerSorts:
                            df = ledgerSort.to_dataframe()
                            df['exchange'] = ledgerExchange
                            df_list.append(df)

                    # Concatenate all dataframes in the list to create a single dataframe
                    if df_list:  # Check if df_list is not empty
                        df_ledger = pd.concat(df_list, ignore_index=True)

                except Exception as e:
                    print("failed to get ledgers")
                    print(e)
                    return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                df_ledger['source'] = 'ledger'

                print("got ledger data")

            report = Reports.objects.get(id=new_report_response.data['id'])

            # try:
            df_transactions = pd.DataFrame()

            # get all transactions from selected wallets
            walletAddresses = []
            df_list = []
            for walletId in walletsId:
                walletAddress = Wallets.objects.get(id=walletId).address
                walletSorts = WalletsSort.objects.filter(wallet=walletId)
                walletAddresses.append(walletAddress)
                for walletSort in walletSorts:
                    df = walletSort.to_dataframe()
                    df_list.append(df)

            try:
                df_transactions = pd.concat(df_list, ignore_index=True)
            except Exception as e:
                print("failed to get transaction for wallet: ", walletAddress)
                print(e)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            df_transactions = get_Tx_type(df_transactions, walletAddresses)
            df_transactions = df_transactions.sort_values(by=['time'])


            print("got block explorer data")

            # except Exception as e:
            #     print("failed to get transactions")
            #     print(e)
            #     return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            print("creating reports for the tokens")
            for contract in selectedTokenContracts:
                #if contract null
                if contract[0] == None:
                    token = contract[1]
                else:
                #check if token exists in the crypto model
                    print('contract', contract)
                    token = CryptoCompareAssets.objects.get(contract_address=contract[0])
                    print('token', token)
                    token = token.asset_symbol
                try:
                    crypto = Crypto.objects.get(name=token)
                    print('Token exists')
                except:
                    print('Token in creation')
                    try:
                        print('Getting all closing prices for ', token)
                        create_crypto(token, currency)
                        crypto = Crypto.objects.get(name=token)
                    except:
                        crypto = None
                        print('Failed to get crypto prices. Token is not supported')

                   

                subreport = SubReports.objects.create(user=userProfile, report=report, token=token)

                if ledgersId:
                    df_ledg = df_ledger.copy()
                    df_ledg = filterToken(df_ledger, token)
                    df_ledg.loc[df_ledg['asset'] != token, 'balance'] = 0


                df_tx = df_transactions.copy()

                if token == 'ETH':
                    df_tx = df_tx[df_tx['token_symbol'].isnull()]                    
                    df_tx.loc[df_tx['isError'] == True, 'amount'] = 0
                    df_tx['balance'] = df_tx.apply(lambda row: row['amount'] if row['tx_type'] == 'inner' else (-row['amount'] - row['gasfee']) if row['token_symbol'] is None else -row['gasfee'], axis=1)
                    df_tx['balance'] = df_tx['balance'].cumsum()


                else:
                    df_tx = df_tx[df_tx['token_symbol'] == token]
                    df_tx['balance'] = df_tx.apply(lambda row: row['amount'] if row['tx_type'] == 'inner' else -row['amount'], axis=1)
                    df_tx['balance'] = df_tx['balance'].cumsum()

                #getting asset price
                asset_price = []
                for index, row in df_tx.iterrows():
                    try:
                        closing_price = DailyClosingPrice.objects.get(crypto=crypto, date=row['time'].date()).closing_price
                        asset_price.append(closing_price)
                    except DailyClosingPrice.DoesNotExist:
                        try:
                            closing_price = DailyClosingPrice.objects.get(crypto=crypto, date=row['time'].date() + timezone.timedelta(days=1)).closing_price
                            asset_price.append(closing_price)
                        except DailyClosingPrice.DoesNotExist:
                            asset_price.append(0)         
                df_tx['asset_price'] = asset_price    

                #calculate gas price in Euro
                df_tx['gasToCurrency'] = df_tx['gasfee'] * df_tx['asset_price']

                if ledgersId:
                    df_tx = pd.concat([df_ledg, df_tx], ignore_index=True)
                else:
                    df_tx['transaction_type'] = None

                df_tx = sortData(df_tx)
                if ledgersId:
                    df_tx = find_transfere(df_tx)
                df_tx = df_tx.reset_index(drop=True)
                print('data is sorted for token: ', token)


                #get every unique exchange

                unique_exchanges = df_tx['exchange'].unique()
                exchange_balances = {exchange: 0 for exchange in unique_exchanges}
                total_balance = []

                for index, row in df_tx.iterrows():
                    exchange_balances[row['exchange']] = row['balance']
                    
                    total_balance.append(sum(exchange_balances.values()))

                df_tx['total_balance'] = total_balance 


                #Get pmp
                df_tx = calculate_PMP(df_tx, token)
                #Get appreciation
                try:
                    df_tx = calculate_pv(df_tx)
                except:
                    print('failed to calculate appreciation')

                for index, row in df_tx.iterrows():
                    if row['source'] == 'blockexplorer':
                        user = userProfile
                        report = Reports.objects.get(id=new_report_response.data['id'])
                        blockchain = 'ETH'

                        average_buy_price = row['average_buy_price']
                        appreciation = row['appreciation']

                        block_number = row['block_number']
                        time = row['time']
                        hash = row['hash']
                        source = 'blockexplorer'
                        exchange = row['exchange']
                        total_balance = row['total_balance']
                        asset_price = row['asset_price']
                        tx_type = row['tx_type']
                        asset = token
                        contract_address = row['contract_address']
                        if token == 'ETH':
                            contract_address = None
                            amount = row['amount']
                            balance = row['balance']

                        isError = row['isError']
                        gasfee = row['gasfee']
                        gas = row['gas']
                        gasToCurrency = row['gasToCurrency']
                        sender = row['sender']
                        receiver = row['receiver']
                        hash = row['hash']
                        is_erc = False
                        is_transfer = False

                        if row['token_symbol'] is not None:
                            is_erc = True
                            token_name = row['token_name']       
                            if token == 'ETH':
                                asset = 'Fee'
                                amount = 0
                            else:
                                asset = token_name
                                amount = row['amount']
                                balance = row['balance']
                            token_symbol = row['token_symbol']
                            token_decimal = row['token_decimal']
                        else:
                            token_name = None   
                            token_symbol = None
                            token_decimal = None

                        try:
                            Transactions.objects.create(
                                user = user,
                                report = report,
                                sub_report = subreport,
                                order = index,
                                blockchain = blockchain,
                                block_number = block_number,
                                source = source,
                                average_buy_price = average_buy_price,
                                appreciation = appreciation,
                                time = time,
                                asset = asset,
                                balance = balance,
                                total_balance = total_balance,
                                amount = amount,
                                isError = isError,
                                gasfee = gasfee,
                                gas = gas,
                                gasToCurrency = gasToCurrency,
                                sender = sender,
                                receiver = receiver,
                                tx_type = tx_type,
                                hash = hash,
                                is_erc = is_erc,
                                is_transfer = is_transfer,
                                asset_price = asset_price,
                                original_asset_price = asset_price,
                                token_name = token_name,
                                token_symbol = token_symbol,
                                token_decimal = token_decimal,
                                exchange =exchange,
                                contract_address = contract_address
                            )


                        except Exception as e:
                            print("failed to create transaction")
                            print(e)
                            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)   
                    elif row['source'] == 'ledger':
                        report = Reports.objects.get(id=new_report_response.data['id'])
                        order = index
                        ledger = row['ledger']
                        ledger = Ledgers.objects.get(id=ledger)
                        average_buy_price = row['average_buy_price']
                        appreciation = row['appreciation']


                        time = row['time']
                        asset = row['asset']
                        refid = row['refid']
                        source = 'ledger'
                        exchange = row['exchange']
                        transaction_type = row['transaction_type']
                        fee = row['fee']
                        balance = row['balance']
                        total_balance = row['total_balance']
                        amount = row['amount']
                        try:
                            Transactions.objects.create(
                                user = userProfile,
                                report = report,
                                order = order,
                                ledger = ledger,
                                time = time,
                                average_buy_price = average_buy_price,
                                appreciation = appreciation,
                                asset = asset,
                                refid = refid,
                                source = source,
                                transaction_type = transaction_type,
                                fee = fee,
                                balance = balance,
                                total_balance = total_balance,
                                amount = amount,
                                sub_report = subreport,
                                exchange = exchange,
                            )
                        except Exception as e:
                            print("failed to create transaction")
                            print(e)
                            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


                print('transactions created for token: ', token)
        
            print('All transactions created')


        return Response(new_report_response.data, status=status.HTTP_201_CREATED)
    



class SubReportViewSet(viewsets.ModelViewSet):
    serializer_class = SubReportSerializer

    permission_classes = [IsAuthenticated, IsVerified]
    filter_backends = [DjangoFilterBackend, IsObjectOwner]

    def get_queryset(self):
        report_id = self.request.query_params.get('report_id')
        if report_id:
            return SubReports.objects.filter(report=report_id)

        return SubReports.objects.none()



class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    permission_classes = [IsAuthenticated, IsVerified]
    filter_backends = [DjangoFilterBackend, IsObjectOwner]

    def get_queryset(self):
        queryset = Transactions.objects.all()
        report_id = self.request.query_params.get('report_id', None)
        if report_id is not None:
            queryset = queryset.filter(sub_report=report_id)
            #sort by order
            queryset = queryset.order_by('order')
        return queryset
    

    def partial_update(self, request, *args, **kwargs):
        transaction = self.get_object()
        if request.data.get('asset_price'):       
            transaction.asset_price = request.data.get('asset_price')
        else:
            transaction.asset_price = transaction.original_asset_price
        transaction.save()
        print('asset price updated')
        

        # try:
        df = []
        transactions = Transactions.objects.filter(sub_report=transaction.sub_report)
        for transaction in transactions:
            transaction_id = transaction.id
            df_tx = transaction.to_dataframe()
            df_tx['id'] = transaction_id
            df.append(df_tx)
        if df:  # Check if df_list is not empty
            df_data = pd.concat(df, ignore_index=True)

        df_data = df_data.sort_values(by=['order'])
        df_data = df_data.reset_index(drop=True)
        df_data = calculate_PMP(df_data, transaction.asset)
        df_data = calculate_pv(df_data)

        for index, row in df_data.iterrows():
            transaction = Transactions.objects.get(id=row['id'])
            transaction.appreciation = row['appreciation']
            transaction.average_buy_price = row['average_buy_price']
            transaction.save()
        # except:
        #     return Response({"detail": "failed to calculate PMP and PV"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "asset price updated"})
    
