Example for Agreement
---------------------

Agreement ownership change
~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's view transfer example for agreement transfer.


Getting agreement's credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At first let's get agreement credentials:

.. include:: tutorial/get-agreement-credentials.http
   :code:

`broker` is current agreement's ``owner``.

Note that response's `access` section contains a ``transfer`` key which is used to change tender ownership.

After agreement's credentials obtaining broker has to provide its customer with ``transfer`` key.

Transfer creation
^^^^^^^^^^^^^^^^^

First of all, you must know ID of the agreement that you want to transfer.

Broker that is going to become new agreement owner should create a `Transfer`.

.. include:: tutorial/create-agreement-transfer.http
   :code:

`Transfer` object contains new access ``token`` and new ``transfer`` token for the object that will be transferred to new broker.

Changing agreement's owner
^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to change agreement's ownership new broker should send POST request to appropriate `/agreements/id/` with `data` section containing ``id`` of `Transfer` and ``transfer`` token received from customer:

.. include:: tutorial/change-agreement-ownership.http
   :code:

Updated ``owner`` value indicates that ownership is successfully changed. 

Note that new broker has to provide its customer with new ``transfer`` key (generated in `Transfer` object).

After `Transfer` is applied it stores agreement path in ``usedFor`` property.

.. include:: tutorial/get-used-agreement-transfer.http
   :code:

Let's try to change the agreement using ``token`` received on `Transfer` creation:

.. include:: tutorial/modify-agreement.http
   :code:
