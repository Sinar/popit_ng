from django.conf.urls import url
from popit.views import *

urlpatterns = [
    url(r'^/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w]+)/?$', AreaLinkDetail.as_view(),
        name="area-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/links/?$', AreaLinkList.as_view(), name="area-link-list"),
    url(r'^/(?P<pk>[-\w]+)/?$', AreaDetail.as_view(), name="area-detail"),
    url(r'^/?$', AreaList.as_view(), name="area-list"),


]
