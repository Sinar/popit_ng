from django.test import TestCase
from django.test import override_settings
from popit_search.utils import search
from popit.models import Person
from popit.serializers import PersonSerializer
from mock import patch


# I really don't like the idea of testing implementation
# TODO: Also find out the proper output from ES, to make this test proper.
@override_settings(ES_INDEX="test_popit")
class SearchUtilTestCase(TestCase):
    fixtures = [ "api_request_test_data.yaml" ]

    @patch("elasticsearch.Elasticsearch")
    def test_index_person(self, mock_es):
        instance = mock_es.return_value
        instance.index.return_value = {

        }
        instance.search.return_value = {
            "hits": {
                "hits": []
            }
        }
        popit_search = search.SerializerSearch("persons", index="test_popit")
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        serializer = PersonSerializer(person)
        result = popit_search.add(person, PersonSerializer)
        data=popit_search.sanitize_data(serializer.data)
        instance.index.assert_called_with(index=popit_search.index, doc_type=popit_search.doc_type, body=data)

    @patch("elasticsearch.Elasticsearch")
    def test_search_person(self, mock_es):
        instance = mock_es.return_value
        instance.index.return_value = {

        }
        instance.search.return_value = {
            "hits": {
                "hits": []
            }
        }
        popit_search = search.SerializerSearch("persons", index="test_popit")

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        serializer = PersonSerializer(person)
        result = popit_search.add(person, PersonSerializer)
        search_result = popit_search.search("id:ab1a5788e5bae955c048748fa6af0e97", language="en")
        instance.search.assert_called_with(index=popit_search.index, doc_type=popit_search.doc_type,
                                           q="id:ab1a5788e5bae955c048748fa6af0e97 AND language_code:en")

    @patch("elasticsearch.Elasticsearch")
    def test_update_person_search(self, mock_es):
        instance = mock_es.return_value
        instance.index.return_value = {

        }
        instance.search.return_value = {
            "hits": {
                "hits": [
                    {
                        "_id": "random_key",
                        "_source": {"id":"_blah"}
                    }
                ]
            }
        }
        instance.update.return_value = {

        }
        popit_search = search.SerializerSearch("persons", index="test_popit")

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        serializer = PersonSerializer(person)

        person.given_name = "jerry jambul"
        person.save()
        result = popit_search.update(person, PersonSerializer)
        data = popit_search.sanitize_data(serializer.data)
        instance.update.assert_called_with(index=popit_search.index, doc_type=popit_search.doc_type, id="random_key",
                                           body={"doc":data})

    @patch("elasticsearch.Elasticsearch")
    def test_delete_person_search(self, mock_es):
        instance = mock_es.return_value
        instance.index.return_value = {

        }
        instance.search.return_value = {
            "hits": {
                "hits": [
                    {
                        "_id": "random_key"
                    }
                ]
            }
        }
        instance.delete.return_value = {

        }
        popit_search = search.SerializerSearch("persons", index="test_popit")

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        popit_search.delete(person)
        instance.delete.assert_called_with(index=popit_search.index, doc_type=popit_search.doc_type, id="random_key")

    @patch("elasticsearch.Elasticsearch")
    def test_sanitize_data(self, mock_es):
        data = {
            "name": "rocky",
            "birth_date": "1999",
            "contact_details": [
                {
                    "type":"email",
                    "value":"test@sinarproject.org",
                    "valid_from": "1999",
                    "valid_until": "2000"
                }
            ],
            "other_names": [
                {
                    "name": "the winner",
                    "start_date": "2000"
                }

            ]
        }
        popit_search = search.SerializerSearch("persons", index="test_popit")
        output = popit_search.sanitize_data(data)
        self.assertEqual(output["birth_date"], "1999-01-01T000000")
        self.assertEqual(output["contact_details"][0]["valid_from"], "1999-01-01T000000")
        self.assertEqual(output["other_names"][0]["start_date"], "2000-01-01T000000")
