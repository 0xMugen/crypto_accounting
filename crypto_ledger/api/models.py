from django.db import models
from api.base_models import TimeStampedModel, UUIDModel

from accounts.models import User, UserProfile

from django.forms.models import model_to_dict
import pandas as pd

BLOCKCHAIN_CHOICE = (
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
    ('MATIC', 'Polygon'),
)

ASSET_CHOICE = (
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
    ('MATIC', 'Polygon'),
    ('USDT', 'Tether'),
    ('USDC', 'USD Coin'),
    ('BNB', 'Binance Coin'),
    ('ADA', 'Cardano'),
    ('DOGE', 'Dogecoin'),
    ('DOT', 'Polkadot'),
    ('UNI', 'Uniswap'),
    ('LINK', 'Chainlink'),
    ('LTC', 'Litecoin'),
    ('BCH', 'Bitcoin Cash'),
    ('SOL', 'Solana'),
    ('XLM', 'Stellar'),
    ('MATIC', 'Polygon'),
)

CURRENCY_CHOICE = (
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
)

EXCHANGE_CHOICE = (
    ('BINANCE', 'Binance'),
    ('KRAKEN', 'Kraken'),
    ('COINBASE', 'Coinbase'),
)

TX_TYPE_CHOICE = (
    ('INNER', 'Inner'),
    ('OUTER', 'Outer'),
    ('INTERNAL', 'Internal'),
)

class CryptoCompareAssets(TimeStampedModel):
    asset_name = models.CharField(max_length=20, unique=True)
    asset_symbol = models.CharField(max_length=20, unique=True)
    blockchain = models.CharField(max_length=20, null=True, blank=True)
    contract_address = models.TextField(null=True, blank=True)


class Wallets(UUIDModel):

    name = models.CharField(max_length=20)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    blockchain = models.CharField(max_length=8, choices=BLOCKCHAIN_CHOICE)
    address = models.CharField(max_length=42)

    def __str__(self):
        return self.address
    
class WalletToken(UUIDModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)
    contract_address = models.CharField(max_length=66, null=True, blank=True)
    count = models.IntegerField(default=0)
    is_asset_price = models.BooleanField(default=False)


class WalletsSort(UUIDModel):
    wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    contract_address = models.CharField(max_length=66, null=True, blank=True)

    blockchain = models.CharField(max_length=8, choices=BLOCKCHAIN_CHOICE)
    block_number = models.IntegerField()
    source = models.CharField(max_length=42)
    time = models.DateTimeField()
    amount = models.DecimalField(max_digits=30, decimal_places=18)
    isError = models.BooleanField(default=False)
    gasfee = models.DecimalField(max_digits=38, decimal_places=20, null=True, blank=True)
    gas = models.IntegerField(null=True, blank=True)
    sender = models.CharField(max_length=42, null=True, blank=True)
    receiver = models.CharField(max_length=42, null=True, blank=True)
    hash = models.CharField(max_length=66, null=True, blank=True)
    token_name = models.CharField(max_length=30, null=True, blank=True)
    token_symbol = models.CharField(max_length=30, null=True, blank=True)
    token_decimal = models.IntegerField(null=True, blank=True)
    exchange = models.CharField(max_length=20, null=True, blank=True)

    def to_dataframe(self):
        wallet_dict = model_to_dict(self)
        df = pd.DataFrame([wallet_dict])

        return df



class ExchangeAPIKey(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICE)

    api_key = models.CharField(max_length=500)
    api_secret = models.CharField(max_length=500)

    class Meta:
        verbose_name = "User API Key"
        verbose_name_plural = "User API Keys"

    def __str__(self):
        return self.user.username


class Ledgers(UUIDModel):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICE)
    file = models.FileField(upload_to='ledgers/', null=True, blank=True)
    api_key = models.ForeignKey(ExchangeAPIKey, null=True, blank=True ,on_delete=models.CASCADE, related_name='ledgers')

    def __str__(self):
        return f"{self.exchange} - {self.ledger.name}"

        
class LedgerSort(UUIDModel):
    ledger = models.ForeignKey(Ledgers, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    refid = models.CharField(max_length=25)

    source = models.CharField(max_length=42)
    time = models.DateTimeField()
    asset = models.CharField(max_length=20)
    transaction_type = models.CharField(max_length=20)
    fee = models.DecimalField(max_digits=23, decimal_places=18)
    balance = models.DecimalField(max_digits=23, decimal_places=18)
    amount = models.DecimalField(max_digits=23, decimal_places=18)

    def to_dataframe(self):
        ledger_dict = model_to_dict(self)
        df = pd.DataFrame([ledger_dict])

        return df

    
class Reports(UUIDModel):

    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('done', 'Done'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='pending')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    wallets = models.ManyToManyField(Wallets)
    ledgers = models.ManyToManyField(Ledgers)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICE)
    report = models.FileField(upload_to='reports/', null=True, blank=True)

class SubReports(UUIDModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    token = models.CharField(max_length=8, choices=ASSET_CHOICE)


class Transactions(UUIDModel):
    #header

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    sub_report = models.ForeignKey(SubReports, on_delete=models.CASCADE, null=True, blank=True)
    order = models.PositiveIntegerField()
    blockchain = models.CharField(max_length=8, choices=BLOCKCHAIN_CHOICE, null=True, blank=True)
    source = models.CharField(max_length=42)
    exchange = models.CharField(max_length=20, null=True, blank=True)

    #exchange
    ledger = models.ForeignKey(Ledgers ,on_delete=models.PROTECT, null=True, blank=True)
    asset = models.CharField(max_length=30, null=True, blank=True)
    fee = models.DecimalField(max_digits=30, decimal_places=18, null=True, blank=True)
    refid = models.CharField(max_length=25, null=True, blank=True)

    #blockexplorer
    isError = models.BooleanField(default=False)
    gas = models.IntegerField(null=True, blank=True)
    gasfee = models.DecimalField(max_digits=38, decimal_places=20, null=True, blank=True)
    gasToCurrency = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    contract_address = models.CharField(max_length=66, null=True, blank=True)
    
    asset_price = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    original_asset_price = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    average_buy_price = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    appreciation = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    sender = models.CharField(max_length=42, null=True, blank=True)
    receiver = models.CharField(max_length=42, null=True, blank=True)
    hash = models.CharField(max_length=66, null=True, blank=True)
    block_number = models.IntegerField(null=True, blank=True)
    tx_type = models.CharField(max_length=30, choices=TX_TYPE_CHOICE, null=True, blank=True)
    is_transfer = models.BooleanField(default=False)

    #both
    time = models.DateTimeField()
    amount = models.DecimalField(max_digits=38, decimal_places=20)
    balance = models.DecimalField(max_digits=38, decimal_places=20, null=True, blank=True)
    total_balance = models.DecimalField(max_digits=38, decimal_places=20, null=True, blank=True)
    transaction_type = models.CharField(max_length=30, null=True, blank=True)

    is_erc = models.BooleanField(default=False)
    token_name = models.CharField(max_length=30, null=True, blank=True)
    token_symbol = models.CharField(max_length=30, null=True, blank=True)
    token_decimal = models.IntegerField(null=True, blank=True)


    def to_dataframe(self):
        ledger_dict = model_to_dict(self)
        df = pd.DataFrame([ledger_dict])
        return df

class TransactionExchangeBalance(TimeStampedModel):
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICE)
    balance = models.DecimalField(max_digits=20, decimal_places=18)


class Crypto(TimeStampedModel):
    name = models.CharField(max_length=20, choices=ASSET_CHOICE, unique=True)


class DailyClosingPrice(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    date = models.DateField()
    closing_price = models.DecimalField(max_digits=30, decimal_places=2)

    class Meta:
        verbose_name = "Daily Closing Price"
        verbose_name_plural = "Daily Closing Prices"
        unique_together = ('crypto', 'date')

    def __str__(self):
        return f"{self.crypto.name} - {self.date}"
