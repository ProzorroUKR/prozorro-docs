.. _tutorial:

Tutorial
========

When customer needs to change current broker this customer should provide new preferred broker with ``transfer`` key for an object. Then new broker should create `Transfer` object and send request with `Transfer` ``id`` and ``transfer`` key (received from customer) in order to change object's owner.

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
