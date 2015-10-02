from django.contrib import admin
from hvad.admin import TranslatableAdmin
from popit.models import Person
from popit.models import Link
from popit.models import Contact
from popit.models import OtherName
from popit.models import Identifier


# Register your models here.
class PersonAdmin(TranslatableAdmin):
    pass


class LinkAdmin(TranslatableAdmin):
    pass


class ContactAdmin(TranslatableAdmin):
    pass


class OtherNameAdmin(TranslatableAdmin):
    pass


class IdentifierAdmin(TranslatableAdmin):
    pass


admin.site.register(Person, PersonAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(OtherName, OtherNameAdmin)
admin.site.register(Identifier, IdentifierAdmin)
