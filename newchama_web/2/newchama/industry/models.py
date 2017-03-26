from django.db import models

# Create your models here.


class Industry(models.Model):
    name_cn = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    level = models.IntegerField(default=0)
    father = models.ForeignKey('self', null=True, blank=True)
    is_display = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name_en

    class Meta:
        db_table = 'industry_industry'
