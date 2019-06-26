.. _tutorial:

Tutorial
========

When customer needs to change current broker this customer should provide new preferred broker with ``transfer`` key for an object (tender, bid, complaint, etc.). Then new broker should create `Transfer` object and send request with `Transfer` ``id`` and ``transfer`` key (received from customer) in order to change object's owner.

Examples for Tender
-------------------

Tender ownership change
~~~~~~~~~~~~~~~~~~~~~~~

Let's view transfer example for tender.


Tender creation
^^^^^^^^^^^^^^^

At first let's create a tender:

.. include:: tutorial/create-tender.http
   :code:

`broker` is current tender's ``owner``.

Note that response's `access` section contains a ``transfer`` key which is used to change tender ownership. 

After tender's registration in CDB broker has to provide its customer with ``transfer`` key.

Transfer creation
^^^^^^^^^^^^^^^^^

Broker that is going to become new tender owner should create a `Transfer`.

.. include:: tutorial/create-transfer.http
   :code:

`Transfer` object contains new access ``token`` and new ``transfer`` token for the object that will be transferred to new broker.

`Transfer` can be retrieved by `id`:

.. include:: tutorial/get-transfer.http
   :code:

Changing tender's owner
^^^^^^^^^^^^^^^^^^^^^^^

Pay attention that only broker with appropriate accreditation level can become new owner. Otherwise broker will be forbidden from this action.

To change tender's ownership new broker should send POST request to appropriate `/tenders/id/` with `data` section containing ``id`` of `Transfer` and ``transfer`` token received from customer:

.. include:: tutorial/change-tender-ownership.http
   :code:

Updated ``owner`` value indicates that ownership is successfully changed. 

Note that new broker has to provide its customer with new ``transfer`` key (generated in `Transfer` object).

After `Transfer` is applied it stores tender path in ``usedFor`` property:

.. include:: tutorial/get-used-transfer.http
   :code:

'Used' `Transfer` can't be applied to any other object.

Let's try to change the tender using ``token`` received on `Transfer` creation:

.. include:: tutorial/modify-tender.http
   :code:
   

Bid ownership change
~~~~~~~~~~~~~~~~~~~~

Let's submit a bid via current broker:

.. include:: tutorial/create-bid.http
   :code:

Response contains `access` section with a ``transfer`` key that can be used to change bid ownership.

Current broker has to provide its customer with ``transfer`` key for the bid. Then customer can pass it to new broker.
   
Transfer creation
^^^^^^^^^^^^^^^^^

Note that each `Transfer` can be applied only once. New broker (that is going to become new bid owner) should create separate `Transfer` for each owner change:

.. include:: tutorial/create-bid-transfer.http
   :code:

`Transfer` object contains new access ``token`` and new ``transfer`` key for the object that will be transferred to new broker.
   
Changing bid's owner
^^^^^^^^^^^^^^^^^^^^

Pay attention that only broker with appropriate accreditation level can become new owner. Otherwise broker will be forbidden from this action.

New broker should send POST request to appropriate `/tenders/id/bids/id` with `data` section containing ``id`` of `Transfer` and ``transfer`` key for the bid received from customer:

.. include:: tutorial/change-bid-ownership.http
   :code:

Now new broker became bid owner. Check whether new owner is able to change the bid:

.. include:: tutorial/modify-bid.http
   :code:
   
New broker should provide its customer with new ``transfer`` key (received within `Transfer` object).

Check whether `Transfer` object has successfully stored bid path in ``usedFor`` property:

.. include:: tutorial/get-used-bid-transfer.http
   :code:

   
Complaint ownership change
~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's submit a complaint via current broker:

.. include:: tutorial/create-complaint.http
   :code:

Response contains `access` section with a ``transfer`` key that can be used to change complaint ownership.

Current broker has to provide its customer with ``transfer`` key for the complaint. Then customer can pass it to new broker.

Transfer creation
^^^^^^^^^^^^^^^^^

Note that each `Transfer` can be applied only once. New broker (that is going to become new complaint owner) should create separate `Transfer` for each owner change:

.. include:: tutorial/create-complaint-transfer.http
   :code:

`Transfer` object contains new access ``token`` and new ``transfer`` key for the object that will be transferred to new broker.

Changing complaint's owner
^^^^^^^^^^^^^^^^^^^^^^^^^^

Pay attention that only broker with appropriate accreditation level can become new owner. Otherwise broker will be forbidden from this action.

New broker should send POST request to appropriate `/tenders/id/complaints/id` with `data` section containing ``id`` of `Transfer` and ``transfer`` key for the complaint received from customer:

.. include:: tutorial/change-complaint-ownership.http
   :code:

Now new broker became complaint owner. Check whether new owner is able to change the complaint:

.. include:: tutorial/modify-complaint.http
   :code:

New broker should provide its customer with new ``transfer`` key (received within `Transfer` object).

Check whether `Transfer` object has successfully stored complaint path in ``usedFor`` property:

.. include:: tutorial/get-used-complaint-transfer.http
   :code:

Award complaint ownership change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's submit a award complaint via current broker:

.. include:: tutorial/create-award-complaint.http
   :code:

Response contains `access` section with a ``transfer`` key that can be used to change complaint ownership.

Current broker has to provide its customer with ``transfer`` key for the complaint. Then customer can pass it to new broker.

Transfer creation
^^^^^^^^^^^^^^^^^

Note that each `Transfer` can be applied only once. New broker (that is going to become new complaint owner) should create separate `Transfer` for each owner change:

.. include:: tutorial/create-award-complaint-transfer.http
   :code:

`Transfer` object contains new access ``token`` and new ``transfer`` key for the object that will be transferred to new broker.

Changing complaint's owner
^^^^^^^^^^^^^^^^^^^^^^^^^^

Pay attention that only broker with appropriate accreditation level can become new owner. Otherwise broker will be forbidden from this action.

New broker should send POST request to appropriate `/tenders/id/awards/id/complaints/id` with `data` section containing ``id`` of `Transfer` and ``transfer`` key for the complaint received from customer:

.. include:: tutorial/change-award-complaint-ownership.http
   :code:

Now new broker became award complaint owner. Check whether new owner is able to change the award complaint:

.. include:: tutorial/modify-award-complaint.http
   :code:

New broker should provide its customer with new ``transfer`` key (received within `Transfer` object).

Check whether `Transfer` object has successfully stored complaint path in ``usedFor`` property:

.. include:: tutorial/get-used-award-complaint-transfer.http
   :code:


Examples for Contract
----------------------
   
Contract ownership change
~~~~~~~~~~~~~~~~~~~~~~~~~

Let's view transfer example for contract transfer.

Transfer creation 
^^^^^^^^^^^^^^^^^

First of all, you must know ID of the contract that you want to transfer.

Broker that is going to become new contract owner should create a `Transfer`.

.. include:: tutorial/create-contract-transfer.http
   :code:

`Transfer` object contains new access ``token`` and new ``transfer`` token for the object that will be transferred to new broker.

Changing contract's owner
^^^^^^^^^^^^^^^^^^^^^^^^^

In order to change contract's ownership new broker should send POST request to appropriate `/contracts/id/` with `data` section containing ``id`` of `Transfer` and ``transfer`` token received from customer:

.. include:: tutorial/change-contract-ownership.http
   :code:

Updated ``owner`` value indicates that ownership is successfully changed. 

Note that new broker has to provide its customer with new ``transfer`` key (generated in `Transfer` object).

After `Transfer` is applied it stores contract path in ``usedFor`` property.

.. include:: tutorial/get-used-contract-transfer.http
   :code:

Let's try to change the contract using ``token`` received on `Transfer` creation:

.. include:: tutorial/modify-contract.http
   :code:

Contract credentials change
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to get rights for future contract editing, you need to generate Transfer object and then apply this Transfer using the endpoint POST: /contracts/{id}/ownership, where id stands for contract ID.

Create new transfer
^^^^^^^^^^^^^^^^^^^

Let`s generate Transfer.

.. include:: tutorial/create-contract-transfer-credentials.http
   :code:

`Transfer` object contains new ``access.token`` that can be used for further contract modification and new ``transfer`` token.

Changing contract's credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to generate new contract's credentials broker should send POST request to appropriate endpoint /contracts/{id}/ownership with data section containing id of new Transfer generated previously and tender_token.

.. include:: tutorial/change-contract-credentials.http
   :code:

After Transfer is applied it stores contract path in usedFor property and can`t be used for other object.

.. include:: tutorial/get-used-contract-credentials-transfer.http
   :code:

Let's change the contract using ``token`` received on `Transfer` creation:

.. include:: tutorial/modify-contract-credentials.http
   :code:
Examples for OpenEU procedure 
------------------------------

Bid qualification complaint ownership change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenEU procedure contains bid qualification (pre-qualification) stage that allows complaints.

We will use this OpenEU procedure tender as an example: 

.. include:: tutorial/create-tender-for-qualification.http
   :code:

Response contains tender ID and `access` section with Tender ``token``.

Submit a Bid
^^^^^^^^^^^^

Let's submit a bid for qualification:

.. include:: tutorial/create-first-bid-for-qualification.http
   :code:

Response contains `access` section with a ``token`` key that can be used to create bid qualification complaint.


Submit a Complaint
^^^^^^^^^^^^^^^^^^

Let's create a bid qualification complaint:

.. include:: tutorial/create-qualification-complaint.http
   :code:
   
From response we take complaint ``id`` from `data` section and complaint ``transfer`` key from `access` section.

Changing complaint's owner
^^^^^^^^^^^^^^^^^^^^^^^^^^

Broker that is going to become new qualification complaint owner should create a `Transfer`.

.. include:: tutorial/create-qualification-complaint-transfer.http
   :code:

`Transfer` object contains new access ``token`` and new ``transfer`` key for the object that will be transferred to new broker.

New broker should send POST request to the appropriate `/tenders/id/qualifications/id/complaints/id` with `data` section containing ``id`` of `Transfer` and ``transfer`` key for the complaint received from customer:

.. include:: tutorial/change-qualification-complaint-owner.http
   :code:

Examples for Сompetitive Dialogue procedure
-------------------------------------------

Stage1 procedure
~~~~~~~~~~~~~~~~

Changing owner of tender in stage 1 is similar to Open UA or Open EU tenders procedure.

Stage2 procedure
~~~~~~~~~~~~~~~~

To change second stage tender owner, we need transfer token received during getting access to second stage tender. `Get token for second stage <http://openprocurementtendercompetitivedialogue.readthedocs.io/en/latest/tutorial.html#get-token-for-second-stage>`

Transfer creation
^^^^^^^^^^^^^^^^^

Broker that is going to become new tender owner should create a `Transfer`.

.. include:: tutorial/create-transfer-stage2.http
   :code:

`Transfer` object contains new access ``token`` and new ``transfer`` token for the tender that will be transferred to new broker.


Changing tender's stage2 owner
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Pay attention that only broker with appropriate accreditation level can become new owner. Otherwise broker will be forbidden from this action.

To change tender's ownership new broker should send POST request to appropriate `/tenders/<tender_id>/ownership`  with `data` section containing ``id`` of `Transfer` and ``transfer`` token received from previous PATCH request to  `tender/<tender_id>/credentials?acc_token=<acc_token>`.

.. include:: tutorial/change-tender-ownership-stage2.http
   :code:

Updated ``owner`` value indicates that ownership is successfully changed. 

Note that new broker has to provide its customer with new ``transfer`` key (generated in `Transfer` object).

Let's try to change the tender using ``token`` received on `Transfer` creation:

.. include:: tutorial/modify-tender-stage2.http
   :code:
