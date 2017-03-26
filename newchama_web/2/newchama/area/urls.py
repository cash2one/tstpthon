from django.conf.urls import patterns, include, url
from area import views

urlpatterns = patterns('',
    url(r'^get_provinces/(\d+)', views.get_provinces, name='area.get_provinces'),
    url(r'^get_cities/(\d+)', views.get_cities, name='area.get_cities'),
    url(r'^get_regionleveltwo/(\d+)', views.get_regionleveltwo, name='area.get_regionleveltwo'),
    url(r'^get_regionlevelthree/(\d+)', views.get_regionlevelthree, name='area.get_regionlevelthree'),
)

