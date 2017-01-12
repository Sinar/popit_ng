from django.conf.urls import url
from popit_search.views import AdvanceSearchView


urlpatterns = [
        url(r"^(?P<entity>\w+)$", AdvanceSearchView.as_view(), name="advance_search"),

        ]
