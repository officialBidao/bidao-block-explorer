from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Crypto, History, Asset, Global


class CryptoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crypto
        fields=('name','symbol','total_supply','circ_supply','price','marketcap','dchange','info','type','vol', 'likes', 'faq')


class CryptoSerializerBasic(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crypto
        fields =('name','symbol')


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ('symbol', 'supply', 'price', 'marketcap', 'dchange')


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = History
        fields = ('symbol', 'price', 'date', 'marketcap')

class GlobalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Global
        fields = ('marketcap', 'vol', 'stakedcap',
                  'capofallstakingcoins', 'btcdominance', 'capchange')

