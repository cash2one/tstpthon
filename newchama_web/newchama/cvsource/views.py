from django.shortcuts import render
from django.shortcuts import render,render_to_response, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count,Sum
from services.models import Member, CVSourceContact
from cvsource.models import BuyTogether,BuyEp
from django.utils import simplejson
from newchama.helper import member_login_required
from django.core.context_processors import csrf
from django.utils.translation import ugettext_lazy as _
from django.core import serializers
from django.template import RequestContext
from django.core.mail import send_mail,EmailMessage
from newchama.settings import EMAIL_HOST_USER, MEDIA_ROOT, EMAIL_CVSOURCE
from django.template import loader
from django.contrib import messages
import datetime
import logging
logger = logging.getLogger(__name__)


def rank(request):
    
    day=int(request.GET['day'])
    num=int(request.GET['num'])
    type=int(request.GET['type'])

    result={'is_ok':0,'error':''}
    member = request.session.get('member', None)

    

    start_date = datetime.datetime.now()+datetime.timedelta(days=-day)


    if member != None:

      try:
          current_member=Member.objects.get(pk=member['id'])
          temp_list1={}
          
          if type==0:
            top_list = BuyTogether.objects.exclude(cvIndustryOne=None).filter(happenDate__gt=start_date).values('cvIndustryOne').annotate(usd_all=Sum('usd')).order_by('-usd_all')[:num]

            for item in top_list:
              temp_list1[item['cvIndustryOne']]=float(item['usd_all'])
          elif type==1:
            top_list = BuyTogether.objects.exclude(epAddress1=None).filter(happenDate__gt=start_date).values('epAddress1').annotate(usd_all=Sum('usd')).order_by('-usd_all')[:num]
            for item in top_list:
              temp_list1[item['epAddress1']]=float(item['usd_all'])
          elif type==2:
            top_list = BuyTogether.objects.exclude(type=None).filter(happenDate__gt=start_date).values('type').annotate(usd_all=Sum('usd')).order_by('-usd_all')[:num]
            for item in top_list:
              temp_list1[item['type']]=float(item['usd_all'])
          else:
            temp_list1['<5 MUSB']=float(BuyTogether.objects.exclude(usd=None).filter(happenDate__gt=start_date,usd__lt=500).aggregate(Sum('usd'))['usd__sum'])
            temp_list1['5-10 MUSB']=float(BuyTogether.objects.exclude(usd=None).filter(happenDate__gt=start_date,usd__gt=500,usd__lt=1000).aggregate(Sum('usd'))['usd__sum'])
            temp_list1['10-50 MUSB']=float(BuyTogether.objects.exclude(usd=None).filter(happenDate__gt=start_date,usd__gt=1000,usd__lt=5000).aggregate(Sum('usd'))['usd__sum'])
            temp_list1['50-100 MUSB']=float(BuyTogether.objects.exclude(usd=None).filter(happenDate__gt=start_date,usd__gt=5000,usd__lt=10000).aggregate(Sum('usd'))['usd__sum'])
            temp_list1['>100 MUSB']=float(BuyTogether.objects.exclude(usd=None).filter(happenDate__gt=start_date,usd__gt=10000).aggregate(Sum('usd'))['usd__sum'])
            
          
          result['is_ok']=1
          
          result['top_list']=temp_list1
      except ObjectDoesNotExist:
          result['error']=ugettext('User is not exist!')    

    return HttpResponse(simplejson.dumps(result))


@member_login_required
def contact(request):
    c = {}
    c['title'] = _("Need More Information")
    c.update(csrf(request))
    if request.method == "POST":
        try:
            contact_email = request.POST.get("contact_email", False)
            company_name = request.POST.get("company_name", False)
            contact_name = request.POST.get("contact_name", False)
            contact_title = request.POST.get("contact_title", False)
            contact_tel = request.POST.get("contact_tel", False)
            contact_desc = request.POST.get("contact_desc", False)

            cc = CVSourceContact()
            cc.company_name = company_name
            cc.contact_name = contact_name
            cc.contact_title = contact_title
            cc.contact_tel = contact_tel
            cc.contact_email = contact_email
            cc.contact_desc = contact_desc
            cc.member_id = request.session["member"]["id"]
            cc.save()

            #TODO: send email to need more information with CVSource
            html_content = loader.render_to_string("cvsource/"+request.lang+"/email_cvsource.html",
                        {'title': _('Order from NewChama'), 'company_name': company_name, 'contact_name': contact_name, 'contact_title': contact_title, 'contact_tel': contact_tel, 'contact_desc': contact_desc, 'contact_email': contact_email})
            msg = EmailMessage(_('Order from NewChama'), html_content, EMAIL_HOST_USER, [EMAIL_CVSOURCE])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            messages.success(request, _("success"))
        except Exception, e:
            messages.error(request, e.message)

    return render_to_response("cvsource/"+request.lang+"/contact.html", c, context_instance=RequestContext(request))


def data(request):
    c = {}
    # c['title']=_("Detail")

    c['member']= request.session.get('member', None)
    return render_to_response("cvsource/"+request.lang+"/data.html", c)


def news(request):
    c = {}
    # c['title']=_("Detail")

    c['member'] = request.session.get('member', None)
    return render_to_response("cvsource/"+request.lang+"/news.html", c)