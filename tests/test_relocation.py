# -*- coding: utf-8 -*-
import os

from copy import deepcopy
from datetime import timedelta
from uuid import uuid4
from hashlib import sha512

from openprocurement.tender.belowthreshold.tests.base import (
    BaseTenderWebTest,
    test_tender_data,
    test_organization,
    test_author)
from openprocurement.tender.openeu.constants import TENDERING_DAYS
from openprocurement.contracting.api.tests.base import test_contract_data
from openprocurement.tender.competitivedialogue.tests.base import (
    BaseCompetitiveDialogWebTest,
    test_tender_stage2_data_ua,
    test_access_token_stage1)
from openprocurement.tender.openeu.models import TENDERING_DURATION
from openprocurement.api.models import get_now

from tests.base.test import DumpsWebTestApp, MockWebTestMixin


class TransferDocsTest(BaseTenderWebTest, MockWebTestMixin):
    AppClass = DumpsWebTestApp

    relative_to = os.path.dirname(__file__)

    def setUp(self):
        super(TransferDocsTest, self).setUp()
        self.setUpMock()

    def tearDown(self):
        self.tearDownMock()
        super(TransferDocsTest, self).tearDown()

    def create_tender(self):
        pass

    def test_docs(self):
        data = deepcopy(test_tender_data)
        now = get_now()
        data['items'][0].update({"deliveryDate": {
             "startDate": (now + timedelta(days=2)).isoformat(),
             "endDate": (now + timedelta(days=5)).isoformat()}})
        data.update({
            "enquiryPeriod": {"endDate": (now + timedelta(days=7)).isoformat()},
            "tenderPeriod": {"endDate": (now + timedelta(days=14)).isoformat()}})
        self.app.authorization = ('Basic', ('broker', ''))

        with open('docs/source/relocation/tutorial/create-tender.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/tenders?opt_pretty=1', {"data": data})
            self.assertEqual(response.status, '201 Created')

        tender = response.json['data']
        self.tender_id = tender['id']
        owner_token = response.json['access']['token']
        orig_tender_transfer_token = response.json['access']['transfer']

        self.app.authorization = ('Basic', ('broker1', ''))

        with open('docs/source/relocation/tutorial/create-transfer.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/transfers', {"data": {}})
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')
            transfer = response.json['data']
            new_access_token = response.json['access']['token']
            new_transfer_token = response.json['access']['transfer']

        with open('docs/source/relocation/tutorial/get-transfer.http', 'w') as self.app.file_obj:
            response = self.app.get('/transfers/{}'.format(transfer['id']))

        with open('docs/source/relocation/tutorial/change-tender-ownership.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/tenders/{}/ownership'.format(self.tender_id),
                                          {"data": {"id": transfer['id'], 'transfer': orig_tender_transfer_token}})
            self.assertEqual(response.status, '200 OK')
            self.assertNotIn('transfer', response.json['data'])
            self.assertNotIn('transfer_token', response.json['data'])
            self.assertEqual('broker1', response.json['data']['owner'])

        with open('docs/source/relocation/tutorial/get-used-transfer.http', 'w') as self.app.file_obj:
            response = self.app.get('/transfers/{}'.format(transfer['id']))

        with open('docs/source/relocation/tutorial/modify-tender.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/tenders/{}?acc_token={}'.format(self.tender_id, new_access_token),
                                           {"data": {"description": "broker1 now can change the tender"}})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.json['data']['description'], 'broker1 now can change the tender')


        ########################
        # Contracting transfer #
        ########################

        test_tender_token = uuid4().hex
        data = deepcopy(test_contract_data)
        data.update({
            u"dateSigned": get_now().isoformat(),
            u"id": uuid4().hex,
            u"tender_id": uuid4().hex,
            u"tender_token": sha512(test_tender_token).hexdigest()
        })
        tender_token = data['tender_token']
        self.app.authorization = ('Basic', ('contracting', ''))

        response = self.app.post_json('/contracts', {'data': data})
        self.assertEqual(response.status, '201 Created')
        self.contract = response.json['data']
        self.assertEqual('broker', response.json['data']['owner'])
        self.contract_id = self.contract['id']

        self.app.authorization = ('Basic', ('broker', ''))
        with open('docs/source/relocation/tutorial/get-contract-transfer.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                '/contracts/{}/credentials?acc_token={}'.format(self.contract_id, tender_token),
                {'data': ''})
            self.assertEqual(response.status, '200 OK')
            token = response.json['access']['token']
            self.contract_transfer = response.json['access']['transfer']

        self.app.authorization = ('Basic', ('broker3', ''))
        with open('docs/source/relocation/tutorial/create-contract-transfer.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/transfers', {"data": {}})
            self.assertEqual(response.status, '201 Created')
            transfer = response.json['data']
            self.assertIn('date', transfer)
            transfer_creation_date = transfer['date']
            new_access_token = response.json['access']['token']
            new_transfer_token = response.json['access']['transfer']

        with open('docs/source/relocation/tutorial/change-contract-ownership.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/contracts/{}/ownership'.format(self.contract_id),
                                          {"data": {"id": transfer['id'], 'transfer': self.contract_transfer}})
            self.assertEqual(response.status, '200 OK')
            self.assertNotIn('transfer', response.json['data'])
            self.assertNotIn('transfer_token', response.json['data'])
            self.assertEqual('broker3', response.json['data']['owner'])

        with open('docs/source/relocation/tutorial/modify-contract.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/contracts/{}?acc_token={}'.format(self.contract_id, new_access_token),
                                           {"data": {"description": "broker3 now can change the contract"}})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.json['data']['description'], 'broker3 now can change the contract')

        with open('docs/source/relocation/tutorial/get-used-contract-transfer.http', 'w') as self.app.file_obj:
            response = self.app.get('/transfers/{}'.format(transfer['id']))
