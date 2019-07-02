# -*- coding: utf-8 -*-
import os

from copy import deepcopy
from datetime import timedelta
from uuid import uuid4
from hashlib import sha512

from openprocurement.tender.belowthreshold.tests.base import (
    test_tender_data,
    test_organization,
    test_author)
from openprocurement.relocation.api.tests.base import (
    OwnershipWebTest,
    OpenEUOwnershipWebTest,
    test_ua_bid_data)
from openprocurement.tender.openeu.constants import TENDERING_DAYS
from openprocurement.tender.openeu.tests.base import test_tender_data as test_eu_tender_data
from openprocurement.contracting.api.tests.base import test_contract_data
from openprocurement.tender.competitivedialogue.tests.base import (
    BaseCompetitiveDialogWebTest,
    test_tender_stage2_data_ua,
    test_access_token_stage1)
from openprocurement.tender.openeu.models import TENDERING_DURATION
from openprocurement.api.models import get_now

from tests.base.test import DumpsWebTestApp, MockWebTestMixin


class TransferDocsTest(OwnershipWebTest, MockWebTestMixin):
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

        #################
        # Bid ownership #
        #################

        self.set_tendering_status()

        self.tick()

        self.app.authorization = ('Basic', ('broker', ''))
        with open('docs/source/relocation/tutorial/create-bid.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/tenders/{}/bids'.format(
                self.tender_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')
            bid = response.json['data']
            bid_tokens = response.json['access']

        self.app.authorization = ('Basic', ('broker2', ''))

        with open('docs/source/relocation/tutorial/create-bid-transfer.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/transfers', {"data": {}})
            self.assertEqual(response.status, '201 Created')
            transfer = response.json['data']
            transfer_tokens = response.json['access']

        with open('docs/source/relocation/tutorial/change-bid-ownership.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/tenders/{}/bids/{}/ownership'.format(self.tender_id, bid['id']),
                                          {"data": {"id": transfer['id'], 'transfer': bid_tokens['transfer']}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/relocation/tutorial/modify-bid.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                '/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], transfer_tokens['token']),
                {"data": {'value': {"amount": 450}}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/relocation/tutorial/get-used-bid-transfer.http', 'w') as self.app.file_obj:
            response = self.app.get('/transfers/{}'.format(transfer['id']))

        #######################
        # Complaint ownership #
        #######################

        self.app.authorization = ('Basic', ('broker2', ''))

        with open('docs/source/relocation/tutorial/create-complaint.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/tenders/{}/complaints'.format(self.tender_id), {
                'data': {'title': 'complaint title', 'description': 'complaint description',
                         'author': test_author, 'status': 'claim'}})
            self.assertEqual(response.status, '201 Created')
            complaint = response.json['data']
            complaint_token = response.json['access']['token']
            complaint_transfer = response.json['access']['transfer']

        self.app.authorization = ('Basic', ('broker', ''))

        with open('docs/source/relocation/tutorial/create-complaint-transfer.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/transfers', {"data": {}})
            self.assertEqual(response.status, '201 Created')
            transfer = response.json['data']
            transfer_tokens = response.json['access']

        with open('docs/source/relocation/tutorial/change-complaint-ownership.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/tenders/{}/complaints/{}/ownership'.format(self.tender_id, complaint['id']),
                                          {"data": {"id": transfer['id'], 'transfer': complaint_transfer}})
            self.assertEqual(response.status, '200 OK')
            complaint_transfer = transfer_tokens['transfer']

        with open('docs/source/relocation/tutorial/modify-complaint.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                '/tenders/{}/complaints/{}?acc_token={}'.format(self.tender_id, complaint['id'],
                                                                transfer_tokens['token']),
                {"data": {'status': 'cancelled', 'cancellationReason': 'Important reason'}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/relocation/tutorial/get-used-complaint-transfer.http', 'w') as self.app.file_obj:
            response = self.app.get('/transfers/{}'.format(transfer['id']))

        #############################
        # Award complaint ownership #
        #############################

        self.app.authorization = ('Basic', ('broker2', ''))

        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'tenderers': [test_organization], "value": {"amount": 350}}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bid = response.json['data']
        bid_tokens = response.json['access']

        self.set_qualification_status()
        self.app.authorization = ('Basic', ('token', ''))
        response = self.app.post_json('/tenders/{}/awards'.format(
            self.tender_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': bid['id']}})
        award = response.json['data']
        self.award_id = award['id']

        self.app.authorization = ('Basic', ('broker2', ''))

        with open('docs/source/relocation/tutorial/create-award-complaint.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/tenders/{}/awards/{}/complaints?acc_token={}'.format(self.tender_id, self.award_id,
                                                                       bid_tokens['token']), {
                    'data': {'title': 'complaint title', 'description': 'complaint description',
                             'author': test_author, 'status': 'claim'}})
            self.assertEqual(response.status, '201 Created')
            complaint = response.json['data']
            complaint_token = response.json['access']['token']
            complaint_transfer = response.json['access']['transfer']

        self.app.authorization = ('Basic', ('broker', ''))

        with open('docs/source/relocation/tutorial/create-award-complaint-transfer.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/transfers', {"data": {}})
            self.assertEqual(response.status, '201 Created')
            transfer = response.json['data']
            transfer_tokens = response.json['access']

        with open('docs/source/relocation/tutorial/change-award-complaint-ownership.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/tenders/{}/awards/{}/complaints/{}/ownership'.format(self.tender_id, self.award_id, complaint['id']),
                {"data": {"id": transfer['id'], 'transfer': complaint_transfer}})
            self.assertEqual(response.status, '200 OK')
            complaint_transfer = transfer_tokens['transfer']

        with open('docs/source/relocation/tutorial/modify-award-complaint.http', 'w') as self.app.file_obj:
            response = self.app.patch_json(
                '/tenders/{}/awards/{}/complaints/{}?acc_token={}'.format(self.tender_id, self.award_id,
                                                                          complaint['id'], transfer_tokens['token']),
                {"data": {'status': 'cancelled', 'cancellationReason': 'Important reason'}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/relocation/tutorial/get-used-award-complaint-transfer.http', 'w') as self.app.file_obj:
            response = self.app.get('/transfers/{}'.format(transfer['id']))

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

        # Create Transfer
        with open('docs/source/relocation/tutorial/create-contract-transfer-credentials.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/transfers', {"data": {}})
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')
            transfer = response.json['data']
            contract_token = response.json['access']['token']
            new_transfer_token = response.json['access']['transfer']

        # Getting access
        with open('docs/source/relocation/tutorial/change-contract-credentials.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/contracts/{}/ownership'.format(self.contract_id),
                                          {"data": {"id": transfer['id'], 'tender_token': test_tender_token}})
            self.assertEqual(response.status, '200 OK')
            self.assertNotIn('transfer', response.json['data'])
            self.assertNotIn('transfer_token', response.json['data'])
            self.assertEqual('broker3', response.json['data']['owner'])

        # Check Transfer is used
        with open('docs/source/relocation/tutorial/get-used-contract-credentials-transfer.http', 'w') as self.app.file_obj:
            response = self.app.get('/transfers/{}'.format(transfer['id']))

        # Modify contract with new credentials
        with open('docs/source/relocation/tutorial/modify-contract-credentials.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/contracts/{}?acc_token={}'.format(self.contract_id, contract_token),
                                           {"data": {"description": "new credentials works"}})
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.json['data']['description'], 'new credentials works')


class EuTransferDocsTest(OpenEUOwnershipWebTest, MockWebTestMixin):
    AppClass = DumpsWebTestApp

    relative_to = os.path.dirname(__file__)

    def setUp(self):
        super(EuTransferDocsTest, self).setUp()
        self.setUpMock()

    def tearDown(self):
        self.tearDownMock()
        super(EuTransferDocsTest, self).tearDown()

    def create_tender(self):
        pass

    def test_eu_procedure(self):
        ##############################
        # Qualification owner change #
        ##############################

        self.app.authorization = ('Basic', ('broker', ''))
        now = get_now()
        data = deepcopy(test_eu_tender_data)
        data['items'][0].update({"deliveryDate": {
             "startDate": (now + timedelta(days=2)).isoformat(),
             "endDate": (now + timedelta(days=5)).isoformat()}})
        data.update({"tenderPeriod": {"endDate": (now + timedelta(days=TENDERING_DAYS + 1)).isoformat()}})
        with open('docs/source/relocation/tutorial/create-tender-for-qualification.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/tenders?opt_pretty=1', {"data": data})
            self.assertEqual(response.status, '201 Created')
            tender = response.json['data']
            self.tender_token = response.json['access']['token']
            self.tender_id = tender['id']
        self.set_tendering_status()
        self.tick()
        # broker(tender owner) create bid
        with open('docs/source/relocation/tutorial/create-first-bid-for-qualification.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), test_ua_bid_data)
            self.assertEqual(response.status, '201 Created')
            bid1_token = response.json['access']['token']

        # broker4 create bid
        auth = self.app.authorization
        self.app.authorization = ('Basic', ('broker4', ''))
        response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), test_ua_bid_data)
        self.assertEqual(response.status, '201 Created')
        bid2_id = response.json['data']['id']
        bid2_token = response.json['access']['token']
        # broker change status to pre-qualification
        self.set_pre_qualification_status()
        self.tick()
        self.app.authorization = ('Basic', ('chronograph', ''))
        response = self.app.patch_json('/tenders/{}'.format(self.tender_id), {"data": {"id": self.tender_id}})
        self.app.authorization = auth

        # qualifications
        response = self.app.get('/tenders/{}/qualifications'.format(self.tender_id))
        self.assertEqual(response.status, "200 OK")
        qualifications = response.json['data']
        for qualification in qualifications:
            response = self.app.patch_json(
                '/tenders/{}/qualifications/{}?acc_token={}'.format(self.tender_id, qualification['id'],
                                                                    self.tender_token),
                {"data": {"status": "active", "qualified": True, "eligible": True}})
            self.assertEqual(response.status, "200 OK")
        # active.pre-qualification.stand-still
        response = self.app.patch_json('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token),
                                       {"data": {"status": "active.pre-qualification.stand-still"}})
        self.assertEqual(response.status, "200 OK")
        self.assertEqual(response.json['data']['status'], "active.pre-qualification.stand-still")
        qualification_id = qualifications[0]['id']
        # broker4 create complaint
        self.app.authorization = ('Basic', ('broker4', ''))
        with open('docs/source/relocation/tutorial/create-qualification-complaint.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/tenders/{}/qualifications/{}/complaints?acc_token={}'.format(self.tender_id, qualification_id,
                                                                               bid2_token),
                {'data': {'title': 'complaint title', 'description': 'complaint description',
                          'author': test_author, 'status': 'claim'}})
            self.assertEqual(response.status, '201 Created')
            complaint_id = response.json["data"]["id"]
            complaint_transfer = response.json['access']['transfer']

        # broker4 create Transfer
        self.app.authorization = ('Basic', ('broker4', ''))
        with open('docs/source/relocation/tutorial/create-qualification-complaint-transfer.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/transfers', {"data": {}})
            self.assertEqual(response.status, '201 Created')
            transfer = response.json['data']
            self.assertIn('date', transfer)
            transfer = response.json['data']
            transfer_tokens = response.json['access']

        with open('docs/source/relocation/tutorial/change-qualification-complaint-owner.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/tenders/{}/qualifications/{}/complaints/{}/ownership'.format(self.tender_id, qualification_id,
                                                                               complaint_id),
                {"data": {"id": transfer['id'], 'transfer': complaint_transfer}})
            self.assertEqual(response.status, '200 OK')


class CompetitiveDialogueStage2TransferDocsTest(BaseCompetitiveDialogWebTest, MockWebTestMixin):
    AppClass = DumpsWebTestApp

    relative_to = os.path.dirname(__file__)

    def setUp(self):
        super(CompetitiveDialogueStage2TransferDocsTest, self).setUp()
        self.setUpMock()

    def tearDown(self):
        self.tearDownMock()
        super(CompetitiveDialogueStage2TransferDocsTest, self).tearDown()

    def create_tender(self):
        pass

    def test_stage2(self):
        # create tender with bridge
        self.app.authorization = ('Basic', ('competitive_dialogue', ''))
        now = get_now()
        data = deepcopy(test_tender_stage2_data_ua)
        data['items'][0].update({"deliveryDate": {
            "startDate": (now + timedelta(days=2)).isoformat(),
            "endDate": (now + timedelta(days=5)).isoformat()}})
        data.update({
            "tenderPeriod": {"endDate": (now + timedelta(days=TENDERING_DAYS + 1)).isoformat()},
            "dialogueID": uuid4().hex})
        response = self.app.post_json('/tenders?opt_pretty=1', {"data": data})
        self.assertEqual(response.status, '201 Created')
        self.tender_id = response.json['data']['id']
        tender = response.json['data']

        # get credentials of tender
        self.app.authorization = ('Basic', ('broker', ''))
        self.set_status('draft.stage2')

        response = self.app.patch_json(
            '/tenders/{}/credentials?acc_token={}&opt_pretty=1'.format(self.tender_id, test_access_token_stage1))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.json['data']['status'], 'draft.stage2')
        tender_transfer_token = response.json['access']['transfer']

        # change tender owner
        self.app.authorization = ('Basic', ('broker3', ''))
        with open('docs/source/relocation/tutorial/create-transfer-stage2.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/transfers', {"data": {}})
            self.assertEqual(response.status, '201 Created')
            transfer = response.json['data']
            self.assertIn('date', transfer)
            new_access_token = response.json['access']['token']
            new_transfer_token = response.json['access']['transfer']

        with open('docs/source/relocation/tutorial/change-tender-ownership-stage2.http', 'w') as self.app.file_obj:
            response = self.app.post_json('/tenders/{}/ownership'.format(self.tender_id),
                                          {"data": {"id": transfer['id'], 'transfer': tender_transfer_token}})
            self.assertEqual(response.status, '200 OK')
            self.assertNotIn('transfer', response.json['data'])
            self.assertNotIn('transfer_token', response.json['data'])
            self.assertEqual('broker3', response.json['data']['owner'])

        # broker3 can change the tender
        with open('docs/source/relocation/tutorial/modify-tender-stage2.http', 'w') as self.app.file_obj:
            now = get_now()
            response = self.app.patch_json('/tenders/{}?acc_token={}'.format(self.tender_id, new_access_token),
                                           {"data": {
                                               "tenderPeriod": {"endDate": (now + TENDERING_DURATION).isoformat()}}})
            self.assertEqual(response.status, '200 OK')
            self.assertNotIn('transfer', response.json['data'])
            self.assertNotIn('transfer_token', response.json['data'])
            self.assertIn('owner', response.json['data'])
            self.assertEqual(response.json['data']['owner'], 'broker3')
            self.assertEqual(response.json['data']["tenderPeriod"]['endDate'], (now + TENDERING_DURATION).isoformat())
