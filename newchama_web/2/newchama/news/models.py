from django.db import models
import datetime
# Create your models here.
class News(models.Model):
    
    title =  models.CharField(max_length=200, blank=True, null=True)
    content =  models.TextField(blank=True, null=True)
    tag =  models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'cvsource_news'

   