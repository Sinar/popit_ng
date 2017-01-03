from django.conf.urls import url
from popit.views import *

urlpatterns = [
    url(r'^/(?P<parent>[-\w]+)/citations/(?P<field>\w+)/(?P<pk>[-\w]+)/?$',
        MembershipCitationDetailView.as_view(), name="membership-citation-detail"),
    url(r'^/(?P<pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        MembershipCitationListCreateView.as_view(), name="membership-citation-list"),
    url(r'^/(?P<pk>[-\w]+)/citations/?$', MembershipFieldCitationView.as_view(),
        name="membership-field-citation-view"),

    url(
        r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/(?P<link_id>[-\w]+)/?$',
        MembershipContactDetailCitationDetailView.as_view(), name="membership-contact-detail-citation-detail"
    ),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        MembershipContactDetailCitationListView.as_view(), name="membership-contact-detaion-citation-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/?$',
        MembershipContactDetailFieldCitationView.as_view(), name="membership-contact-detail-field-citation"),

    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/?$',
        MembershipContactDetailLinkDetail.as_view(), name="membership-contact-detail-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/?$', MembershipContactDetailLinkList.as_view(),
        name="membership-contact-detail-link-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/?$', MembershipContactDetailDetail.as_view(),
        name="membership-contact-detail-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/?$', MembershipContactDetailList.as_view(),
        name="membership-contact-detail-list"),

    url(r'^/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w]+)/?$', MembershipLinkDetail.as_view(),
        name="membership-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/links/?$', MembershipLinkList.as_view(),
        name="membership-link-list"),
    url(r'^/(?P<pk>[-\w]+)/?$', MembershipDetail.as_view(),
        name="membership-detail"),
    url(r'^/?$', MembershipList.as_view(), name="membership-list"),
]
