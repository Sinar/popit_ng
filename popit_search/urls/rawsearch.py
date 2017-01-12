from django.conf.urls import url
from popit_search.views import GenericRawSearchView


urlpatterns = [
        url(r"^$", GenericRawSearchView.as_view(), name="rawsearch"),

        ]
