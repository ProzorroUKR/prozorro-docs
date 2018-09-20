.. include:: defs.hrst

.. index:: Lot

.. _Lot:

Lot
===

Schema
------

:id:
    string, auto-generated

:title:
   string, multilingual

   The name of the tender lot.

:description:
   string, multilingual

   Detailed description of tender lot.

:value:
   :ref:`value`, required

   Total available tender lot budget. Bids greater then ``value`` will be rejected.

:guarantee:
    :ref:`Guarantee`

    Bid guarantee

    Absent in :ref:`limited`
    
:date:
    string, :ref:`date`, auto-generated
    
:minimalStep:
   :ref:`value`, required

   The minimal step of auction (reduction). Validation rules:

   * `amount` should be less then `Lot.value.amount`
   * `currency` should either be absent or match `Lot.value.currency`
   * `valueAddedTaxIncluded` should either be absent or match `Lot.value.valueAddedTaxIncluded`

   Absent in :ref:`limited`

:auctionPeriod:
   :ref:`period`, read-only

   Period when Auction is conducted.

   Absent in :ref:`limited`

:auctionUrl:
    url

    A web address for view auction.

    Absent in :ref:`limited`

:status:
   string

   :`active`:
       Active tender lot (active)
   :`unsuccessful`:
       Unsuccessful tender lot (unsuccessful)
   :`complete`:
       Complete tender lot (complete)
   :`cancelled`:
       Cancelled tender lot (cancelled)

   Status of the Lot.


Workflow in :ref:`limited` and :ref:`openeu`
--------------------------------------------

.. graphviz::

    digraph G {
        A [ label="active*" ]
        B [ label="complete"]
        C [ label="cancelled"]
        D [ label="unsuccessful"]
         A -> B;
         A -> C;
         A -> D;
    }

\* marks initial state