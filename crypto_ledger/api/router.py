from rest_framework import routers

from api.views.ledgers import LedgerViewSet, ExchangeApiKeyViewSet, LedgerSortViewSet
from api.views.wallets import WalletViewSet, WalletSortViewSet, WalletTokenViewSet
from api.views.reports import ReportViewSet, SubReportViewSet, TransactionViewSet
from api.views.crypto import CryptoViewSet, DailyClosingPriceViewSet, CryptoCompareAssetsViewSet
# from api.views.reports import 


drf_router = routers.DefaultRouter()

drf_router.register(r'ledgers', LedgerViewSet, basename='ledgers')
drf_router.register(r'wallets', WalletViewSet, basename='wallets')
drf_router.register(r'exchangeAPIKeys', ExchangeApiKeyViewSet, basename='apikeys')
drf_router.register(r'ledgerSort', LedgerSortViewSet, basename='ledgerSort')
drf_router.register(r'reports', ReportViewSet, basename='reports')
drf_router.register(r'subreports', SubReportViewSet, basename='subreports')
drf_router.register(r'transactions', TransactionViewSet, basename='transactions')
drf_router.register(r'cryptos', CryptoViewSet, basename='cryptos')
drf_router.register(r'dailyClosingPrices', DailyClosingPriceViewSet, basename='dailyClosingPrices')
drf_router.register(r'walletSort', WalletSortViewSet, basename='walletSort')
drf_router.register(r'walletTokens', WalletTokenViewSet, basename='walletTokens')
drf_router.register(r'cryptoCompareAssets', CryptoCompareAssetsViewSet, basename='cryptoCompareAssets')