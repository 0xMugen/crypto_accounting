from rest_framework import serializers

from api.models import Reports, Transactions, TransactionExchangeBalance, SubReports, Wallets, Ledgers
from api.serializers.ledgers import LedgerSerializer
from api.serializers.wallets import WalletSerializer


class SubReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubReports
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    wallets = serializers.PrimaryKeyRelatedField(queryset=Wallets.objects.all(), many=True, write_only=True)
    ledgers = serializers.PrimaryKeyRelatedField(queryset=Ledgers.objects.all(), many=True, write_only=True)
    SubReports = SubReportSerializer(many=True, read_only=True)

    class Meta:
        model = Reports
        fields = ['id', 'user', 'name', 'wallets', 'ledgers', 'currency', 'report', 'SubReports', 'start_date', 'end_date', 'status']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['wallets'] = WalletSerializer(instance.wallets.all(), many=True).data
        representation['ledgers'] = LedgerSerializer(instance.ledgers.all(), many=True).data
        return representation

class SubReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubReports
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'

class TransactionExchangeBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionExchangeBalance
        fields = '__all__'

    