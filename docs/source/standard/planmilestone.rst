.. index:: PlanMilestone

.. _planmilestone:

PlanMilestone
=============

Schema
------

:id:
    uid, auto-generated

:title:
    string, required

:description:
    string

:type:
    string, required

    The only possible value is:

    * `approval`

:status:
    string

    Possible values are:

    * `scheduled`
    * `met`
    * `notMet`

:dueDate:
    string, :ref:`date`, auto-generated

:dateModified:
    string, :ref:`date`, auto-generated

:dateMet:
    string, :ref:`date`, auto-generated
