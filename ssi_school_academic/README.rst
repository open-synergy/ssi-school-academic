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
enrollments of the class, filled in, and approved. The homeroom teacher then
makes the report card of a student for an open enrollment: one line per
subject with the final score, the minimum score and the predicate computed
from the score sheets that are done, plus the co-curricular, extracurricular,
absence and note parts written by hand, finished through approval. A report
card is printed as a PDF from one py3o template, for the Mid-Term and the Final
type.


Work Instruction
================

* `Create Subject <docs/school_subject/01-create.html>`_
* `Edit Subject <docs/school_subject/02-edit.html>`_
* `Archive Subject <docs/school_subject/03-archive.html>`_
* `Create Score Component <docs/school_score_component/01-create.html>`_
* `Edit Score Component <docs/school_score_component/02-edit.html>`_
* `Archive Score Component <docs/school_score_component/03-archive.html>`_
* `Create Report Card Main Subject <docs/school_report_card_main_subject/01-create.html>`_
* `Edit Report Card Main Subject <docs/school_report_card_main_subject/02-edit.html>`_
* `Archive Report Card Main Subject <docs/school_report_card_main_subject/03-archive.html>`_
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
* `Enter Scores of School Score Sheet <docs/school_score_sheet/08-enter-scores.html>`_
* `Create School Report Card <docs/school_report_card/01-create.html>`_
* `Generate Lines of School Report Card <docs/school_report_card/02-generate-lines.html>`_
* `Compute Scores of School Report Card <docs/school_report_card/03-compute-scores.html>`_
* `Confirm School Report Card <docs/school_report_card/04-confirm.html>`_
* `Approve School Report Card <docs/school_report_card/05-approve.html>`_
* `Reject School Report Card <docs/school_report_card/06-reject.html>`_
* `Cancel School Report Card <docs/school_report_card/07-cancel.html>`_
* `Print School Report Card <docs/school_report_card/08-print.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-school-academic
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *School Academic*
6.  Install the module


Usage
=====

* In the **Scores** tab of a score sheet, a **Score** cell that was never filled shows
  empty. Type ``0`` to enter a zero score: it counts in the average and the final score.
  Empty the cell to take the score back: an empty cell does not count.
* The print shows at most four score component columns on a Mid-Term report
  card. Set the **Displayed Columns** of the Report Card Type in the order of
  the **Sequence** of the components; a fifth component and the ones after it
  are not printed.
* The **Phase** of the grade is filled on the grade form and printed in the page
  header of the report card.
* The **Main Subjects** menu lists the subjects that break a tie in the rank of the
  students, per **Grade** and optionally per **Expertise Program**. A record with an
  empty program is the fallback of the grade. Only one active record is allowed for
  the same grade and program.
* The **Report Card Ledger** menu (Classroom) opens a wizard where you pick a
  **Grade Class**, an **Academic Term** and a **Report Card Type**. **Show** displays the
  ledger of the class on screen and **Print** prints it as a PDF file. A row is listed
  for every enrollment of the class and term that is on progress or done, and only the
  report cards that are done give a score. A student without a done report card is
  listed with dashes and without a rank, below the other students. The rank follows the
  total; a tie is broken by the main subjects of the class and then by all the subjects.
  A score below the minimum score (KKM) of its subject is shown on a red background.
* To show the Print wizard of the SSI document form, configure the
  **Print Document Type** in the user interface; it is not part of this module.

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
