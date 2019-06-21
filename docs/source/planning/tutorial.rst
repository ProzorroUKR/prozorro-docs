.. _planning_tutorial:

Tutorial
========

Creating plan procurement
-------------------------

Let’s create a plan:

.. include:: tutorial/create-plan.http
   :code:

We have `201 Created` response code, `Location` header and body with extra `id`, `planID`, and `dateModified` properties.

Let's check what plan registry contains:

.. include:: tutorial/plan-listing.http
   :code:

We do see the internal `id` of a plan (that can be used to construct full URL by prepending `http://api-sandbox.openprocurement.org/api/0/plans/`) and its `dateModified` datestamp.


Modifying plan
--------------

Let's update plan by supplementing it with all other essential properties:

.. include:: tutorial/patch-plan-procuringEntity-name.http
   :code:

.. XXX body is empty for some reason (printf fails)

We see the added properies have merged with existing plan data. Additionally, the `dateModified` property was updated to reflect the last modification datestamp.

Checking the listing again reflects the new modification date:

.. include:: tutorial/plan-listing-after-patch.http
   :code:

.. _tender-from-plan:


Tender creation from a procurement plan
---------------------------------------

A tender can be created from your procurement plan. This tender will be linked with the plan
using :ref:`plan_id<tender>` and :ref:`tender_id` fields to ensure 1-1 relation between these entities.



.. note::
    | System failures during tender-from-plan creation can produce tenders that are not linked with their plans by :ref:`tender_id`.
    | Make sure you do use :ref:`2pc` and do not proceed with these error state tender objects (create new ones).


There are validation rules that are supposed to decline the chance of making a mistake

.. include:: tutorial/tender-from-plan-validation.http
   :code:

There are three of them:

    * procurementMethodType
    * procuringEntity.identifier - matching id and scheme with the same fields in tender data
    * classification.id  - matching with tender item classification codes using first 4 digits (``336`` is exception)

A successful example looks like this:

.. include:: tutorial/tender-from-plan.http
   :code:
