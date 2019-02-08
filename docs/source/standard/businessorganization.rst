.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: BusinessOrganization, Company

.. _BusinessOrganization:

BusinessOrganization
====================

Schema
------

:name:
    string, multilingual

    Additionally in :ref:`openeu` and :ref:`esco`:

    uk (title) and en (title_en) translations are required
    
    |ocdsDescription|
    The common name of the organization.
    
:identifier:
    :ref:`Identifier`
    
    |ocdsDescription|
    The primary identifier for this organization. 
    
:additionalIdentifiers:
    List of :ref:`identifier` objects

:address:
    :ref:`Address`, required

:contactPoint:
    :ref:`ContactPoint`, required

Additionally in :ref:`openeu`:

:additionalContactPoints:
    List of :ref:`ContactPoint` objects

:scale:
    string, required

    Possible values are:

    * `micro`
    * `sme`
    * `large`
    * `mid`

    |ocdsDescription|
    The scale property can be used to indicate the size or scale of a commercial organization.
