from django.contrib import admin
from hvad.admin import TranslatableAdmin
from popit.models import Person
from popit.models import Link
from popit.models import Contact
from popit.models import OtherName
from popit.models import Identifier
from popit.models import Area
from popit.models import Organization
from popit.models import Post
from popit.models import ContactDetail
from popit.models import Membership
from reversion.admin import VersionAdmin


# Register your models here.
class PersonAdmin(TranslatableAdmin, VersionAdmin):
    pass


class LinkAdmin(TranslatableAdmin, VersionAdmin):
    pass


class ContactAdmin(TranslatableAdmin, VersionAdmin):
    pass


class OtherNameAdmin(TranslatableAdmin, VersionAdmin):
    pass


class IdentifierAdmin(TranslatableAdmin, VersionAdmin):
    pass


class AreaAdmin(TranslatableAdmin, VersionAdmin):
    pass


class OrganizationAdmin(TranslatableAdmin, VersionAdmin):
    pass


class PostAdmin(TranslatableAdmin, VersionAdmin):
    pass


class ContactDetailAdmin(TranslatableAdmin, VersionAdmin):
    pass


class MembershipAdmin(TranslatableAdmin, VersionAdmin):
    pass

admin.site.register(Person, PersonAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(OtherName, OtherNameAdmin)
admin.site.register(Identifier, IdentifierAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ContactDetail, ContactDetailAdmin)
admin.site.register(Membership, MembershipAdmin)