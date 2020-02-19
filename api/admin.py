from django.contrib import admin

# Register your models here.
from api.models import History, Crypto, Cron,Asset,Global,HistoryGlobal, Reddit, RedditHistory, Pool


class CryptoAdmin(admin.ModelAdmin):
    search_fields = ['symbol']


class AssetAdmin(admin.ModelAdmin):
    search_fields = ['symbol']

class HistoryAdmin(admin.ModelAdmin):
    search_fields = ['symbol']


class RedditHistoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(History, HistoryAdmin)
admin.site.register(Crypto, CryptoAdmin)
admin.site.register(Cron)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Global)
admin.site.register(HistoryGlobal)
