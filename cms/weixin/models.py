#-*-encoding:utf-8-*-
from django.db import models

class GobalAccessToken(models.Model):
    appid = models.CharField('APP ID', max_length=255)
    access_token = models.CharField('Access Token', max_length=255, null=True, blank=True)
    access_token_expires_at = models.IntegerField('Acesss 过期时间',default=0)
    js_api_ticket =  models.CharField('JS API TICKET', max_length=255, null=True, blank=True)
    js_api_ticket_expires_at = models.IntegerField('Js api ticket 过期时间',default=0)

    def __unicode__(self):
        return self.access_token
    class Meta:
        verbose_name='微信AccessToken'
        verbose_name_plural = "微信AccessToken"