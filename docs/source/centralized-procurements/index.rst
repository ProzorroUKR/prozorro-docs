.. _centralized_procurements:


Centralized procurements
========================


Creating plan procurement
-------------------------

Buyer creates a plan. He should specify himself in `buyers` list and point at one of the central procurement organizations in `procuringEntity` field:

.. include:: http/create-plan.http
   :code:


Creating approve milestone
--------------------------

As central procurement organization sees itself as `procuringEntity` of a plan,
it can post milestones to this plan:

    .. include:: http/post-plan-milestone.http
       :code:

Only if the access token from the response is provided, the milestone can be changed later:

    .. include:: http/patch-plan-milestone.http
       :code:

Posting documents is also require the milestone access token (as well as changing documents using PATCH/PUT methods):

    .. include:: http/post-plan-milestone-document.http
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
