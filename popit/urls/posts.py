from django.conf.urls import url
from popit.views import *

urlpatterns = [
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/(?P<link_id>\w+)/?$',
        PostContactDetailCitationDetailView.as_view(), name="post-contact-detail-citation-detail-view"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        PostContactDetailCitationListView.as_view(), name="post-contact-detail-citation-list-views"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<child_pk>[-\w]+)/citations/?$',
        PostContactDetailFieldCitationView.as_view(), name="post-contact-detail-field-citation-views"),

    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/?$',
        PostContactDetailLinkDetail.as_view(), name="post-contact-detail-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/links/?$',
        PostContactDetailLinkList.as_view(), name="post-contact-detail-link-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/(?P<pk>[-\w]+)/?$',
        PostContactDetailDetail.as_view(), name="post-contact-detail-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/contact_details/?$', PostContactDetailList.as_view(),
        name="post-contact-detail-list"),

    url(r'^/(?P<parent_pk>[-\w]+)/other_labels/(?P<child_pk>[-\w]+)/citations/(?P<field>[-\w]+)/(?P<link_id>[-\w]+)/?$',
        PostOtherLabelsCitationDetailView.as_view(), name="post-other-labels-citation-detail-view"),
    url(r'^/(?P<parent_pk>[-\w]+)/other_labels/(?P<child_pk>[-\w]+)/citations/(?P<field>[-\w]+)/?$',
        PostOtherLabelsCitationListView.as_view(), name="post-other-labels-citation-list-view"),
    url(r'^/(?P<parent_pk>[-\w]+)/other_labels/(?P<child_pk>[-\w]+)/citations/?$',
        PostOtherLabelFieldCitationView.as_view(), name="post-other-labels-field-citation-view"),

    url(r'^/(?P<parent_pk>[-\w]+)/other_labels/(?P<pk>[-\w]+)/links/(?P<link_pk>[-\w]+)/?$',
        PostOtherLabelsLinkDetail.as_view(), name="post-other-label-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/other_labels/(?P<pk>[-\w]+)/links/?$', PostOtherLabelsLinkList.as_view(),
        name="posts-other-label-link-list"),
    url(r'^/(?P<parent_pk>[-\w]+)/other_labels/(?P<pk>[-\w]+)/?$', PostOtherLabelsDetail.as_view(),
        name="post-other-label-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/other_labels/?$', PostOtherLabelsList.as_view(), name="post-other-label-list"),

    url(r'^/(?P<parent_pk>[-\w]+)/links/(?P<pk>[-\w]+)/?$', PostLinkDetail.as_view(), name="posts-link-detail"),
    url(r'^/(?P<parent_pk>[-\w]+)/links/?$', PostLinkList.as_view(), name="post-link-list"),

    url(r'^/(?P<parent>[-\w]+)/citations/(?P<field>\w+)/(?P<pk>\w+)/?$',
        PostCitationDetailView.as_view(), name="post-citation-detail-view"),
    url(r'^/(?P<pk>[-\w]+)/citations/(?P<field>\w+)/?$',
        PostCitationListCreateView.as_view(), name="post-citation-list-views"),
    url(r'^/(?P<pk>[-\w]+)/citations/?$', PostFieldCitationView.as_view(),
        name="post-citation-field-view"),

    url(r'^/(?P<pk>[-\w]+)/?$', PostDetail.as_view(), name="post-detail"),
    url(r'^/?$', PostList.as_view(), name="post-list"),


]
