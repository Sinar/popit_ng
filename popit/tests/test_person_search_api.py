from django.test import TestCase
from popit_search.views import ResultFilters
from popit_search.views import ES_MODEL_MAP
from popit_search.views import ES_SERIALIZER_MAP
from popit_search.views import GenericSearchView
from popit.models import Person
from popit.serializers import PersonSerializer
from mock import patch
from mock import DEFAULT


class PersonSearchUtilsTestCase(TestCase):
    fixtures = [ "api_request_test_data.yaml" ]

    def test_filter_person_exist(self):
        filter_ = ResultFilters()
        entity = ES_MODEL_MAP["persons"]
        check = filter_.filter_instance(entity, "8497ba86-7485-42d2-9596-2ab14520f1f4", "en")
        self.assertTrue(check)

    def test_filter_person_not_exist(self):
        filter_ = ResultFilters()
        entity = ES_MODEL_MAP["persons"]
        check = filter_.filter_instance(entity, "not_exist", "en")
        self.assertFalse(check)

    def test_filter_person_result(self):
        test_data = [
            {
                u'identifiers': [],
                u'links': [], u'honorific_suffix': None,
                u'image': None,
                u'updated_at': u'2016-03-09T01:51:30.546117Z',
                u'patronymic_name': None,
                u'national_identity': None,
                u'language_code': u'en',
                u'summary': u'',
                u'id': u'c0c56e3684cb466f8e3cd373c77b817d',
                u'biography': u'',
                u'additional_name': None,
                u'other_names': [],
                u'honorific_prefix': None,
                u'given_name': None,
                u'email': None,
                u'contact_details': [],
                u'family_name': None,
                u'name': u'Billy Kidd',
                u'gender': None,
                u'created_at': u'2016-03-09T01:51:30.546088Z',
                u'death_date': None,
                u'sort_name': None,
                u'memberships': [],
                u'birth_date': None
            },
            {
                u'identifiers': [
                    {
                        u'identifier': u'12321223',
                        u'links': [
                            {
                                u'url': u'http://github.com/sinarproject/',
                                u'created_at': u'2015-10-12T00:00:00Z',
                                u'updated_at': u'2015-10-12T00:00:00Z',
                                u'label': u'',
                                u'note': u'',
                                u'field': u'',
                                u'language_code': u'en',
                                u'id': u'9c9a2093-c3eb-4b51-b869-0d3b4ab281fd'
                            }
                        ],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'language_code': u'en',
                        u'scheme': u'random',
                        u'id': u'af7c01b5-1c4f-4c08-9174-3de5ff270bdb'
                    },
                    {
                        u'identifier': u'53110321',
                        u'links': [],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'language_code': u'en',
                        u'scheme': u'random',
                        u'id': u'34b59cb9-607a-43c7-9d13-dfe258790ebf'
                    }
                ],
                u'links': [
                    {
                        u'url': u'http://github.com/sweemeng/',
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'label': u'',
                        u'note': u'just the github link',
                        u'field': u'',
                        u'language_code': u'en',
                        u'id': u'f70854dd-4e2e-4141-a2b8-051a36e5c9ee'
                    }
                ],
                u'honorific_suffix': u'of Sinar Project',
                u'image': u'',
                u'updated_at': u'2015-10-06T00:00:00Z',
                u'patronymic_name': u'',
                u'national_identity': u'Malaysia',
                u'language_code': u'en',
                u'summary': u'Our test person',
                u'id': u'8497ba86-7485-42d2-9596-2ab14520f1f4',
                u'biography': u'he is created so that we can test this application',
                u'additional_name': u'Fake Person',
                u'other_names': [
                    {
                        u'family_name': u'Doe',
                        u'links': [
                            {
                                u'url': u'http://google.com',
                                u'created_at': u'2015-10-28T00:00:00Z',
                                u'updated_at': u'2015-10-28T00:00:00Z',
                                u'label': u'',
                                u'note': u'',
                                u'field': u'',
                                u'language_code': u'en',
                                u'id': u'4d8d71c4-20ea-4ed1-ae38-4b7d7550cdf6'
                            }
                        ],
                        u'end_date': u'2000-01-01',
                        u'honorific_suffix': u'of Sinar Project',
                        u'additional_name': u'something',
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'start_date': u'1950-01-01',
                        u'note': u'Turn out that she had a sex change. People have right to decide their own gender asshole!',
                        u'honorific_prefix': u'Datuk',
                        u'given_name': u'Lucky Jane',
                        u'language_code': u'en',
                        u'patronymic_name': u'',
                        u'id': u'cf93e73f-91b6-4fad-bf76-0782c80297a8',
                        u'name': u'Jane'
                    }
                ],
                u'honorific_prefix': u'Datuk',
                u'given_name': u'John Doe',
                u'email': u'johndoe@sinarproject.org',
                u'contact_details': [
                    {
                        u'valid_until': u'2020-10-06',
                        u'valid_from': u'2015-10-06T00:00:00.00000+00:00',
                        u'links': [
                            {
                                u'url': u'http://google.com',
                                u'created_at': u'2015-10-28T00:00:00Z',
                                u'updated_at': u'2015-11-09T00:00:00Z',
                                u'label': u'',
                                u'note': u'',
                                u'field': u'',
                                u'language_code': u'en',
                                u'id': u'6d0afb46-67d4-4708-87c4-4d51ce99767e'
                            }
                        ],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-11-09T00:00:00Z',
                        u'value': u'0123423424342',
                        u'label': u'anon phone',
                        u'note': u'Just an anon phone',
                        u'language_code': u'en',
                        u'type': u'phone',
                        u'id': u'2256ec04-2d1d-4994-b1f1-16d3f5245441'
                    }
                ],
                u'family_name': u'Doe',
                u'name': u'John',
                u'gender': u'Male',
                u'created_at': u'2015-10-06T00:00:00Z',
                u'death_date': u'2001-01-01',
                u'sort_name': u'',
                u'memberships': [
                    {
                        u'member': None,
                        u'area_id': None,
                        u'contact_details': [],
                        u'end_date': None,
                        u'links': [],
                        u'on_behalf_of_id': None,
                        u'created_at': u'2015-11-13T02:44:58.358098Z',
                        u'language_code': u'en',
                        u'updated_at': u'2015-11-13T02:44:58.358117Z',
                        u'start_date': None,
                        u'organization_id': u'3d62d9ea-0600-4f29-8ce6-f7720fd49aa3',
                        u'post_id': None,
                        u'on_behalf_of': None,
                        u'role': u'',
                        u'member_id': None,
                        u'person_id': u'8497ba86-7485-42d2-9596-2ab14520f1f4',
                        u'label': u'',
                        u'id': u'b5464931-d3a9-4250-a645-204740c1bd9e'
                    }
                ],
                u'birth_date': u'1901-01-01'
            }
        ]
        # Billy kid do not exist in fixture
        filter_ = ResultFilters()
        result =filter_.filter_result(test_data, "persons", "en")
        self.assertEqual(len(result), 1)

    def test_filter_nested(self):
        test_data = {
                u'identifiers': [
                    {
                        u'identifier': u'12321223',
                        u'links': [
                            {
                                u'url': u'http://github.com/sinarproject/',
                                u'created_at': u'2015-10-12T00:00:00Z',
                                u'updated_at': u'2015-10-12T00:00:00Z',
                                u'label': u'',
                                u'note': u'',
                                u'field': u'',
                                u'language_code': u'en',
                                u'id': u'9c9a2093-c3eb-4b51-b869-0d3b4ab281fd'
                            }
                        ],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'language_code': u'en',
                        u'scheme': u'random',
                        u'id': u'af7c01b5-1c4f-4c08-9174-3de5ff270bdb'
                    },
                    {
                        u'identifier': u'53110321',
                        u'links': [],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'language_code': u'en',
                        u'scheme': u'random',
                        u'id': u'34b59cb9-607a-43c7-9d13-dfe258790ebf'
                    }
                ],
                u'links': [
                    {
                        u'url': u'http://github.com/sweemeng/',
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'label': u'',
                        u'note': u'just the github link',
                        u'field': u'',
                        u'language_code': u'en',
                        u'id': u'f70854dd-4e2e-4141-a2b8-051a36e5c9ee'
                    },
                    {
                        u'url': u'http://google/',
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'label': u'',
                        u'note': u'just the google link',
                        u'field': u'',
                        u'language_code': u'en',
                        u'id': u'not_exist'
                    }
                ],
                u'honorific_suffix': u'of Sinar Project',
                u'image': u'',
                u'updated_at': u'2015-10-06T00:00:00Z',
                u'patronymic_name': u'',
                u'national_identity': u'Malaysia',
                u'language_code': u'en',
                u'summary': u'Our test person',
                u'id': u'8497ba86-7485-42d2-9596-2ab14520f1f4',
                u'biography': u'he is created so that we can test this application',
                u'additional_name': u'Fake Person',
                u'other_names': [
                    {
                        u'family_name': u'Doe',
                        u'links': [
                            {
                                u'url': u'http://google.com',
                                u'created_at': u'2015-10-28T00:00:00Z',
                                u'updated_at': u'2015-10-28T00:00:00Z',
                                u'label': u'',
                                u'note': u'',
                                u'field': u'',
                                u'language_code': u'en',
                                u'id': u'4d8d71c4-20ea-4ed1-ae38-4b7d7550cdf6'
                            }
                        ],
                        u'end_date': u'2000-01-01',
                        u'honorific_suffix': u'of Sinar Project',
                        u'additional_name': u'something',
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'start_date': u'1950-01-01',
                        u'note': u'Turn out that she had a sex change. People have right to decide their own gender asshole!',
                        u'honorific_prefix': u'Datuk',
                        u'given_name': u'Lucky Jane',
                        u'language_code': u'en',
                        u'patronymic_name': u'',
                        u'id': u'cf93e73f-91b6-4fad-bf76-0782c80297a8',
                        u'name': u'Jane'
                    }
                ],
                u'honorific_prefix': u'Datuk',
                u'given_name': u'John Doe',
                u'email': u'johndoe@sinarproject.org',
                u'contact_details': [
                    {
                        u'valid_until': u'2020-10-06',
                        u'valid_from': u'2015-10-06T00:00:00.00000+00:00',
                        u'links': [
                            {
                                u'url': u'http://google.com',
                                u'created_at': u'2015-10-28T00:00:00Z',
                                u'updated_at': u'2015-11-09T00:00:00Z',
                                u'label': u'',
                                u'note': u'',
                                u'field': u'',
                                u'language_code': u'en',
                                u'id': u'6d0afb46-67d4-4708-87c4-4d51ce99767e'
                            }
                        ],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-11-09T00:00:00Z',
                        u'value': u'0123423424342',
                        u'label': u'anon phone',
                        u'note': u'Just an anon phone',
                        u'language_code': u'en',
                        u'type': u'phone',
                        u'id': u'2256ec04-2d1d-4994-b1f1-16d3f5245441'
                    }
                ],
                u'family_name': u'Doe',
                u'name': u'John',
                u'gender': u'Male',
                u'created_at': u'2015-10-06T00:00:00Z',
                u'death_date': u'2001-01-01',
                u'sort_name': u'',
                u'memberships': [
                    {
                        u'member': None,
                        u'area_id': None,
                        u'contact_details': [],
                        u'end_date': None,
                        u'links': [],
                        u'on_behalf_of_id': None,
                        u'created_at': u'2015-11-13T02:44:58.358098Z',
                        u'language_code': u'en',
                        u'updated_at': u'2015-11-13T02:44:58.358117Z',
                        u'start_date': None,
                        u'organization_id': u'3d62d9ea-0600-4f29-8ce6-f7720fd49aa3',
                        u'post_id': None,
                        u'on_behalf_of': None,
                        u'role': u'',
                        u'member_id': None,
                        u'person_id': u'8497ba86-7485-42d2-9596-2ab14520f1f4',
                        u'label': u'',
                        u'id': u'b5464931-d3a9-4250-a645-204740c1bd9e'
                    },
                    {
                        u'member': None,
                        u'area_id': None,
                        u'contact_details': [],
                        u'end_date': None,
                        u'links': [],
                        u'on_behalf_of_id': None,
                        u'created_at': u'2015-11-13T02:44:58.358098Z',
                        u'language_code': u'en',
                        u'updated_at': u'2015-11-13T02:44:58.358117Z',
                        u'start_date': None,
                        u'organization_id': u'3d62d9ea-0600-4f29-8ce6-f7720fd49aa3',
                        u'post_id': None,
                        u'on_behalf_of': None,
                        u'role': u'',
                        u'member_id': None,
                        u'person_id': u'8497ba86-7485-42d2-9596-2ab14520f1f4',
                        u'label': u'',
                        u'id': u'not_exist'
                    }
                ],
                u'birth_date': u'1901-01-01'
            }

        filter_ = ResultFilters()
        result = filter_.filter_nested(test_data, "en")
        self.assertEqual(len(result["memberships"]), 1)
        self.assertEqual(len(result["other_names"]), 1)
        self.assertEqual(len(result["links"]), 1)

    def test_drop_result(self):
        test_data = {
            u'identifiers':
                [
                    {
                        u'identifier': u'12321223',
                        u'links': [
                            {
                                u'url': u'http://github.com/sinarproject/',
                                u'created_at': u'2015-10-12T00:00:00Z',
                                u'updated_at': u'2015-10-12T00:00:00Z',
                                u'label': u'',
                                u'note': u'',
                                u'field': u'',
                                u'language_code': u'en',
                                u'id': u'9c9a2093-c3eb-4b51-b869-0d3b4ab281fd'
                            }
                        ],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'language_code': u'en',
                        u'scheme': u'random',
                        u'id': u'af7c01b5-1c4f-4c08-9174-3de5ff270bdb'
                    },
                    {
                        u'identifier': u'53110321',
                        u'links': [],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'language_code': u'en',
                        u'scheme': u'random',
                        u'id': u'34b59cb9-607a-43c7-9d13-dfe258790ebf'
                    }
                ],
            u'links': [
                {
                    u'url': u'http://github.com/sweemeng/',
                    u'created_at': u'2015-10-06T00:00:00Z',
                    u'updated_at': u'2015-10-06T00:00:00Z',
                    u'label': u'',
                    u'note': u'just the github link',
                    u'field': u'',
                    u'language_code': u'en',
                    u'id': u'f70854dd-4e2e-4141-a2b8-051a36e5c9ee'
                }
            ],
            u'honorific_suffix': u'of Sinar Project',
            u'image': u'',
            u'updated_at': u'2015-10-06T00:00:00Z',
            u'patronymic_name': u'',
            u'national_identity': u'Malaysia',
            u'language_code': u'en',
            u'summary': u'Our test person',
            u'id': u'8497ba86-7485-42d2-9596-2ab14520f1f4',
            u'biography': u'he is created so that we can test this application',
            u'additional_name': u'Fake Person',
            u'other_names': [
                {
                    u'family_name': u'Doe',
                    u'links': [
                        {
                            u'url': u'http://google.com',
                            u'created_at': u'2015-10-28T00:00:00Z',
                            u'updated_at': u'2015-10-28T00:00:00Z',
                            u'label': u'',
                            u'note': u'',
                            u'field': u'',
                            u'language_code': u'en',
                            u'id': u'4d8d71c4-20ea-4ed1-ae38-4b7d7550cdf6'
                        }
                    ],
                    u'end_date': u'2000-01-01',
                    u'honorific_suffix': u'of Sinar Project',
                    u'additional_name': u'something',
                    u'created_at': u'2015-10-06T00:00:00Z',
                    u'updated_at': u'2015-10-06T00:00:00Z',
                    u'start_date': u'1950-01-01',
                    u'note': u'Turn out that she had a sex change. People have right to decide their own gender asshole!',
                    u'honorific_prefix': u'Datuk',
                    u'given_name': u'Lucky Jane',
                    u'language_code': u'en',
                    u'patronymic_name': u'',
                    u'id': u'cf93e73f-91b6-4fad-bf76-0782c80297a8',
                    u'name': u'Jane'
                }
            ],
            u'honorific_prefix': u'Datuk',
            u'given_name': u'John Doe',
            u'email': u'johndoe@sinarproject.org',
            u'contact_details': [
                {
                    u'valid_until': u'2020-10-06',
                    u'valid_from': u'2015-10-06T00:00:00.00000+00:00',
                    u'links': [
                        {
                            u'url': u'http://google.com',
                            u'created_at': u'2015-10-28T00:00:00Z',
                            u'updated_at': u'2015-11-09T00:00:00Z',
                            u'label': u'',
                            u'note': u'',
                            u'field': u'',
                            u'language_code': u'en',
                            u'id': u'6d0afb46-67d4-4708-87c4-4d51ce99767e'
                        }
                    ],
                    u'created_at': u'2015-10-06T00:00:00Z',
                    u'updated_at': u'2015-11-09T00:00:00Z',
                    u'value': u'0123423424342',
                    u'label': u'anon phone',
                    u'note': u'Just an anon phone',
                    u'language_code': u'en',
                    u'type': u'phone',
                    u'id': u'2256ec04-2d1d-4994-b1f1-16d3f5245441'
                }
            ],
            u'family_name': u'Doe',
            u'name': u'John',
            u'gender': u'Male',
            u'created_at': u'2015-10-06T00:00:00Z',
            u'death_date': u'2001-01-01',
            u'sort_name': u'',
            u'memberships': [
                {
                    u'member': None,
                    u'area_id': None,
                    u'contact_details': [],
                    u'end_date': None,
                    u'links': [],
                    u'on_behalf_of_id': None,
                    u'created_at': u'2015-11-13T02:44:58.358098Z',
                    u'language_code': u'en',
                    u'updated_at': u'2015-11-13T02:44:58.358117Z',
                    u'start_date': None,
                    u'organization_id': u'3d62d9ea-0600-4f29-8ce6-f7720fd49aa3',
                    u'post_id': None,
                    u'on_behalf_of': None,
                    u'role': u'',
                    u'member_id': None,
                    u'person_id': u'8497ba86-7485-42d2-9596-2ab14520f1f4',
                    u'label': u'',
                    u'id': u'b5464931-d3a9-4250-a645-204740c1bd9e'
                }
            ],
            u'birth_date': u'1901-01-01'
        }

        filter_ = ResultFilters()
        result = filter_.drop_result(test_data, "name:john")
        self.assertFalse(result)

    def test_parse_query(self):
        filter_ = ResultFilters()
        query = "name:Bill"
        query, value = filter_.parse_query(query)
        self.assertEqual(value, "Bill")
        self.assertEqual(query, ["name",])

    @patch("popit_search.views.SerializerSearch")
    def test_search_workflow(self, mock_search):
        instance = mock_search.return_value
        instance.search.return_value = [
            {
                u'identifiers': [],
                u'links': [], u'honorific_suffix': None,
                u'image': None,
                u'updated_at': u'2016-03-09T01:51:30.546117Z',
                u'patronymic_name': None,
                u'national_identity': None,
                u'language_code': u'en',
                u'summary': u'',
                u'id': u'c0c56e3684cb466f8e3cd373c77b817d',
                u'biography': u'',
                u'additional_name': None,
                u'other_names': [],
                u'honorific_prefix': None,
                u'given_name': None,
                u'email': None,
                u'contact_details': [],
                u'family_name': None,
                u'name': u'Billy Kidd',
                u'gender': None,
                u'created_at': u'2016-03-09T01:51:30.546088Z',
                u'death_date': None,
                u'sort_name': None,
                u'memberships': [],
                u'birth_date': None
            },
            {
                u'identifiers': [
                    {
                        u'identifier': u'12321223',
                        u'links': [
                            {
                                u'url': u'http://github.com/sinarproject/',
                                u'created_at': u'2015-10-12T00:00:00Z',
                                u'updated_at': u'2015-10-12T00:00:00Z',
                                u'label': u'',
                                u'note': u'',
                                u'field': u'',
                                u'language_code': u'en',
                                u'id': u'9c9a2093-c3eb-4b51-b869-0d3b4ab281fd'
                            }
                        ],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'language_code': u'en',
                        u'scheme': u'random',
                        u'id': u'af7c01b5-1c4f-4c08-9174-3de5ff270bdb'
                    },
                    {
                        u'identifier': u'53110321',
                        u'links': [],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'language_code': u'en',
                        u'scheme': u'random',
                        u'id': u'34b59cb9-607a-43c7-9d13-dfe258790ebf'
                    }
                ],
                u'links': [
                    {
                        u'url': u'http://github.com/sweemeng/',
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'label': u'',
                        u'note': u'just the github link',
                        u'field': u'',
                        u'language_code': u'en',
                        u'id': u'f70854dd-4e2e-4141-a2b8-051a36e5c9ee'
                    }
                ],
                u'honorific_suffix': u'of Sinar Project',
                u'image': u'',
                u'updated_at': u'2015-10-06T00:00:00Z',
                u'patronymic_name': u'',
                u'national_identity': u'Malaysia',
                u'language_code': u'en',
                u'summary': u'Our test person',
                u'id': u'8497ba86-7485-42d2-9596-2ab14520f1f4',
                u'biography': u'he is created so that we can test this application',
                u'additional_name': u'Fake Person',
                u'other_names': [
                    {
                        u'family_name': u'Doe',
                        u'links': [
                            {
                                u'url': u'http://google.com',
                                u'created_at': u'2015-10-28T00:00:00Z',
                                u'updated_at': u'2015-10-28T00:00:00Z',
                                u'label': u'',
                                u'note': u'',
                                u'field': u'',
                                u'language_code': u'en',
                                u'id': u'4d8d71c4-20ea-4ed1-ae38-4b7d7550cdf6'
                            }
                        ],
                        u'end_date': u'2000-01-01',
                        u'honorific_suffix': u'of Sinar Project',
                        u'additional_name': u'something',
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-10-06T00:00:00Z',
                        u'start_date': u'1950-01-01',
                        u'note': u'Turn out that she had a sex change. People have right to decide their own gender asshole!',
                        u'honorific_prefix': u'Datuk',
                        u'given_name': u'Lucky Jane',
                        u'language_code': u'en',
                        u'patronymic_name': u'',
                        u'id': u'cf93e73f-91b6-4fad-bf76-0782c80297a8',
                        u'name': u'Jane'
                    }
                ],
                u'honorific_prefix': u'Datuk',
                u'given_name': u'John Doe',
                u'email': u'johndoe@sinarproject.org',
                u'contact_details': [
                    {
                        u'valid_until': u'2020-10-06',
                        u'valid_from': u'2015-10-06T00:00:00.00000+00:00',
                        u'links': [
                            {
                                u'url': u'http://google.com',
                                u'created_at': u'2015-10-28T00:00:00Z',
                                u'updated_at': u'2015-11-09T00:00:00Z',
                                u'label': u'',
                                u'note': u'',
                                u'field': u'',
                                u'language_code': u'en',
                                u'id': u'6d0afb46-67d4-4708-87c4-4d51ce99767e'
                            }
                        ],
                        u'created_at': u'2015-10-06T00:00:00Z',
                        u'updated_at': u'2015-11-09T00:00:00Z',
                        u'value': u'0123423424342',
                        u'label': u'anon phone',
                        u'note': u'Just an anon phone',
                        u'language_code': u'en',
                        u'type': u'phone',
                        u'id': u'2256ec04-2d1d-4994-b1f1-16d3f5245441'
                    }
                ],
                u'family_name': u'Doe',
                u'name': u'John',
                u'gender': u'Male',
                u'created_at': u'2015-10-06T00:00:00Z',
                u'death_date': u'2001-01-01',
                u'sort_name': u'',
                u'memberships': [
                    {
                        u'member': None,
                        u'area_id': None,
                        u'contact_details': [],
                        u'end_date': None,
                        u'links': [],
                        u'on_behalf_of_id': None,
                        u'created_at': u'2015-11-13T02:44:58.358098Z',
                        u'language_code': u'en',
                        u'updated_at': u'2015-11-13T02:44:58.358117Z',
                        u'start_date': None,
                        u'organization_id': u'3d62d9ea-0600-4f29-8ce6-f7720fd49aa3',
                        u'post_id': None,
                        u'on_behalf_of': None,
                        u'role': u'',
                        u'member_id': None,
                        u'person_id': u'8497ba86-7485-42d2-9596-2ab14520f1f4',
                        u'label': u'',
                        u'id': u'b5464931-d3a9-4250-a645-204740c1bd9e'
                    }
                ],
                u'birth_date': u'1901-01-01'
            }
        ]

        params = {
            "q": "name:John"
        }
        response = self.client.get("/en/search/persons/", params)
        data = response.data
        print(data)
        self.assertEqual(len(data["results"]), 1)

