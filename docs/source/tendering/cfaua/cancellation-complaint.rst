

Complaint Retrieval
===================

Tender Cancellation Complaint Retrieval
---------------------------------------

You can list all Tender Cancellation Complaints:

.. include:: tutorial/cancellation-complaints-list.http
   :code:

And check individual complaint:

.. include:: tutorial/cancellation-complaint.http
   :code:


Complaint Submission
====================

If tender cancellation are favoriting particular supplier, or in any other viable case, any registered user can submit Tender Cancellation Complaint if tender in `active.tendering` status or participants if tender in any other status.

Tender Cancellation Complaint Submission (with documents)
---------------------------------------------------------

At first create a draft:

.. include:: tutorial/cancellation-complaint-submission.http
   :code:

Then upload necessary documents:

.. include:: tutorial/cancellation-complaint-submission-upload.http
   :code:

Submit tender cancellation complaint:

.. include:: tutorial/cancellation-complaint-complaint.http
   :code:

Tender Cancellation Complaint Submission (without documents)
------------------------------------------------------------

You can submit complaint that does not need additional documents:

.. include:: tutorial/cancellation-complaint-submission-complaint.http
   :code:


Complaint Resolution
====================

Rejecting Tender Cancellation Complaint
---------------------------------------

.. include:: tutorial/cancellation-complaint-reject.http
   :code:


Accepting Tender Cancellation Complaint
---------------------------------------

.. include:: tutorial/cancellation-complaint-accept.http
   :code:


Submitting Tender Cancellation Complaint Resolution
---------------------------------------------------

The Complaint Review Body uploads the resolution document:

.. include:: tutorial/cancellation-complaint-resolution-upload.http
   :code:

And either resolves complaint:

.. include:: tutorial/cancellation-complaint-resolve.http
   :code:

Or declines it:

.. include:: tutorial/cancellation-complaint-decline.http
   :code:

Submitting Resolution Confirmation
----------------------------------

For submit resolution confirmation, cancellation must be in `unsuccessful` status.

.. include:: tutorial/cancellation-complaint-resolved.http
   :code:

Cancelling Tender Cancellation Complaint
========================================

Cancelling not accepted complaint
---------------------------------

.. include:: tutorial/cancellation-complaint-cancel.http
   :code:

Cancelling accepted complaint by Complainant
--------------------------------------------

.. include:: tutorial/cancellation-complaint-accepted-stopping.http
   :code:

.. include:: tutorial/cancellation-complaint-stopping-stopped.http
   :code:

Cancelling accepted complaint by Reviewer
-----------------------------------------

.. include:: tutorial/cancellation-complaint-accepted-stopped.http
   :code:
