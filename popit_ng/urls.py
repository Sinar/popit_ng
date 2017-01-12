"""popit_ng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/?$', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from popit.views import *
from popit_search.views import GenericSearchView
from popit_search.views import GenericRawSearchView
from popit_search.views import AdvanceSearchView
from rest_framework.authtoken import views as token_view


urlpatterns = [
    url(r'^api-token-auth/?$', token_view.obtain_auth_token),
    url(r'^admin/?', include(admin.site.urls)),
]

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'rosetta/?', include('rosetta.urls'))
    ]

if "rest_framework_docs" in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^docs/?', include('rest_framework_docs.urls')),
    ]


# TODO: the parameter in url is wrong

api_urls = [
    url(r'^rawsearch/?$', include('popit_search.urls.rawsearch')),
    url(r'^advancesearch', include('popit_search.urls.advancesearch')),
    url(r'^(?P<language>\w{2})/search', include('popit_search.urls.generic_search')),

    url(r'^(?P<language>\w{2})/posts', include('popit.urls.posts')),
    url(r'^(?P<language>\w{2})/persons', include('popit.urls.persons')),
    url(r'^(?P<language>\w{2})/organizations', include('popit.urls.organizations')),
    url(r'^(?P<language>\w{2})/memberships', include('popit.urls.memberships')),
    url(r'^(?P<language>\w{2})/areas', include('popit.urls.areas')),

    url(r'^', include('popit.urls.rooturls')),
 ]

api_urls = format_suffix_patterns(api_urls)
urlpatterns += api_urls


