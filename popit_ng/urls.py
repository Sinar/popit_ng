"""popit_ng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from popit.views import PersonDetail
from popit.views import PersonList
from popit.views import PersonContactDetail
from popit.views import PersonContactList
from popit.views import PersonLinkDetail
from popit.views import PersonLinkList
from popit.views import PersonOtherNameDetail
from popit.views import PersonOtherNameList
from popit.views import PersonIdentifierDetail
from popit.views import PersonIdentifierList
from popit.views import PersonIdentifierLinkDetail
from popit.views import PersonIdentifierLinkList
from popit.views import PersonContactLinkDetail
from popit.views import PersonContactLinkList
from popit.views import PersonOtherNameLinkDetail
from popit.views import PersonOtherNameLinkList

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'rosetta/', include('rosetta.urls'))
    )

api_urls = [
    url(r'^(?P<language>\w+)/persons/$', PersonList.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<pk>[-\w]+)/$', PersonDetail.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/contacts/$', PersonContactList.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/contacts/(?P<pk>[-\w]+)/$', PersonContactDetail.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/links/$', PersonLinkList.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w]+)/$', PersonLinkDetail.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/othernames/$', PersonOtherNameList.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/$', PersonOtherNameDetail.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/identifiers/$', PersonIdentifierList.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/$', PersonIdentifierDetail.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/contacts/(?P<pk>[-\w]+)/links/$', PersonContactLinkList.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/contacts/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/$',
        PersonContactLinkDetail.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/links/$',
        PersonOtherNameLinkList.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/$',
        PersonOtherNameLinkDetail.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/$',
        PersonIdentifierLinkList.as_view()),
    url(r'^(?P<language>\w+)/persons/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/$',
        PersonIdentifierLinkDetail.as_view()),
 ]

api_urls = format_suffix_patterns(api_urls)
urlpatterns += api_urls


