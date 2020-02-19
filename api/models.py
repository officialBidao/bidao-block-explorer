from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.


class CryptoManager(models.Manager):
    def get_by_natural_key(self, symbol):
        return self.get(symbol=symbol)

class Crypto(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    total_supply = models.BigIntegerField()
    circ_supply = models.BigIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=8)
    vol = models.DecimalField(max_digits=20, decimal_places=3, null =True)
    marketcap = models.DecimalField(max_digits=30, decimal_places=8,null = True)
    dchange = models.DecimalField(max_digits=5, decimal_places=3, null= True)
    type = models.CharField(max_length=30, null=True)
    info = JSONField(null=True)
    likes = models.BigIntegerField(default = 1)
    faq = models.TextField(null = True)

    objects = CryptoManager()

    class Meta:
        unique_together = [['symbol']]

    def natural_key(self):
        return (self.symbol)


class History(models.Model):
    price = JSONField()
    date = JSONField()
    marketcap = JSONField()
    vol = JSONField(null=True)
    symbol = models.CharField(max_length=10)

class Asset(models.Model):
    symbol = models.CharField(max_length=100)
    price =  models.DecimalField(max_digits=10, decimal_places=3)
    supply =  models.DecimalField(max_digits=50, decimal_places=3)
    marketcap =  models.DecimalField(max_digits=50, decimal_places=3)
    dchange = models.DecimalField(max_digits=5, decimal_places=3, null=True)

class Cron(models.Model):
     time =models.CharField(max_length=100)

class HistoryGlobal(models.Model):
    marketcap = JSONField()
    stakedcap = JSONField()
    capofallstakingcoins = JSONField()
    vol = JSONField()
    date = JSONField()

class Global(models.Model):
    vol = models.DecimalField(max_digits=20, decimal_places=3, null =True)
    marketcap = models.DecimalField(max_digits=20, decimal_places=3,null = True)
    stakedcap = models.DecimalField(max_digits=20,decimal_places=3,null = True)
    capofallstakingcoins = models.DecimalField(max_digits=20,decimal_places=3,null = True)
    btcdominance = models.DecimalField(max_digits=20,decimal_places=3, null =True)
    capchange = models.DecimalField(max_digits=20, decimal_places=3, null =True)
