from django.conf.urls import url
from popit_search.views import GenericSearchView


urlpatterns = [
        url(r"^/(?P<index_name>\w+)/?$", GenericSearchView.as_view(), name="search"),

        ]
