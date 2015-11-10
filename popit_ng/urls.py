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
from popit.views import *


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'rosetta/', include('rosetta.urls'))
    )

api_urls = [

    url(r'^(?P<language>\w{2})/posts/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w+])/links/(?P<link_pk>[-\w]+)/$', PostContactDetailLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/posts/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w+])/links/$', PostContactDetailLinkList.as_view()),
    url(r'^(?P<language>\w{2})/posts/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w+])/$', PostContactDetailDetail.as_view()),
    url(r'^(?P<language>\w{2})/posts/(?P<parent_pk>[-\w]+)/contact_details/$', PostContactDetailList.as_view()),

    url(r'^(?P<language>\w{2})/posts/(?P<parent_pk>[-\w]+)/other_labels/(?P<pk>[-\w+])/links/(?P<link_pk>[-\w]+)/$', PostOtherLabelsLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/posts/(?P<parent_pk>[-\w]+)/other_labels/(?P<pk>[-\w+])/links/$', PostOtherLabelsLinkList.as_view()),
    url(r'^(?P<language>\w{2})/posts/(?P<parent_pk>[-\w]+)/other_labels/(?P<pk>[-\w+])/$', PostOtherLabelsDetail.as_view()),
    url(r'^(?P<language>\w{2})/posts/(?P<parent_pk>[-\w]+)/other_labels/$', PostOtherLabelsList.as_view()),

    url(r'^(?P<language>\w{2})/posts/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w+])/$', PostLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/posts/(?P<parent_pk>[-\w]+)/links/$', PostLinkList.as_view()),
    url(r'^(?P<language>\w{2})/posts/(?P<pk>[-\w]+)/$', PostDetail.as_view()),
    url(r'^(?P<language>\w{2})/posts/$', PostList.as_view()),

    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/$',
        PersonContactDetailLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/$', PersonContactDetailLinkList.as_view()),
    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/$', PersonContactDetailDetail.as_view()),
    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/contact_details/$', PersonContactDetailList.as_view()),

    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w]+)/$', PersonLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/links/$', PersonLinkList.as_view()),

    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/$',
        PersonOtherNameLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/links/$',
        PersonOtherNameLinkList.as_view()),
    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/othernames/$', PersonOtherNameList.as_view()),
    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/$', PersonOtherNameDetail.as_view()),

    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/$',
        PersonIdentifierLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/$',
        PersonIdentifierLinkList.as_view()),
    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/identifiers/$', PersonIdentifierList.as_view()),
    url(r'^(?P<language>\w{2})/persons/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/$', PersonIdentifierDetail.as_view()),

    url(r'^(?P<language>\w{2})/persons/(?P<pk>[-\w]+)/$', PersonDetail.as_view()),
    url(r'^(?P<language>\w{2})/persons/$', PersonList.as_view()),

    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/$',
        OrganizationContactDetailLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/$', OrganizationContactDetailLinkList.as_view()),
    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/$', OrganizationContactDetailDetail.as_view()),
    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/contact_details/$', OrganizationContactDetailList.as_view()),

    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w]+)/$', OrganizationLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/links/$', OrganizationLinkList.as_view()),

    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/$',
        OrganizationOtherNameLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/links/$',
        OrganizationOtherNameLinkList.as_view()),
    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/$', OrganizationOtherNameDetail.as_view()),
    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/othernames/$', OrganizationOtherNameList.as_view()),

    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/$',
        OrganizationIdentifierLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/$',
        OrganizationIdentifierLinkList.as_view()),
    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/$', OrganizationIdentifierDetail.as_view()),
    url(r'^(?P<language>\w{2})/organizations/(?P<parent_pk>[-\w]+)/identifiers/$', OrganizationIdentifierList.as_view()),

    url(r'^(?P<language>\w{2})/organizations/(?P<pk>[-\w]+)/', OrganizationDetail.as_view()),
    url(r'^(?P<language>\w{2})/organizations/$', OrganizationList.as_view()),

    url(r'^(?P<language>\w{2})/areas/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w]+)/$', AreaLinkDetail.as_view()),
    url(r'^(?P<language>\w{2})/areas/(?P<parent_pk>[-\w]+)/links/$', AreaLinkList.as_view()),
    url(r'^(?P<language>\w{2})/areas/(?P<pk>[-\w]+)/$', AreaDetail.as_view()),
    url(r'^(?P<language>\w{2})/areas/$', AreaList.as_view()),
 ]

api_urls = format_suffix_patterns(api_urls)
urlpatterns += api_urls


