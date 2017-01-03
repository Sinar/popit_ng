from django.conf.urls import url
from popit.views import *

urlpatterns = [
    url(r'^/(?P<pk>[-\w]+)/citations/?$', PersonFieldCitationView.as_view(),
        name="person-field-citations-views"),
    url(r'^/(?P<pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        PersonCitationListCreateView.as_view(),
        name="person-citation-list-view"),
    url(r'^/(?P<parent>[-\w]+)/citations/(?P<field>\w+)/(?P<pk>[-\w]+)/?$',
        PersonCitationDetailView.as_view(), name="person-citation-detail"),

    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/(?P<link_id>[-\w]+)/?$',
        PersonContactDetailCitationDetailView.as_view(), name="person-contact-details-citations-detail-view"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        PersonContactDetailCitationListView.as_view(), name="person-contact-details-citations-view"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/?$',
        PersonContactDetailFieldCitationView.as_view(), name="person-contact-details-field-citations-view"),

    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/?$',
        PersonContactDetailLinkDetail.as_view(), name="person-contact-detail-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/?$', PersonContactDetailLinkList.as_view(),
        name="person-contact-detail-link-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/?$', PersonContactDetailDetail.as_view(),
        name="person-contact-detail-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/?$', PersonContactDetailList.as_view(),
        name="person-contact-detail-list"),

    url(r'^/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w]+)/?$', PersonLinkDetail.as_view(),
        name="person-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/links/?$', PersonLinkList.as_view(), name="person-link-list"),

    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<child_pk>[-\w]+)/citations/(?P<field>[-\w]+)/(?P<link_id>[-\w]+)/?$',
        PersonOthernameCitationDetailView.as_view(), name="person-othername-citation-detail-view"),
    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<child_pk>[-\w]+)/citations/(?P<field>[-\w]+)/?$',
        PersonOthernameCitationListView.as_view(), name="person-othername-citation-list-view"),
    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<child_pk>[-\w]+)/citations/?$',
        PersonOtherNameFieldCitationView.as_view(), name="person-othername-citation-field-view"),

    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/?$',
        PersonOtherNameLinkDetail.as_view(), name="person-othername-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/links/?$',
        PersonOtherNameLinkList.as_view(), name="person-othername-link-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/?$', PersonOtherNameDetail.as_view(),
        name="person-othername-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/othernames/?$', PersonOtherNameList.as_view(),
        name="person-othername-list"),

    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/(?P<link_id>[-\w]+)/?$',
        PersonIdentifierCitationDetailView.as_view(), name="person-identifier-citation-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        PersonIdentifierCitationListView.as_view(), name="person-identifier-citation-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<child_pk>[-\w]+)/citations/?$',
        PersonIdentifierFieldCitationView.as_view(), name="person-identifier-citation-field-view"),

    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/?$',
        PersonIdentifierLinkDetail.as_view(), name="person-identifier-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/?$',
        PersonIdentifierLinkList.as_view(), name="person-identifier-link-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/?$', PersonIdentifierDetail.as_view(),
        name="person-identifier-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/?$', PersonIdentifierList.as_view(),
        name="person-identifier-list"),

    url(r'^/(?P<pk>[-\w]+)/?$', PersonDetail.as_view(), name="person-detail"),
    url(r'^/?$', PersonList.as_view(), name="person-list"),



] 
