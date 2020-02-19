from rest_framework import viewsets
from api.models import Asset, Crypto, History, Global, Reddit, Pool
from api.serializers import CryptoSerializer,HistorySerializer,AssetSerializer, GlobalSerializer,RedditSerializer, PoolSerializer
from api.tasks import update_prices_for_symbols,update_bitcoin_circ_supply
from rest_framework.decorators import api_view
import time
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.serializers import serialize


@api_view(['GET'])
def update_prices(request):
    """
    List all code snippets, or create a new snippet.
    """
    INTERVALL = 60
    if request.method == 'GET':
        while True:
            update_bitcoin_circ_supply()
            update_prices_for_symbols(['BTCUSDT'], 'BTC')
            time.sleep(INTERVALL)
        return Response(serializer.data)


@api_view(['GET'])
def get_crypto(request, symbol):
    """
    List all code snippets, or create a new snippet.
    """
    serializer = CryptoSerializer
    if request.method == 'GET':
        c = Crypto.objects.get(symbol=symbol)
        serializer = CryptoSerializer(c)
        return Response(serializer.data)

@api_view(['GET'])
def get_symbols(request):

    if request.method == 'GET':
        s = list(Crypto.objects.all().values_list('symbol', flat=True))
        return JsonResponse(s, safe=False)

@api_view(['GET'])
def get_marketcap(request):

    if request.method == 'GET':
        s = list(Crypto.objects.filter(type='s').order_by('marketcap').values_list('symbol',flat=True))
        m = list(Crypto.objects.filter(type='s').order_by('marketcap').values_list('marketcap', flat=True))
        return JsonResponse({'symbol': s, 'marketcap': m}, safe=False)



@api_view(['GET'])
def get_global(request):
    """
    List all code snippets, or create a new snippet.
    """
    serializer = GlobalSerializer
    if request.method == 'GET':
        c = Global.objects.all()[0]
        serializer = GlobalSerializer(c)
        return Response(serializer.data)


@api_view(['GET'])
def get_recent_history(request, symbol):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        c = History.objects.get(symbol=symbol)
        c.price = c.price[-10:]
        c.date = c.date[-10:]
        c.marketcap = c.marketcap[-10:]
        c.vol = c.vol[-10:]
        serializer = HistorySerializer(c)
        return Response(serializer.data)

@api_view(['GET'])
def get_asset(request, symbol):
    """
    List all code snippets, or create a new snippet.
    """
    serializer = AssetSerializer
    if request.method == 'GET':
        c = Asset.objects.get(symbol=symbol)
        serializer = AssetSerializer(c)
        return Response(serializer.data)

class CryptoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer


class HistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = History.objects.all()
    serializer_class = HistorySerializer

@api_view(['GET'])
def get_reddit(request):
    """
    List all code snippets, or create a new snippet.
    """
    serializer = RedditSerializer
    if request.method == 'GET':
        c = Reddit.objects.all().order_by('-subs')
        serializer = RedditSerializer(c, many=True)
        return Response(serializer.data)
