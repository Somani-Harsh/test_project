from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "search.views.home"),
    url(r'^get_location/',"search.views.home",name="get_location"),
    url(r'^test/',"search.utils.get_reviews_details"),
)
