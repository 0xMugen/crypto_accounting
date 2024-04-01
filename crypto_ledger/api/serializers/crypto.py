from rest_framework import serializers
from api.models import Crypto, DailyClosingPrice, CryptoCompareAssets

class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = '__all__'

class DailyClosingPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyClosingPrice
        fields = '__all__'

class CryptoCompareAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCompareAssets
        fields = '__all__'