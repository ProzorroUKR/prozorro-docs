# -*- coding: utf-8 -*-
import os

import openprocurement.planning.api.tests.base as base_test
from openprocurement.planning.api.tests.base import BasePlanWebTest
from openprocurement.planning.api.tests.base import test_plan_data

from tests.base import DumpsWebTestApp, DOCS_HOST

TARGET_DIR = 'docs/source/planning/tutorial/'


class PlanResourceTest(BasePlanWebTest):
    initial_data = test_plan_data
    docservice = True

    docs_host = DOCS_HOST

    def setUp(self):
        self.app = DumpsWebTestApp("config:tests.ini", relative_to=os.path.dirname(base_test.__file__))
        self.couchdb_server = self.app.app.registry.couchdb_server
        self.db = self.app.app.registry.db
        if self.docservice:
            self.setUpDS()
            self.app.app.registry.docservice_url = 'http://{}'.format(self.docs_host)

    def tearDown(self):
        self.couchdb_server.delete(self.db.name)

    def generate_docservice_url(self):
        url = super(PlanResourceTest, self).generate_docservice_url()
        return url.replace('localhost', self.docs_host)

    def test_docs(self):
        self.app.authorization = ('Basic', ('broker', ''))
        # empty plans listing
        response = self.app.get('/plans')
        self.assertEqual(response.json['data'], [])

        # create plan
        with open(TARGET_DIR + 'create-plan.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/plans?opt_pretty=1',
                {'data': test_plan_data})
            self.assertEqual(response.status, '201 Created')

        plan = response.json['data']
        plan_id = self.plan_id = response.json['data']['id']
        owner_token = response.json['access']['token']

        with open(TARGET_DIR + 'example_plan.http', 'w') as self.app.file_obj:
            response = self.app.get('/plans/{}'.format(plan_id))

        with open(TARGET_DIR + 'plan-listing.http', 'w') as self.app.file_obj:
            self.app.authorization = None
            response = self.app.get('/plans')
            self.assertEqual(response.status, '200 OK')
            self.app.file_obj.write("\n")

        self.app.authorization = ('Basic', ('broker', ''))
        with open(TARGET_DIR + 'patch-plan-procuringEntity-name.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                '/plans/{}?acc_token={}'.format(plan['id'], owner_token),
                {'data':
                    {"items": [
                        {
                            "description": "Насіння овочевих культур",
                            "classification": {
                                "scheme": "ДК021",
                                "description": "Vegetable seeds",
                                "id": "03111700-9"
                            },
                            "additionalClassifications": [
                                {
                                    "scheme": "ДКПП",
                                    "id": "01.13.6",
                                    "description": "Насіння овочевих культур"
                                }
                            ],
                            "deliveryDate": {
                                "endDate": "2016-06-01T23:06:30.023018+03:00"
                            },
                            "unit": {
                                "code": "KGM",
                                "name": "кг"
                            },
                            "quantity": 5000
                        }
                    ]}
                })

        with open(TARGET_DIR + 'plan-listing-after-patch.http', 'w') as self.app.file_obj:
            self.app.authorization = None
            response = self.app.get('/plans')
            self.assertEqual(response.status, '200 OK')
            self.app.file_obj.write("\n")
