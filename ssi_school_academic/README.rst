.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
School Academic
=====================

Manages the academic master data of a school: the subjects taught, the
Subject Group each belongs to, the Grades it applies to, and the minimum
score (KKM) a student must reach on each Grade. It also manages the score
components of the report card (e.g. Daily Test 1, Assignment 1, Mid-Term
Exam), one record per slot. Report card types set how the final score is
calculated: the averaged components, the weights, the printed columns, and
the rounding threshold. Teachers record the scores of a subject on a score
sheet per grade class and academic term: the lines are generated from the open
enrollments of the class, filled in, and approved.


Work Instruction
================

* `Create Subject <docs/school_subject/01-create.html>`_
* `Edit Subject <docs/school_subject/02-edit.html>`_
* `Archive Subject <docs/school_subject/03-archive.html>`_
* `Create Score Component <docs/school_score_component/01-create.html>`_
* `Edit Score Component <docs/school_score_component/02-edit.html>`_
* `Archive Score Component <docs/school_score_component/03-archive.html>`_
* `Create Report Card Type <docs/school_report_card_type/01-create.html>`_
* `Edit Report Card Type <docs/school_report_card_type/02-edit.html>`_
* `Archive Report Card Type <docs/school_report_card_type/03-archive.html>`_
* `Create School Score Sheet <docs/school_score_sheet/01-create.html>`_
* `Generate Lines of School Score Sheet <docs/school_score_sheet/02-generate-lines.html>`_
* `Confirm School Score Sheet <docs/school_score_sheet/03-confirm.html>`_
* `Approve School Score Sheet <docs/school_score_sheet/04-approve.html>`_
* `Reject School Score Sheet <docs/school_score_sheet/05-reject.html>`_
* `Cancel School Score Sheet <docs/school_score_sheet/06-cancel.html>`_
* `Restart School Score Sheet Approval Process <docs/school_score_sheet/07-restart-approval.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-school-academic
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *School Academic*
6.  Install the module


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-school-academic/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
