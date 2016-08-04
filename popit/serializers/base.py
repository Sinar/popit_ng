from hvad.contrib.restframework import TranslatableModelSerializer
from popit.models import Link
from popit.models import Area


class BasePopitSerializer(TranslatableModelSerializer):

    def create_links(self, validated_data, entity):
        language_code = self.language
        validated_data["content_object"] = entity
        Link.objects.language(language_code).create(**validated_data)

    def create_child(self, validated_data, child, parent):
        links = validated_data.pop("links", [])
        language_code = self.language
        validated_data["content_object"] = parent
        obj = child.objects.language(language_code).create(**validated_data)
        for link in links:
            self.create_links(link, obj)

    def create_area(self, validated_data):
        language_code = self.language
        validated_data.pop("language_code", None)
        area = Area.objects.language(language_code).create(**validated_data)
        return area

    def update_childs(self, validated_data, child, parent):
        # parent mostly exist at create,
        language_code = self.language
        if validated_data.get("id"):
            try:
                objs = child.objects.untranslated().get(id=validated_data.get("id"))
            except child.DoesNotExist:
                self.create_child(validated_data, child, parent)
                return

            if not language_code in objs.get_available_languages():
                obj = objs.translate(language_code)
            else:
                obj = child.objects.language(language_code).get(id=validated_data.get("id"))

            links = validated_data.pop("links", [])

            for key, value in validated_data.iteritems():
                if key in ("id", "language_code", "created_at" "updated_at"):
                    continue
                setattr(obj, key, value)

            obj.save()

            for link in links:
                self.update_links(link, obj)
        else:
            self.create_child(validated_data, child, parent)

    def update_links(self, validated_data, parent):
        language_code = self.language

        if validated_data.get("id"):
            links = Link.objects.language(language_code).filter(id=validated_data.get("id"))
            if not links:
                self.create_links(validated_data, parent)
            else:
                link = links[0]
                link.label = validated_data.get("label", link.label)
                link.field = validated_data.get("field", link.field)
                link.url = validated_data.get("url", link.url)
                link.note = validated_data.get("note", link.note)
                link.save()
        else:
            self.create_links(validated_data, parent)