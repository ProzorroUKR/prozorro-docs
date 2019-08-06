Example for Tender
------------------

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

.. include:: tutorial/create-tender-transfer.http
   :code:

`Transfer` object contains new access ``token`` and new ``transfer`` token for the object that will be transferred to new broker.

`Transfer` can be retrieved by `id`:

.. include:: tutorial/get-tender-transfer.http
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

.. include:: tutorial/get-used-tender-transfer.http
   :code:

'Used' `Transfer` can't be applied to any other object.

Let's try to change the tender using ``token`` received on `Transfer` creation:

.. include:: tutorial/modify-tender.http
   :code:
