#coding:utf-8
#coding:gbk
#from django.contrib.auth.models import User,Group
from log.models import Log
from services.models import Member,Project,Country,Demand,ProjectAttach, RecommondItem, ProjectTargetCompanyDetail, \
    Company, DTOTimeline, Favorites, ProjectKeyword, Industry, ProjectTag, StockStructure
from rest_framework import serializers

class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ()
'''
class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ()#'password','mobile','first_name','company','companyType')

class Get_Valid_Code_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ()


'''

class Get_Dynamic_Msg_ListSerializer(serializers.Serializer):
    member_id = serializers.IntegerField()
    member_realname = serializers.CharField()
    member_avatar = serializers.CharField()
    member_link = serializers.CharField()
    content_link = serializers.CharField()
    content_cn_start = serializers.CharField()
    content_cn = serializers.CharField()
    content_cn_end = serializers.CharField()
    content_en_start = serializers.CharField()
    content_en = serializers.CharField()
    content_en_end = serializers.CharField()
    addtime = serializers.DateTimeField()
    member_company = serializers.CharField()
    member_title = serializers.CharField()
    project_id = serializers.IntegerField()
    content_type = serializers.IntegerField()


class Get_User_Detail_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ('fullname','position_cn','companyNameCn','avatar',)#'member_focus_aspect',)

class Get_User_Publish_Pro_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name_cn','status','is_anonymous','add_time','expire_date','pv','favorite_times','message_times')

class Get_User_Care_Pro_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorites
        fields = ('user_fav_pro_name','user_fav_pro_status','user_fav_pro_add_time','user_fav_pro_expire_date','user_fav_pro_pv','user_fav_pro_favorite_times','user_fav_pro_message_times',)

class Get_User_Care_Member_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorites
        fields = ('user_fav_member_name','user_fav_member_image')

class Get_Pro_Detail_Serializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = Project
        fields = ('member_avatar','name_cn','status','is_anonymous','add_time','expire_date','member_name','member_job_title','company_name_cn','companyIndustry','companyCountry','companyProvince','companyCity','new_employees_count_type','currency_type_financial','expected_enterprice_value','stock_percent','deal_size','income','income_last_phase_2','income_last_phase_3','profit','profit_last_phase_2','profit_last_phase_3','ebitda','ebitda_2','ebitda_3','audit_status','audit_status_2','audit_status_3','pv','favorite_times','message_times','features_cn','company_stock_symbol',)

class Get_Pro_Detail_Tag_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectTag
        fields =('tag',)

class Get_Pro_Keywords_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectKeyword
        fields =('keyword',)

class Get_Pro_Stock_Structure_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StockStructure
        fields =('rate',)

class Get_Pro_List_Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ('id','member_avatar','member_name','company_name_cn','member_job_title','company_tag','name_cn','companyIndustry','pv','favorite_times','message_times','expected_enterprice_value','stock_percent')

class Get_Demand_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Demand
        fields = ('member_avatar','member_name','company_name','member_job_title','name_cn','companyIndustry','pv','favorite_times','message_times','expected_enterprice_value','stock_percent')

class Get_Target_Pro_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('member_avatar','member_name','company_name_cn','member_job_title','name_cn','companyIndustry','pv','favorite_times','message_times','expected_enterprice_value','stock_percent')

class Get_Target_Demand_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Demand
        fields = ('member_avatar','member_name','company_name','member_job_title','name_cn','companyIndustry','pv','favorite_times','message_times','expected_enterprice_value','stock_percent')

class Get_Keyword_Search_Pro_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectKeyword
        fields = ('company_tag','member_avatar','member_name','company_name','member_job_title','project_name','company_industry','pv','favorite_times','message_times','expected_enterprice_value','stock_percent')

class Define_Pro_Not_Proper_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ()

class Get_Pro_Msg_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorites
        fields = ('user_fav_member_name','user_fav_member_company_name')

class Get_Friends_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorites
        fields = ('user_fav_member_name','user_fav_member_company_name')

class Get_Pro_Teaser_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name_cn','status','is_anonymous','add_time','expire_date',)

class Get_Upload_File_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name_cn','upload_file',)

class Get_Personal_Detail_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ('fullname','position_cn','companyNameCn','avatar','member_focus_aspect',)

class Get_Personal_Publish_Pro_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name_cn','status','is_anonymous','add_time','expire_date','pv','favorite_times','message_times')

class Get_Personal_Care_Pro_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorites
        fields = ('user_fav_pro_name','user_fav_pro_status','user_fav_pro_add_time','user_fav_pro_expire_date','user_fav_pro_pv','user_fav_pro_favorite_times','user_fav_pro_message_times',)

class Get_Personal_Company_Detail_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ('companyNameCn','company_address','company_website','company_introduction_cn')

class Genius_Company_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecommondItem
        fields = ('companyName','companyAddress','companyWebsite','target_reason_cn',)

class Genius_Get_Filter_Buyer_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecommondItem
        fields = ('companyName','companyAddress','companyWebsite','target_reason_cn',)

class Get_Controlboard_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectTargetCompanyDetail
        fields = ('companyName','status')

class Get_Controlboard_Recent_View_Pro_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ('user_name','user_image')

class Get_Controlboard_Recent_Focus_Pro_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ('user_name','user_image')

class Controlboard_Company_Operation_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectTargetCompanyDetail
        fields = ('companyName','status')

class Get_Newbuyer_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('name_cn','address_cn','website',)

class Get_Focus_Aspect_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Industry
        fields = ('name_cn',)

class Get_Hot_Tag_List_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectTag
        fields = ('tag',)

class Get_Member_In_Same_Company_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ('fullname','avatar',)