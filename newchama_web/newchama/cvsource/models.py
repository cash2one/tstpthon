from django.db import models

# Create your models here.
class BuyTogether(models.Model):
    
    tBuyID = models.IntegerField(primary_key=True)
    cnName = models.CharField(max_length=200, blank=True, null=True)
    usd = models.DecimalField(max_digits=19, decimal_places=6, null=True)
    money = models.DecimalField(max_digits=19, decimal_places=6, null=True)
    currency = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    tBuyWay = models.CharField(max_length=20, blank=True, null=True)
    attitudeName = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    happenDate = models.DateTimeField(null=True)
    endDate = models.DateTimeField(null=True)
    dstrict = models.BooleanField(default=0)
    whetherTrade = models.BooleanField(default=0)
    stockRightPercent = models.FloatField(blank=True, null=True)
    desc = models.CharField(max_length=2000, blank=True, null=True)
    payStyle = models.CharField(max_length=20, blank=True, null=True)
    cvIndustryOne = models.CharField(max_length=20, blank=True, null=True)
    cvIndustryTwo = models.CharField(max_length=20, blank=True, null=True)
    cvIndustryThree = models.CharField(max_length=20, blank=True, null=True)
    gbIndustryOne = models.CharField(max_length=20, blank=True, null=True)
    gbIndustryTwo = models.CharField(max_length=20, blank=True, null=True)
    gbIndustryThree = models.CharField(max_length=20, blank=True, null=True)
    gbIndustryFour = models.CharField(max_length=20, blank=True, null=True)
    swIndustryOne = models.CharField(max_length=20, blank=True, null=True)
    swIndustryTwo = models.CharField(max_length=20, blank=True, null=True)
    swIndustryThree = models.CharField(max_length=20, blank=True, null=True)
    zjIndustryOne = models.CharField(max_length=20, blank=True, null=True)
    zjIndustryTwo = models.CharField(max_length=20, blank=True, null=True)
    zjIndustryThree = models.CharField(max_length=20, blank=True, null=True)
    zjIndustryFour = models.CharField(max_length=20, blank=True, null=True)
    epCnName =  models.CharField(max_length=100, blank=True, null=True)
    epCnShortName =  models.CharField(max_length=50, blank=True, null=True)
    epEnName =  models.CharField(max_length=100, blank=True, null=True)
    epEnShortName =  models.CharField(max_length=50, blank=True, null=True)
    epAddress1 = models.CharField(max_length=200, blank=True, null=True)
    epAddress2 = models.CharField(max_length=200, blank=True, null=True)
    epAddress3 = models.CharField(max_length=200, blank=True, null=True)
    epAddress4 = models.CharField(max_length=200, blank=True, null=True)
    epAddress5 = models.CharField(max_length=200, blank=True, null=True)
    addTime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "[BuyID:%d] %s" % (self.tBuyID,self.cnName)

    class Meta:
        db_table = 'cvsource_buytogether'


class BuyEp(models.Model):
    buyTogether = models.ForeignKey('BuyTogether')
    cnName =  models.CharField(max_length=100, blank=True, null=True)
    cnShortName =  models.CharField(max_length=50, blank=True, null=True)
    enName =  models.CharField(max_length=100, blank=True, null=True)
    enShortName = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.cnShortName

    class Meta:
        db_table = 'cvsource_buyep'

   

