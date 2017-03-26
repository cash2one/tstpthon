#-*- coding:utf-8 -*-

          #################            #
       ######################         #
      #########################      #
    ############################
   ##############################
   ###############################
  ###############################
  ##############################
                  #    ########   #
     ##        ###        ####   ##
                          ###   ###
                        ####   ###
   ####          ##########   ####
   #######################   ####
     ####################   ####
      ##################  ####
        ############      ##
           ########        ###
          #########        #####
        ############      ######
       ########      #########
         #####       ########
           ###       #########
          ######    ############
         #######################
         #   #   ###  #   #   ##
         ########################
          ##     ##   ##     ##
          
#--------------------------------------#
#         copyright  olive.fm          #
#--------------------------------------#


from django.contrib import admin
from cms.models import Site,SiteEditor,SiteAdminUser,Category,Article

def make_upshow(modeladmin, request, queryset):
    queryset.update(is_show= True)
make_upshow.short_description = "上线"

def make_downshow(modeladmin, request, queryset):
    queryset.update(is_show= False)
make_downshow.short_description = "下线"

def make_delete(modeladmin, request, queryset):
    queryset.update(enable= False)
make_delete.short_description = "不可用"

def make_nodelete(modeladmin, request, queryset):
    queryset.update(enable= True)
make_nodelete.short_description = "可用"


class SiteAdmin(admin.ModelAdmin):
    list_filter = ('enable',)
    search_fields = ['name']

class SiteEditorAdmin(admin.ModelAdmin):
    list_filter = ('site__name','enable')
    search_fields = ['name']
    list_display = ('name', 'site','enable')

class SiteAdminUserAdmin(admin.ModelAdmin):
    list_filter = ('site__name','enable')
    search_fields = ['name']
    list_display = ('name', 'site','enable')

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('site__name','enable')
    search_fields = ['name']
    list_display = ('name','parentCategory', 'site','enable','is_show')

class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('category__site__name','enable','is_show')
    search_fields = ['title', 'category']
    list_display = ('title', 'category','auther','add_time','enable','is_show')
    actions = [make_upshow,make_downshow,make_delete,make_nodelete]

admin.site.register(Site, SiteAdmin)
admin.site.register(SiteEditor, SiteEditorAdmin)
admin.site.register(SiteAdminUser, SiteAdminUserAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Article,ArticleAdmin)