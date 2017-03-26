import datetime
from django.db import models
from project.models import Project
from demand.models import Demand
from member.models import Member,Company
from deal.models import Deal
from news.models import News
# Create your models here.


class Message(models.Model):
    TYPES_RELATION = (
        (0, 'Normal'),
        (1, 'Project'),
        (2, 'Demand'),
    )
    sender = models.ForeignKey(Member, related_name="member_message_sender")
    receiver = models.ForeignKey(Member, related_name="member_message_receiver")
    content = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)
    is_read = models.IntegerField(default=0)
    is_delete = models.IntegerField(default=0)
    project = models.ForeignKey(Project, null=True, blank=True)
    demand = models.ForeignKey(Demand, null=True, blank=True)
    type_relation = models.IntegerField(default=0, choices=TYPES_RELATION)

    def __unicode__(self):
        return self.content

    class Meta:
        db_table = 'member_message'


class Favorites(models.Model):
    TYPES_RELATION = (
        (1, 'Project'),
        (2, 'Demand'),
        (3, 'Company'),
        (4, 'Member'),
        (5, 'Data'),
        (6, 'News'),
    )
    member = models.ForeignKey(Member)
    add_time = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, null=True, blank=True)
    demand = models.ForeignKey(Demand, null=True, blank=True)
    receiver = models.ForeignKey(Member, related_name="member_receiver_favorite", null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    news = models.ForeignKey(News, null=True, blank=True)
    data = models.ForeignKey(Deal, null=True, blank=True)
    type_relation = models.IntegerField(default=0, choices=TYPES_RELATION)

    def __unicode__(self):
        if self.project is None:
            return self.demand
        return self.project

    class Meta:
        db_table = 'member_favorites'


class EditorSay(models.Model):
    add_time = models.DateTimeField(auto_now_add=True)
    content_cn = models.TextField()
    content_en = models.TextField()

    def __unicode__(self):
        return self.content_cn

    class Meta:
        db_table = 'editorsay'


class Message_Log(models.Model):
    TYPES_RELATION = (
        (0, 'Normal'),
        (1, 'Project'),
        (2, 'Demand'),
    )
    sender = models.ForeignKey(Member, related_name="member_message_log_sender")
    receiver = models.ForeignKey(Member, related_name="member_message_log_receiver")
    message = models.ForeignKey(Message, related_name="member_message_detail")
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(default=datetime.datetime.now())
    item_type = models.IntegerField(default=0, choices=TYPES_RELATION)
    item_id = models.IntegerField(default=0)

    def __unicode__(self):
        return self.content

    class Meta:
        db_table = 'member_message_log'