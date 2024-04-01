from rest_framework import serializers
from django.core import signing


from api.models import Ledgers, Wallets, ExchangeAPIKey, LedgerSort


class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledgers
        fields = '__all__'
        read_only_fields = ('ledger_id',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('file')
        return ret

class LedgerSortSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerSort
        fields = '__all__'



class ExchangeApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeAPIKey
        fields = '__all__'