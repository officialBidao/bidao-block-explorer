from django_cron import CronJobBase, Schedule
import requests
from api.models import Cron, History, Crypto, Asset,Global,HistoryGlobal, Reddit, RedditHistory
import datetime
import json
import calendar
import time
import decimal
import requests
import re
from account.models import Order, Profile
from django.utils import timezone
import datetime
from django.utils.dateparse import parse_datetime
from django.db.models import F
import json

ids = ['bitcoin', 'ethereum', 'litecoin', 'bitcoin-cash', 'monero']
avail_coins = ['BTC', 'ETH','LTC', 'BCH', 'XMR']
sym_for_coin = dict()
sym_for_coin['BTC'] = ['BTCUSDT']



class BinanceExchange():
    prices = dict()
    vols = dict()

    def update(self, symbols, coin):
        ps = []
        vs = []
        for s in symbols:
            print(s)
            response = requests.get('https://api.binance.com/api/v1/ticker/24hr?symbol='+ s)
            data = response.json()
            print(data)
            price = float(data['lastPrice'])
            vol = float(data['volume'])
            ps.append(price)
            vs.append(vol)
            print(ps)
            print(vs)
        self.prices[coin] = sum(ps) / len(ps)
        self.vols[coin] = sum(vs)

class Gecko():
    prices = dict()
    vols = dict()
    caps = dict()
    changes = dict()

    def update(self, ids, coins):
        strids = ','.join(ids)
        response =requests.get('https://api.coingecko.com/api/v3/simple/price?ids='+ strids + '&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true')
        data = response.json()
        print(data)
        for i in range(0,len(ids)):
            price = float(data[ids[i]]['usd'])
            vol = float(data[ids[i]]['usd_24h_vol'])
            change = float(data[ids[i]]['usd_24h_change'])
            cap = float(data[ids[i]]['usd_market_cap'])
            if cap == 0:
                try:
                    print('cap is 0' + coins[i])
                    c = Crypto.objects.get(symbol=coins[i])
                    if c is not None:
                        cap = price * float(c.circ_supply)
                        print(cap)
                    else:
                        print('None')
                except:
                    pass
            self.prices[coins[i]] = price
            self.vols[coins[i]] = vol
            self.caps[coins[i]] = cap
            self.changes[coins[i]] = change

binance = BinanceExchange()
gecko = Gecko()




def update_prices_for_symbols(symbols, coin):
    binance.update(symbols,coin)
    c = Crypto.objects.get(symbol=coin)
    c.price = binance.prices[coin]
    c.vol = binance.vols[coin]
    c.marketcap = c.price * c.circ_supply
    c.save()

def update_global_data():
    print('updating global data')
    response = requests.get('https://api.coingecko.com/api/v3/global')
    data = response.json()
    globaldata = Global.objects.all()[0]
    coins = Crypto.objects.all().filter(type='s')
    print('here global')
    stakedcap = 0
    capofallstakingcoins = 0
    for c in coins:
        capofallstakingcoins = capofallstakingcoins + c.marketcap
        print(c.info['staked'])
        stakedcap = stakedcap + c.info['staked'] * c.price
        print('here again')

    print('here again')
    globaldata.marketcap = data['data']['total_market_cap']['usd']
    globaldata.vol = data['data']['total_volume']['usd']

    globaldata.capofallstakingcoins = capofallstakingcoins
    globaldata.stakedcap = stakedcap
    globaldata.capchange =data['data']['market_cap_change_percentage_24h_usd']
    globaldata.save()


def update_prices_for_symbols_gecko(ids, coins):
    gecko.update(ids,coins)
    for coin in coins:
        print(coin)
        try:
            c = Crypto.objects.get(symbol=coin)
            c.price = gecko.prices[coin]
            c.vol = gecko.vols[coin]
            c.marketcap = gecko.caps[coin]
            c.dchange = gecko.changes[coin]
            c.save()
        except:
            print(coin + ' not in DB')

def update_global_histories():
    h = HistoryGlobal.objects.all()[0]
    g = Global.objects.all()[0]
    h.marketcap.append(float(g.marketcap))
    h.vol.append(float(g.vol))
    h.capofallstakingcoins.append(float(g.capofallstakingcoins))
    h.stakedcap.append(float(g.stakedcap))
    ts = calendar.timegm(time.gmtime())
    h.date.append(ts)
    print('here')
    h.save()

def update_crypto_histories(symbol):
    h = History.objects.get(symbol=symbol)
    c = Crypto.objects.get(symbol=symbol)
    h.price.append(float(c.price))
    print(float(c.price))
    h.vol.append(float(c.vol))
    h.marketcap.append(float(c.price * c.circ_supply))
    ts = calendar.timegm(time.gmtime())
    h.date.append(ts)
    print('here')
    h.save()

def update_asset_histories(symbol):
    h = History.objects.get(symbol=symbol)
    c = Asset.objects.get(symbol=symbol)
    h.price.append(float(c.price))
    price = c.price
    if symbol == 'GOLD':
        price = float(c.price) / 28.3495  #price per gram
    print(price)
    h.marketcap.append(price * float(c.supply))
    ts = calendar.timegm(time.gmtime())
    h.date.append(ts)
    h.save()



def update_bitcoin_circ_supply():
     response = requests.get('https://blockchain.info/q/totalbc')
     data = response.text
     print(data)
     supply = int(data) / 100000000
     print(supply)
     c = Crypto.objects.get(symbol='BTC')
     c.circ_supply = supply
     c.save()


def update_prices(coin, symbols):
        update_bitcoin_circ_supply()
        update_prices_for_symbols(symbols, coin)


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)



class UpdateCryptoPricesCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.tasks.update_prices_for_symbols'    # a unique code

    def do(self):
        print("cron for crypto prices update started")
        update_prices_for_symbols_gecko(ids, avail_coins)
        for c in avail_coins:
            print('updating ' + c)
            update_prices(c, sym_for_coin[c])

class UpdateCryptoHistoryCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.tasks.update_history_for_symbols'    # a unique code

    def do(self):
        print("cron for crypto history update started")
        for c in avail_coins:
            print('updating ' + c)
            try:
                update_crypto_histories(c)
            except:
                print(c + " not in DB")


class UpdateAssetHistoryCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.tasks.update_history_for_assets'    # a unique code

    def do(self):
        print("cron for asset history update started")
        for c in avail_assets:
            print('updating ' + c)
            update_asset_histories(c)


class UpdateGlobal(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    SECS = RUN_EVERY_MINS * 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.tasks.update_global'    # a unique code

    def do(self):
        print("cron for crypto gold  update started")
        update_global_data()
        update_global_histories()

class UpdateReddit(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    SECS = RUN_EVERY_MINS * 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.tasks.update_reddit'    # a unique code

    def do(self):
        print("cron for reddit  update started")
        for r in subreddits:
            print('updating ' + r)
            try:
                update_reddit(r)
            except:
                print(r + ' not in DB')

class UpdateRedditHistory(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    SECS = RUN_EVERY_MINS * 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api.tasks.update_reddit_histories'    # a unique code

    def do(self):
        print("cron for reddit history update started")
        for r in subreddits:
            try:
                print('updating ' + r)
                update_reddit_histories(r)
            except:
                print(r + ' not in db')
