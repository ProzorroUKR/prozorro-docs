# -*- coding: utf-8 -*-
import os
from copy import deepcopy
from datetime import timedelta
from freezegun import freeze_time
from openprocurement.api.utils import get_now
from openprocurement.planning.api.tests.base import BasePlanWebTest
from tests.base.data import plan
from openprocurement.tender.belowthreshold.tests.base import test_tender_data
from tests.base.data import tender_openeu
from tests.base.constants import DOCS_URL
from tests.base.test import DumpsWebTestApp, MockWebTestMixin

TARGET_DIR = 'docs/source/centralized-procurements/http/'

test_plan_data = deepcopy(plan)
tender_openeu = deepcopy(tender_openeu)
test_tender_data = deepcopy(test_tender_data)


class PlanResourceTest(BasePlanWebTest, MockWebTestMixin):
    AppClass = DumpsWebTestApp

    relative_to = os.path.dirname(__file__)
    initial_data = test_plan_data
    docservice = True
    docservice_url = DOCS_URL

    def setUp(self):
        super(PlanResourceTest, self).setUp()
        self.setUpMock()

    def tearDown(self):
        self.tearDownMock()
        super(PlanResourceTest, self).tearDown()

    def create_plan(self):
        pass

    def test_docs(self):
        self.app.authorization = ('Basic', ('broker', ''))
        # empty plans listing
        response = self.app.get('/plans')
        self.assertEqual(response.json['data'], [])

        # create plan
        test_plan_data['status'] = "draft"
        test_plan_data['tender'].update({"tenderPeriod": {"startDate": (get_now() + timedelta(days=7)).isoformat()}})
        test_plan_data['items'][0].update({"deliveryDate": {"endDate": (get_now() + timedelta(days=15)).isoformat()}})
        test_plan_data['items'] = test_plan_data['items'][:1]

        test_plan_data["buyers"] = [deepcopy(test_plan_data["procuringEntity"])]  # just to be sure

        test_plan_data["procuringEntity"] = {
            "identifier": {
                "scheme": "UA-EDR",
                "id": "111111",
                "legalName": "ДП Центральний закупівельний орган №1"
            },
            "name": "ЦЗО №1"
        }
        test_plan_data["tender"]["procurementMethod"] = ""
        test_plan_data["tender"]["procurementMethodType"] = "centralizedProcurement"

        with freeze_time("2019-05-02 01:00:00"):
            with open(TARGET_DIR + 'create-plan.http', 'w') as self.app.file_obj:
                response = self.app.post_json(
                    '/plans?opt_pretty=1',
                    {'data': test_plan_data})
        self.assertEqual(response.status, '201 Created')

        plan = response.json['data']
        self.plan_id = plan["id"]
        owner_token = response.json['access']['token']

        with freeze_time("2019-05-02 01:01:00"):
            with open(TARGET_DIR + 'patch-plan-status-scheduled.http', 'w') as self.app.file_obj:
                response = self.app.patch_json(
                    '/plans/{}?acc_token={}'.format(plan['id'], owner_token),
                    {'data': {"status": "scheduled"}}
                )
        self.assertEqual(response.json["data"]["status"], "scheduled")
        # self.assertEqual(len(response.json["data"]["milestones"]), 1)
        #
        # milestone = response.json["data"]["milestones"][0]
        # with freeze_time("2019-05-02 01:02:00"):
        #     with open(TARGET_DIR + 'patch-plan-milestone-met.http', 'w') as self.app.file_obj:
        #         response = self.app.patch_json(
        #             '/plans/{}/milestones/{}'.format(plan['id'], milestone["id"]),
        #             {'data': {"status": "met"}}
        #         )
        # self.assertEqual(response.json["data"]["status"], "met")
        #
        # # tender creation
        # procuring_entity = deepcopy(test_plan_data["procuringEntity"])
        # procuring_entity["kind"] = "central"
        # procuring_entity.update(
        #     contactPoint=dict(name=u"Довідкова", telephone="0440000000"),
        #     address=test_tender_data["procuringEntity"]["address"],
        # )
        # test_tender_data["procuringEntity"] = procuring_entity
        # test_tender_data["buyers"] = test_plan_data["buyers"]
        #
        # with freeze_time("2019-05-12 09:00:00"):
        #     with open(TARGET_DIR + 'create-tender.http', 'w') as self.app.file_obj:
        #         response = self.app.post_json(
        #             '/tenders',
        #             {'data': test_tender_data}
        #         )
        # self.assertEqual(response.status, '201 Created')

