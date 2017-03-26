from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=50)
    permission = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def is_has_permission(self, target_permission):
        return self.permission.find(target_permission) >= 0


class AdminUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    realname = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)
    role = models.ManyToManyField(Role)
    isactive = models.CharField(max_length=1)

    def __unicode__(self):
        return self.username

    def make_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
