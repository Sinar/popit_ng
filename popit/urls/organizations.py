from django.conf.urls import url
from popit.views import *

urlpatterns = [
    url(r'^/(?P<parent>[-\w]+)/citations/(?P<field>\w+)/(?P<pk>[-\w]+)/?$',
        OrganizationCitationDetailView.as_view(), name="organization-citation-detail-view"),
    url(r'^/(?P<pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        OrganizationCitationListCreateView.as_view(), name="organization-citation-list-view"),
    url(r'^/(?P<pk>[-\w]+)/citations/?$', OrganizationFieldCitationView.as_view(),
        name="organization-citation-field-view"),

    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/(?P<link_id>[-\w]+)/?$',
        OrganizationContactDetailCitationDetailView.as_view(), name="organization-contact-detail-ciitation-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        OrganizationContactDetailCitationListView.as_view(), name="organization-contact-details-citation-views"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/?$',
        OrganizationContactDetailFieldCitationView.as_view(), name="organization-contact-details-field-citation"),

    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/?$',
        OrganizationContactDetailLinkDetail.as_view(), name="organization-contact-detail-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/?$', OrganizationContactDetailLinkList.as_view(),
        name="organization-contact-detail-link-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/?$', OrganizationContactDetailDetail.as_view(),
        name="organization-contact-detail-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/?$', OrganizationContactDetailList.as_view(),
        name="organization-contact-detail-list"),

    url(r'^/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w]+)/?$', OrganizationLinkDetail.as_view(),
        name="organization-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/links/?$', OrganizationLinkList.as_view(),
        name="organization-link-list"),

    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/(?P<link_id>[-\w]+)/?$',
        OrganizationOthernameCitationDetailView.as_view(), name="organization-othername-citation-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        OrganizationOthernameCitationListView.as_view(), name="organization-othername-citation-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<child_pk>[-\w]+)/citations/?$',
        OrganizationOtherNameFieldCitationView.as_view(), name="organization-othername-field-citation-view"),

    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/?$',
        OrganizationOtherNameLinkDetail.as_view(), name="organization-othername-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/links/?$',
        OrganizationOtherNameLinkList.as_view(), name="organization-othername-link-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/othernames/(?P<pk>[-\w]+)/?$', OrganizationOtherNameDetail.as_view(),
        name="organization-othername-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/othernames/?$', OrganizationOtherNameList.as_view(),
        name="organization-othername-list"),

    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/(?P<link_id>[-\w]+)/?$',
        OrganizationIdentifierCitationDetailView.as_view(), name="organization-identifier-citation-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        OrganizationIdentifierCitationListView.as_view(), name="organization-identifier-citation-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<child_pk>[-\w]+)/citations/?$',
        OrganizationIdentifierFieldCitationView.as_view(), name="organization-identifier-field-citation"),

    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/?$',
        OrganizationIdentifierLinkDetail.as_view(), name="organization-identifier-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/links/?$',
        OrganizationIdentifierLinkList.as_view(), name="organization-identifier-link-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/(?P<pk>[-\w]+)/?$', OrganizationIdentifierDetail.as_view(),
        name="organization-identifier-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/identifiers/?$', OrganizationIdentifierList.as_view(),
        name="organization-identifier-list"),

    url(r'^/(?P<pk>[-\w]+)/?$', OrganizationDetail.as_view(), name="organization-detail"),
    url(r'^/?$', OrganizationList.as_view(), name="organization-list"),

]
