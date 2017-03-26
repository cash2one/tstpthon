from django.db import models

# Create your models here.


class Continent(models.Model):
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'area_continent'


class Country(models.Model):
    continent = models.ForeignKey(Continent)
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)
    intel_code = models.CharField(max_length=10, null=True)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'area_country'


class Province(models.Model):
    country = models.ForeignKey(Country)
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'area_province'


class City(models.Model):
    province = models.ForeignKey(Province)
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'area_city'


class RegionLevelOne(models.Model):
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name_cn

    class Meta:
        db_table = 'area_regionlevelone'


class RegionLevelTwo(models.Model):
    parent = models.ForeignKey(RegionLevelOne)
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name_cn

    class Meta:
        db_table = 'area_regionleveltwo'


class RegionLevelThree(models.Model):
    parent = models.ForeignKey(RegionLevelTwo)
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)
    sort = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name_cn

    class Meta:
        db_table = 'area_regionlevelthree'

