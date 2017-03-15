from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.conf import settings



@api_view(("GET",))
@permission_classes([IsAuthenticatedOrReadOnly,])
def api_root(request, language, format=None):
    data = {
        "persons": reverse("person-list", request=request, format=format, args=(language,)),
        "organizations": reverse("organization-list", request=request, format=format, args=(language,)),
        "posts": reverse("post-list", request=request, format=format, args=(language,)),
        "memberships": reverse("membership-list", request=request, format=format, args=(language,)),
        "relations": reverse("relation-list", request=request, format=format, args=(language,)),
    }
    return Response(data)

@api_view(("GET",))
@permission_classes([IsAuthenticatedOrReadOnly,])
def api_root_all(request, format=None):
    data = {

    }
    for lang, lang_desc in settings.LANGUAGES:
        data[lang] = reverse("api-root", request=request, format=format, args=(lang,))
    return Response(data)
