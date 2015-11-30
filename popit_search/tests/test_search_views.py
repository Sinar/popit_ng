from rest_framework.test import APITestCase
from rest_framework import status
from popit_search.utils.search import popit_indexer
from popit_search.utils.search import remove_popit_index
from mock import patch


class SearchAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    @patch("popit_search.utils.search.SerializerSearch.search")
    def test_person_search(self, mock_search):
        params = {
            "q": "id:8497ba86-7485-42d2-9596-2ab14520f1f4"
        }
        mock_search.return_value = [
            {
                "identifiers": [
                    {
                        "identifier": "12321223",
                        "links": [
                            {
                                "url": "http://github.com/sinarproject/",
                                "created_at": "2015-10-12",
                                "updated_at": "2015-10-12",
                                "label": "",
                                "note": None,
                                "field": "",
                                "language_code": None,
                                "id": "9c9a2093-c3eb-4b51-b869-0d3b4ab281fd"
                            }
                        ],
                        "created_at": "2015-10-06",
                        "updated_at": "2015-10-06",
                        "language_code": None,
                        "scheme": "",
                        "id": "af7c01b5-1c4f-4c08-9174-3de5ff270bdb"
                    },
                    {
                        "identifier": "53110321",
                        "links": [],
                        "created_at": "2015-10-06",
                        "updated_at": "2015-10-06",
                        "language_code": None,
                        "scheme": "",
                        "id": "34b59cb9-607a-43c7-9d13-dfe258790ebf"
                    }
                ],
                "links": [
                    {
                        "url": "http://github.com/sweemeng/",
                        "created_at": "2015-10-06",
                        "updated_at": "2015-10-06",
                        "label": "",
                        "note": None,
                        "field": "",
                        "language_code": None,
                        "id": "f70854dd-4e2e-4141-a2b8-051a36e5c9ee"
                    }
                ],
                "honorific_suffix": "of Sinar Project",
                "image": "",
                "updated_at": "2015-10-06T00:00:00Z",
                "patronymic_name": "",
                "national_identity": "Malaysia",
                "language_code": "en",
                "summary": "Our test person",
                "id": "8497ba86-7485-42d2-9596-2ab14520f1f4",
                "biography": "he is created so that we can test this application",
                "additional_name": "Fake Person",
                "other_names": [
                    {
                        "family_name": None,
                        "links": [
                            {
                                "url": "http://google.com",
                                "created_at": "2015-10-28",
                                "updated_at": "2015-10-28",
                                "label": "",
                                "note": None,
                                "field": "",
                                "language_code": None,
                                "id": "4d8d71c4-20ea-4ed1-ae38-4b7d7550cdf6"
                            }
                        ],
                        "end_date": "2000-01-01",
                        "honorific_suffix": None,
                        "additional_name": None,
                        "created_at": "2015-10-06",
                        "updated_at": "2015-10-06",
                        "start_date": "1950-01-01",
                        "note": "Turn out that she had a sex change. People have right to decide their own gender asshole!",
                        "honorific_prefix": None,
                        "given_name": None,
                        "language_code": None,
                        "patronymic_name": None,
                        "id": "cf93e73f-91b6-4fad-bf76-0782c80297a8",
                        "name": ""
                    }
                ],
                "honorific_prefix": "Datuk",
                "given_name": "John Doe",
                "email": "johndoe@sinarproject.org",
                "contact_details": [
                    {
                        "valid_until": "2020-10-06",
                        "valid_from": "2015-10-06",
                        "links": [
                            {
                                "url": "http://google.com",
                                "created_at": "2015-10-28",
                                "updated_at": "2015-11-09",
                                "label": "",
                                "note": None,
                                "field": "",
                                "language_code": None,
                                "id": "6d0afb46-67d4-4708-87c4-4d51ce99767e"
                            }
                        ],
                        "created_at": "2015-10-06",
                        "updated_at": "2015-11-09",
                        "value": "0123423424342",
                        "label": None,
                        "note": None,
                        "language_code": None,
                        "type": "phone",
                        "id": "2256ec04-2d1d-4994-b1f1-16d3f5245441"
                    }
                ],
                "family_name": "Doe",
                "name": "John",
                "gender": "Male",
                "created_at": "2015-10-06T00:00:00Z",
                "death_date": "2001-01-01",
                "sort_name": "",
                "birth_date": "1901-01-01"
            }
        ]
        response = self.client.get("/en/search/persons/", params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

    @patch("popit_search.utils.search.SerializerSearch.search")
    def test_organization_search(self, mock_search):
        params = {
            "q": "id:3d62d9ea-0600-4f29-8ce6-f7720fd49aa3"
        }
        mock_search.return_value = [
            {
                "id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
                "parent": {
                    "id": "612943b1-864d-4188-8d79-ca387ed19b32",
                    "other_names": [],
                    "identifiers": [],
                    "links": [],
                    "contact_details": [],
                    "area": None,
                    "founding_date": "2013-09-01",
                    "dissolution_date": "2020-09-01",
                    "image": "",
                    "created_at": "2015-10-21T23:22:00.443496Z",
                    "updated_at": "2015-10-21T23:22:44.583911Z",
                    "parent": None,
                    "name": "Pirate Party",
                    "classification": "political party",
                    "abstract": "pirates",
                    "description": "arrrrrr",
                    "language_code": "en"
                },
                "parent_id": "612943b1-864d-4188-8d79-ca387ed19b32",
                "other_names": [
                    {
                        "id": "53a22b00-1383-4bf5-b4be-4753d8d16062",
                        "links": [
                            {
                                "id": "fe662497-c24d-4bbb-a72d-feb77319782a",
                                "label": "",
                                "field": "name",
                                "url": "http://sinarproject.org",
                                "created_at": "2015-10-26",
                                "updated_at": "2015-10-26",
                                "note": "",
                                "language_code": "en"
                            }
                        ],
                        "start_date": None,
                        "end_date": None,
                        "created_at": "2015-10-22",
                        "updated_at": "2015-10-22",
                        "note": "really othername field don't seems appropriate for organization",
                        "name": "Not Sinar Project",
                        "family_name": "",
                        "given_name": "",
                        "additional_name": "",
                        "honorific_prefix": "",
                        "honorific_suffix": "",
                        "patronymic_name": "",
                        "language_code": "en"
                    }
                ],
                "identifiers": [
                    {
                        "id": "2d3b8d2c-77b8-42f5-ac62-3e83d4408bda",
                        "links": [
                            {
                                "id": "02369098-7b46-4d62-9318-a5f1c2d385bd",
                                "label": "",
                                "field": "identifier",
                                "url": "http://ssm.com",
                                "created_at": "2015-10-26",
                                "updated_at": "2015-10-26",
                                "note": "",
                                "language_code": "en"
                            }
                        ],
                        "identifier": "3131312",
                        "created_at": "2015-10-22",
                        "updated_at": "2015-10-22",
                        "scheme": "ssm",
                        "language_code": "en"
                    }
                ],
                "links": [
                    {
                        "id": "45b0a790-8c9e-4553-844b-431ed34b6b12",
                        "label": "",
                        "field": "",
                        "url": "https://github.com/sweemeng/",
                        "created_at": "2015-10-22",
                        "updated_at": "2015-10-22",
                        "note": "Web page of the party leader",
                        "language_code": "en"
                    }
                ],
                "contact_details": [
                    {
                        "id": "651da7cd-f109-4aaa-b04c-df835fb6831f",
                        "links": [
                            {
                                "id": "26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf",
                                "label": "",
                                "field": "type",
                                "url": "http://sinarproject.org/about/",
                                "created_at": "2015-10-26",
                                "updated_at": "2015-11-09",
                                "note": "",
                                "language_code": "en"
                            }
                        ],
                        "type": "phone",
                        "value": "0129123132112",
                        "valid_from": "2015-10-22",
                        "valid_until": "2020-10-22",
                        "created_at": "2015-10-22",
                        "updated_at": "2015-11-09",
                        "label": "sinar project phone",
                        "note": "just a phone",
                        "language_code": "en"
                    }
                ],
                "area": {
                    "id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
                    "links": [
                        {
                            "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
                            "label": "",
                            "field": "",
                            "url": "http://en.wikipedia.com",
                            "created_at": "2015-10-30",
                            "updated_at": "2015-10-30",
                            "note": "",
                            "language_code": "en"
                        }
                    ],
                    "identifier": "",
                    "created_at": "2015-10-21T23:44:40.750284Z",
                    "updated_at": "2015-10-21T23:44:40.750308Z",
                    "parent": "4775c9b6-f8fd-4cdc-bda8-a1844fa7f8ea",
                    "name": "kuala lumpur",
                    "classification": "",
                    "language_code": "en"
                },
                "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
                "founding_date": "2015-10-22",
                "dissolution_date": "2020-10-22",
                "image": "",
                "created_at": "2015-10-21T23:46:14.589608Z",
                "updated_at": "2015-10-21T23:48:16.167211Z",
                "name": "Pirate Party KL",
                "classification": "political party",
                "abstract": "KL Branch of Pirate Party",
                "description": "KL Branch of Pirate Party",
                "language_code": "en"
            }
        ]
        response = self.client.get("/en/search/organizations/", params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

    @patch("popit_search.utils.search.SerializerSearch.search")
    def test_membership_search(self, mock_search):
        params = {
            "q": "id:b351cdc2-6961-4fc7-9d61-08fca66e1d44"
        }
        mock_search.return_value = [
            {
                "id": "0a44195b-c3c9-4040-8dbf-be1aa250b700",
                "person": {
                    "id": "ab1a5788e5bae955c048748fa6af0e97",
                    "other_names": [],
                    "identifiers": [],
                    "links": [
                        {
                            "id": "abbd9287ec0b491d6e84dcbfd6f958fc",
                            "label": "",
                            "field": "",
                            "url": "http://sinarproject.org/en/about/team",
                            "created_at": "2015-10-02",
                            "updated_at": "2015-10-02",
                            "note": "Member of sinar project staff",
                            "language_code": "en"
                        },
                        {
                            "id": "a4ffa24a9ef3cbcb8cfaa178c9329367",
                            "label": "",
                            "field": "",
                            "url": "http://github.com/sweemeng/",
                            "created_at": "2015-10-02",
                            "updated_at": "2015-10-02",
                            "note": "github page",
                            "language_code": "en"
                        }
                    ],
                    "contact_details": [
                        {
                            "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
                            "links": [],
                            "type": "phone",
                            "value": "0123421221",
                            "valid_from": "2015-10-05",
                            "valid_until": "2020-10-05",
                            "created_at": "2015-10-05",
                            "updated_at": "2015-11-09",
                            "label": "sweemeng phone",
                            "note": "my phone",
                            "language_code": "en"
                        }
                    ],
                    "birth_date": None,
                    "death_date": None,
                    "email": "sweester@sinarproject.org",
                    "image": "",
                    "created_at": "2015-10-02T00:00:00Z",
                    "updated_at": "2015-10-12T00:00:00Z",
                    "name": "Swee Meng",
                    "family_name": "ng",
                    "given_name": "",
                    "additional_name": "",
                    "honorific_prefix": "",
                    "honorific_suffix": "",
                    "patronymic_name": "",
                    "sort_name": "",
                    "gender": "",
                    "summary": "just an ordinary guy",
                    "biography": "an ordinary guy",
                    "national_identity": "",
                    "language_code": "en"
                },
                "person_id": "ab1a5788e5bae955c048748fa6af0e97",
                "organization": None,
                "organization_id": None,
                "member": None,
                "member_id": None,
                "on_behalf_of": None,
                "on_behalf_of_id": None,
                "area": {
                    "id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
                    "links": [
                        {
                            "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
                            "label": "",
                            "field": "",
                            "url": "http://en.wikipedia.com",
                            "created_at": "2015-10-30",
                            "updated_at": "2015-10-30",
                            "note": "",
                            "language_code": "en"
                        }
                    ],
                    "identifier": "",
                    "created_at": "2015-10-21T23:44:40.750284Z",
                    "updated_at": "2015-10-21T23:44:40.750308Z",
                    "parent": "4775c9b6-f8fd-4cdc-bda8-a1844fa7f8ea",
                    "name": "kuala lumpur",
                    "classification": "",
                    "language_code": "en"
                },
                "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
                "post": {
                    "id": "c1f0f86b-a491-4986-b48d-861b58a3ef6e",
                    "other_labels": [
                        {
                            "id": "aee39ddd-6785-4a36-9781-8e745c6359b7",
                            "links": [
                                {
                                    "id": "6c928027-4813-4770-80a5-ba413a43efae",
                                    "label": "",
                                    "field": "",
                                    "url": "http://www.facebook.com",
                                    "created_at": "2015-11-03",
                                    "updated_at": "2015-11-03",
                                    "note": "",
                                    "language_code": "en"
                                }
                            ],
                            "start_date": None,
                            "end_date": None,
                            "created_at": "2015-11-03",
                            "updated_at": "2015-11-03",
                            "note": "",
                            "name": "bilge rat",
                            "family_name": "",
                            "given_name": "",
                            "additional_name": "",
                            "honorific_prefix": "",
                            "honorific_suffix": "",
                            "patronymic_name": "",
                            "language_code": "en"
                        }
                    ],
                    "organization": {
                        "id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
                        "parent": {
                            "id": "612943b1-864d-4188-8d79-ca387ed19b32",
                            "other_names": [],
                            "identifiers": [],
                            "links": [],
                            "contact_details": [],
                            "area": None,
                            "founding_date": "2013-09-01",
                            "dissolution_date": "2020-09-01",
                            "image": "",
                            "created_at": "2015-10-21T23:22:00.443496Z",
                            "updated_at": "2015-10-21T23:22:44.583911Z",
                            "parent": None,
                            "name": "Pirate Party",
                            "classification": "political party",
                            "abstract": "pirates",
                            "description": "arrrrrr",
                            "language_code": "en"
                        },
                        "parent_id": "612943b1-864d-4188-8d79-ca387ed19b32",
                        "other_names": [
                            {
                                "id": "53a22b00-1383-4bf5-b4be-4753d8d16062",
                                "links": [
                                    {
                                        "id": "fe662497-c24d-4bbb-a72d-feb77319782a",
                                        "label": "",
                                        "field": "name",
                                        "url": "http://sinarproject.org",
                                        "created_at": "2015-10-26",
                                        "updated_at": "2015-10-26",
                                        "note": "",
                                        "language_code": "en"
                                    }
                                ],
                                "start_date": None,
                                "end_date": None,
                                "created_at": "2015-10-22",
                                "updated_at": "2015-10-22",
                                "note": "really othername field don't seems appropriate for organization",
                                "name": "Not Sinar Project",
                                "family_name": "",
                                "given_name": "",
                                "additional_name": "",
                                "honorific_prefix": "",
                                "honorific_suffix": "",
                                "patronymic_name": "",
                                "language_code": "en"
                            }
                        ],
                        "identifiers": [
                            {
                                "id": "2d3b8d2c-77b8-42f5-ac62-3e83d4408bda",
                                "links": [
                                    {
                                        "id": "02369098-7b46-4d62-9318-a5f1c2d385bd",
                                        "label": "",
                                        "field": "identifier",
                                        "url": "http://ssm.com",
                                        "created_at": "2015-10-26",
                                        "updated_at": "2015-10-26",
                                        "note": "",
                                        "language_code": "en"
                                    }
                                ],
                                "identifier": "3131312",
                                "created_at": "2015-10-22",
                                "updated_at": "2015-10-22",
                                "scheme": "ssm",
                                "language_code": "en"
                            }
                        ],
                        "links": [
                            {
                                "id": "45b0a790-8c9e-4553-844b-431ed34b6b12",
                                "label": "",
                                "field": "",
                                "url": "https://github.com/sweemeng/",
                                "created_at": "2015-10-22",
                                "updated_at": "2015-10-22",
                                "note": "Web page of the party leader",
                                "language_code": "en"
                            }
                        ],
                        "contact_details": [
                            {
                                "id": "651da7cd-f109-4aaa-b04c-df835fb6831f",
                                "links": [
                                    {
                                        "id": "26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf",
                                        "label": "",
                                        "field": "type",
                                        "url": "http://sinarproject.org/about/",
                                        "created_at": "2015-10-26",
                                        "updated_at": "2015-11-09",
                                        "note": "",
                                        "language_code": "en"
                                    }
                                ],
                                "type": "phone",
                                "value": "0129123132112",
                                "valid_from": "2015-10-22",
                                "valid_until": "2020-10-22",
                                "created_at": "2015-10-22",
                                "updated_at": "2015-11-09",
                                "label": "sinar project phone",
                                "note": "just a phone",
                                "language_code": "en"
                            }
                        ],
                        "area": {
                            "id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
                            "links": [
                                {
                                    "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
                                    "label": "",
                                    "field": "",
                                    "url": "http://en.wikipedia.com",
                                    "created_at": "2015-10-30",
                                    "updated_at": "2015-10-30",
                                    "note": "",
                                    "language_code": "en"
                                }
                            ],
                            "identifier": "",
                            "created_at": "2015-10-21T23:44:40.750284Z",
                            "updated_at": "2015-10-21T23:44:40.750308Z",
                            "parent": "4775c9b6-f8fd-4cdc-bda8-a1844fa7f8ea",
                            "name": "kuala lumpur",
                            "classification": "",
                            "language_code": "en"
                        },
                        "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
                        "founding_date": "2015-10-22",
                        "dissolution_date": "2020-10-22",
                        "image": "",
                        "created_at": "2015-10-21T23:46:14.589608Z",
                        "updated_at": "2015-10-21T23:48:16.167211Z",
                        "name": "Pirate Party KL",
                        "classification": "political party",
                        "abstract": "KL Branch of Pirate Party",
                        "description": "KL Branch of Pirate Party",
                        "language_code": "en"
                    },
                    "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
                    "area": {
                        "id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
                        "links": [
                            {
                                "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
                                "label": "",
                                "field": "",
                                "url": "http://en.wikipedia.com",
                                "created_at": "2015-10-30",
                                "updated_at": "2015-10-30",
                                "note": "",
                                "language_code": "en"
                            }
                        ],
                        "identifier": "",
                        "created_at": "2015-10-21T23:44:40.750284Z",
                        "updated_at": "2015-10-21T23:44:40.750308Z",
                        "parent": "4775c9b6-f8fd-4cdc-bda8-a1844fa7f8ea",
                        "name": "kuala lumpur",
                        "classification": "",
                        "language_code": "en"
                    },
                    "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
                    "contact_details": [
                        {
                            "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
                            "links": [
                                {
                                    "id": "a37256e6-eab7-417a-8ac8-32edc5031924",
                                    "label": "",
                                    "field": "",
                                    "url": "http://en.wikipedia.com",
                                    "created_at": "2015-11-06",
                                    "updated_at": "2015-11-09",
                                    "note": "",
                                    "language_code": "en"
                                }
                            ],
                            "type": "email",
                            "value": "sweester@sinarproject",
                            "valid_from": "2015-11-03",
                            "valid_until": "2015-11-03",
                            "created_at": "2015-11-03",
                            "updated_at": "2015-11-09",
                            "label": "",
                            "note": "",
                            "language_code": "en"
                        }
                    ],
                    "links": [
                        {
                            "id": "ce15a9ee-6742-4467-bbfb-c86459ee685b",
                            "label": "",
                            "field": "",
                            "url": "http://www.talklikeapirate.com/howto.html#basic",
                            "created_at": "2015-11-03",
                            "updated_at": "2015-11-03",
                            "note": "",
                            "language_code": "en"
                        }
                    ],
                    "start_date": "2008-05-08",
                    "end_date": "2013-05-05",
                    "created_at": "2015-11-03T00:58:25.398456Z",
                    "updated_at": "2015-11-03T00:58:25.398478Z",
                    "label": "",
                    "role": "member",
                    "language_code": "en"
                },
                "post_id": "c1f0f86b-a491-4986-b48d-861b58a3ef6e",
                "contact_details": [],
                "links": [],
                "start_date": None,
                "end_date": None,
                "created_at": "2015-11-13T01:37:07.640696Z",
                "updated_at": "2015-11-13T01:41:47.306960Z",
                "label": "Swee meng scaly wag",
                "role": "",
                "language_code": "en"
            }
        ]
        response = self.client.get("/en/search/memberships/", params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

    @patch("popit_search.utils.search.SerializerSearch.search")
    def test_post_search(self, mock_search):
        params = {
            "q": "id:c1f0f86b-a491-4986-b48d-861b58a3ef6e"
        }
        mock_search.return_value = [
            {
                "id": "2c6982c2-504a-4e0d-8949-dade5f9e494e",
                "other_labels": [],
                "organization": {
                    "id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
                    "parent": {
                        "id": "612943b1-864d-4188-8d79-ca387ed19b32",
                        "other_names": [],
                        "identifiers": [],
                        "links": [],
                        "contact_details": [],
                        "area": None,
                        "founding_date": "2013-09-01",
                        "dissolution_date": "2020-09-01",
                        "image": "",
                        "created_at": "2015-10-21T23:22:00.443496Z",
                        "updated_at": "2015-10-21T23:22:44.583911Z",
                        "parent": None,
                        "name": "Pirate Party",
                        "classification": "political party",
                        "abstract": "pirates",
                        "description": "arrrrrr",
                        "language_code": "en"
                    },
                    "parent_id": "612943b1-864d-4188-8d79-ca387ed19b32",
                    "other_names": [
                        {
                            "id": "53a22b00-1383-4bf5-b4be-4753d8d16062",
                            "links": [
                                {
                                    "id": "fe662497-c24d-4bbb-a72d-feb77319782a",
                                    "label": "",
                                    "field": "name",
                                    "url": "http://sinarproject.org",
                                    "created_at": "2015-10-26",
                                    "updated_at": "2015-10-26",
                                    "note": "",
                                    "language_code": "en"
                                }
                            ],
                            "start_date": None,
                            "end_date": None,
                            "created_at": "2015-10-22",
                            "updated_at": "2015-10-22",
                            "note": "really othername field don't seems appropriate for organization",
                            "name": "Not Sinar Project",
                            "family_name": "",
                            "given_name": "",
                            "additional_name": "",
                            "honorific_prefix": "",
                            "honorific_suffix": "",
                            "patronymic_name": "",
                            "language_code": "en"
                        }
                    ],
                    "identifiers": [
                        {
                            "id": "2d3b8d2c-77b8-42f5-ac62-3e83d4408bda",
                            "links": [
                                {
                                    "id": "02369098-7b46-4d62-9318-a5f1c2d385bd",
                                    "label": "",
                                    "field": "identifier",
                                    "url": "http://ssm.com",
                                    "created_at": "2015-10-26",
                                    "updated_at": "2015-10-26",
                                    "note": "",
                                    "language_code": "en"
                                }
                            ],
                            "identifier": "3131312",
                            "created_at": "2015-10-22",
                            "updated_at": "2015-10-22",
                            "scheme": "ssm",
                            "language_code": "en"
                        }
                    ],
                    "links": [
                        {
                            "id": "45b0a790-8c9e-4553-844b-431ed34b6b12",
                            "label": "",
                            "field": "",
                            "url": "https://github.com/sweemeng/",
                            "created_at": "2015-10-22",
                            "updated_at": "2015-10-22",
                            "note": "Web page of the party leader",
                            "language_code": "en"
                        }
                    ],
                    "contact_details": [
                        {
                            "id": "651da7cd-f109-4aaa-b04c-df835fb6831f",
                            "links": [
                                {
                                    "id": "26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf",
                                    "label": "",
                                    "field": "type",
                                    "url": "http://sinarproject.org/about/",
                                    "created_at": "2015-10-26",
                                    "updated_at": "2015-11-09",
                                    "note": "",
                                    "language_code": "en"
                                }
                            ],
                            "type": "phone",
                            "value": "0129123132112",
                            "valid_from": "2015-10-22",
                            "valid_until": "2020-10-22",
                            "created_at": "2015-10-22",
                            "updated_at": "2015-11-09",
                            "label": "sinar project phone",
                            "note": "just a phone",
                            "language_code": "en"
                        }
                    ],
                    "area": {
                        "id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
                        "links": [
                            {
                                "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
                                "label": "",
                                "field": "",
                                "url": "http://en.wikipedia.com",
                                "created_at": "2015-10-30",
                                "updated_at": "2015-10-30",
                                "note": "",
                                "language_code": "en"
                            }
                        ],
                        "identifier": "",
                        "created_at": "2015-10-21T23:44:40.750284Z",
                        "updated_at": "2015-10-21T23:44:40.750308Z",
                        "parent": "4775c9b6-f8fd-4cdc-bda8-a1844fa7f8ea",
                        "name": "kuala lumpur",
                        "classification": "",
                        "language_code": "en"
                    },
                    "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
                    "founding_date": "2015-10-22",
                    "dissolution_date": "2020-10-22",
                    "image": "",
                    "created_at": "2015-10-21T23:46:14.589608Z",
                    "updated_at": "2015-10-21T23:48:16.167211Z",
                    "name": "Pirate Party KL",
                    "classification": "political party",
                    "abstract": "KL Branch of Pirate Party",
                    "description": "KL Branch of Pirate Party",
                    "language_code": "en"
                },
                "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
                "area": None,
                "area_id": None,
                "contact_details": [],
                "links": [],
                "start_date": None,
                "end_date": None,
                "created_at": "2015-11-03T01:05:47.328900Z",
                "updated_at": "2015-11-03T01:05:47.328925Z",
                "label": "",
                "role": "Captain",
                "language_code": "en"
            }
        ]
        response = self.client.get("/en/search/posts/", params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

