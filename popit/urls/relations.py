from django.conf.urls import url
from popit.views import *

urlpatterns = [
    url(r'^/(?P<parent>[-\w]+)/citations/(?P<field>\w+)/(?P<pk>[-\w]+)/?$',
        RelationCitationDetailView.as_view(), name="relation-citation-detail"),
    url(r'^/(?P<pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        RelationCitationListCreateView.as_view(), name="relation-citation-list"),
    url(r'^/(?P<pk>[-\w]+)/citations/?$', RelationFieldCitationView.as_view(),
        name="relation-field-citation-view"),

    url(r'^/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w]+)/?$', RelationLinkDetail.as_view(),
        name="relation-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/links/?$', RelationLinkList.as_view(),
        name="relation-link-list"),

    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/(?P<link_id>[-\w]+)/?$',
        RelationIdentifierCitationDetailView.as_view(), name="relation-identifier-citation-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        RelationIdentifierCitationListView.as_view(), name="relation-identifier-citation-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<child_pk>[-\w]+)/citations/?$',
        RelationIdentifierFieldCitationView.as_view(), name="relation-identifier-field-citation"),

    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/?$',
        RelationIdentifierLinkDetail.as_view(), name="relation-identifier-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/?$',
        RelationIdentifierLinkList.as_view(), name="relation-identifier-link-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/?$', RelationIdentifierDetail.as_view(),
        name="relation-identifier-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/?$', RelationIdentifierList.as_view(),
        name="relation-identifier-list"),

    url(r'^/(?P<pk>[-\w]+)/?$', RelationDetail.as_view(),
        name="relation-detail"),
    url(r'^/?$', RelationList.as_view(), name="relation-list"),
]
