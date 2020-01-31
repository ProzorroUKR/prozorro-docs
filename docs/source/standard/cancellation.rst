
.. include:: defs.hrst

.. index:: Cancellation
.. _cancellation:

Cancellation
============

Schema
------

:id:
    uid, auto-generated

:reason:
    string, multilingual, required

    The reason, why Tender is being cancelled.

:status:
    string

    Possible values are:
     :`pending`:
       Default. The request is being prepared.
     :`active`:
       Cancellation activated.

:documents:
    List of :ref:`Document` objects

    Documents accompanying the Cancellation: Protocol of Tender Committee
    with decision to cancel the Tender.

:date:
    string, :ref:`date`

    Cancellation date.

:cancellationOf:
    string, required, default `tender`

    Possible values are:

    * `tender`
    * `lot`

    Possible values in :ref:`limited`:
    * `tender`

:relatedLot:
    string

    Id of related :ref:`lot`.


:reasonType:
    string

    There are four possible types of cancellation reason for common types of procedures set by procuring entity:

     :`noDemand`:
       No need in procurement of goods, works and services.

     :`unFixable`:
       Can not fix revealed violations of the law in the scope of public procurement.
    
     :`forceMajeure`:
       Can not do a procurement due to force majeure conditions.
    
     :`expensesCut`:
       Cut down the expenses of procurement of goods, works and services.
    
    Possible types for :ref:`negotiation` and :ref:`negotiation.quick`:
     
     :`noDemand`:
       No need in procurement of goods, works and services.

     :`unFixable`:
       Can not fix revealed violations of the law in the scope of public procurement.
    
     :`noObjectiveness`: 
       Can not do a procurement due to force majeure conditions.
    
     :`expensesCut`:
       Cut down the expenses of procurement of goods, works and services.
    
     :`dateViolation`:
       Cut down the expenses of procurement of goods, works and services.
    
    Possible types for :ref:`belowThreshold`:
     
     :`noDemand`:
       No need in procurement of goods, works and services.

     :`unFixable`:
       Can not fix revealed violations of the law in the scope of public procurement.

     :`expensesCut`:
       Cut down the expenses of procurement of goods, works and services.
    
    Possible types for :ref:`aboveThresholdUA.defense`:
     
     :`cancelled`:
       Default. Tender was cancelled.
     
     :`unsuccessful`:
       Tender was unsuccessful.
Cancellation workflow in :ref:`limited` and :ref:`openeu`
---------------------------------------------------------

.. graphviz::

    digraph G {
        A [ label="pending*" ]
        B [ label="active"]
         A -> B;
    }

\* marks initial state


