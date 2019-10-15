.. _centralized_procurements:


Centralized procurements
========================


Creating plan procurement
-------------------------

Buyer can create a plan with a special `procurementMethodType` = "centralizedProcurement".
He should specify himself in `buyers` list and point at one of the central procurement organizations in `procuringEntity` field:

.. include:: http/create-plan.http
   :code:

After the plan gets `scheduled`, the `approval` :ref:`PlanMilestone` appears in the data:

.. include:: http/patch-plan-status-scheduled.http
   :code:

The central procurement organization can respond that the plan has been accepted

.. include:: http/patch-plan-milestone-met.http
   :code:

Creating tender
---------------

The central procurement organization creates an aggregated tender
and specifies all the buyer organizations using `buyers` list of :ref:`PlanOrganization`

.. include:: http/create-tender.http
   :code:

