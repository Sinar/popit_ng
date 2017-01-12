from django.conf.urls import url
from popit.views import *


urlpatterns = [
    url(r'^(?P<language>\w{2})', api_root, name="api-root"),
    url(r'^$', api_root_all),
]
