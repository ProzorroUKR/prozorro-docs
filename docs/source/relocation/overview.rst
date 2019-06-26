Overview
========

Conventions
-----------
All API POST and PUT requests expect a top-level object with a single
element in it named `data`.  Successful responses will mirror this format. 
The data element should itself be an object, containing the parameters for
the request.  In the case of creating a new tender, these are the fields we
want to set on the tender itself.

If the request was successful, we will get a response code of `201`
indicating the object was created.  That response will have a data field at
its top level, which will contain complete information on the new tender,
including its ID.

If something went wrong during the request, we'll get a different status
code and the JSON returned will have an `errors` field at the top level
containing a list of problems.  We look at the first one and print out its
message.


Documentation of related packages
---------------------------------

* `OpenProcurement API <http://api-docs.openprocurement.org/en/latest/>`_

* `Open tender procedure (OpenUA) <http://openua.api-docs.openprocurement.org/en/latest/>`_

* `Open tender procedure with publication in English (OpenEU) <http://openeu.api-docs.openprocurement.org/en/latest/>`_

* `Reporting, negotiation procurement procedure and negotiation procedure for the urgent need  <http://limited.api-docs.openprocurement.org/en/latest/>`_

* `Defense open tender <http://defense.api-docs.openprocurement.org/en/latest/>`_

* `Contracting API interface to OpenProcurement database <http://contracting.api-docs.openprocurement.org/en/latest/>`_

* `Document service <http://documentservice.api-docs.openprocurement.org/en/latest/>`_
