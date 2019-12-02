.. _centralized_procurements:


Centralized procurements
========================


Creating plan procurement
-------------------------

Buyer creates a plan. He should specify himself in `buyers` list and point at one of the central procurement organizations in `procuringEntity` field:

.. include:: http/create-plan.http
   :code:

..
    After the plan gets `scheduled`, the `approval` :ref:`PlanMilestone` appears in the data:

    .. include:: http/patch-plan-status-scheduled.http
       :code:

    The central procurement organization can respond that the plan has been accepted

    .. include:: http/patch-plan-milestone-met.http
       :code:


Creating tender
---------------

The central procurement organization creates an aggregated tender in `draft` status
and specifies all the buyer organizations using `buyers` list of :ref:`PlanOrganization`:

.. include:: http/create-tender.http
   :code:


Connecting plans to the tender
------------------------------

The central procurement organization connects the plan to the tender.
If there are many plans, they should be connected one by one.


.. include:: http/post-tender-plans.http
    :code:


As a result the plan is moved to "complete" status

.. include:: http/plan-complete.http
    :code:


The tender `plans` field contains all the plan ids

.. include:: http/tender-get.http
    :code:
