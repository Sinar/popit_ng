from popit.models import Organization
from popit.models import Person
from popit.models import Post
from popit.models import Membership
from popit.models import Identifier
from popit.models import ContactDetail
from popit.models import OtherName
from popit.models import Link
from popit.models import Area
from popit.serializers import OrganizationSerializer
from popit.serializers import PersonSerializer
from popit.serializers import PostSerializer
from popit.serializers import MembershipSerializer
from popit.serializers import AreaSerializer


ES_MODEL_MAP = {
    "organizations": Organization,
    "persons": Person,
    "posts": Post,
    "memberships": Membership,
    "identifiers": Identifier,
    "other_names": OtherName,
    "links": Link,
    "contact_details": ContactDetail,
    "parent": Organization,
    "other_labels": OtherName,
    "contactdetails": ContactDetail,
    "areas": Area
}

ES_SERIALIZER_MAP = {
    "organizations": OrganizationSerializer,
    "persons": PersonSerializer,
    "posts": PostSerializer,
    "memberships": MembershipSerializer,
    "area": AreaSerializer
}