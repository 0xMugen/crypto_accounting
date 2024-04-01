from rest_framework import serializers
from api.models import Wallets, WalletsSort, WalletToken


class WalletTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletToken
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):

    wallettoken_set = WalletTokenSerializer(many=True, read_only=True)

    class Meta:
        model = Wallets
        fields = '__all__'

class WalletSortSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletsSort
        fields = '__all__'

