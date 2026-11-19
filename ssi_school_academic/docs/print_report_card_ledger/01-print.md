# Print Report Card Ledger

> **Module:** `ssi_school_academic`\
> **Model:** `print_report_card_ledger`\
> **Menu:** School > Classroom > Report Card Ledger\
> **Actor:** user in group `Viewer` of the report card

## Pre-Condition

- **Access:** User is in group `Viewer` of the report card.
- **Data:** The enrollments of the class are on progress or done for the academic term.
  The report cards of those students exist for the report card type, and only the ones
  that are **Done** give a score.
- **Config:** The **Main Subjects** menu lists the main subjects of the grade, and of
  the expertise program of the class, to break a tie of the rank. Without a record the
  tie is broken by all the subjects.

## Flow

1. Open the **School > Classroom > Report Card Ledger** menu. A dialog opens.
2. Fill in the required fields:
   - **Grade Class** _(required)_: Select the class of the ledger.
   - **Academic Term** _(required)_: Select the academic term of the enrollments.
   - **Report Card Type** _(required)_: Select the type of the report cards.
3. Click the **Show** button to see the ledger on screen. (Click **Print** instead to
   download it as a PDF file.)

## Post-Condition

- The ledger is shown on screen, or downloaded as a PDF file when **Print** is clicked.
  It lists one row for every enrollment of the class and term that is on progress or
  done, with the number, student ID, name, the score of every subject, the total, the
  average and the rank. The last row shows the average of every subject.
- Only report cards that are **Done** give a score. A student without a done report card
  shows a dash on every score, the total, the average and the rank, in the rows at the
  bottom. A subject without a score shows a dash.
- The total and the average count the scored cells only, and a score of 0 is counted.
- The rank follows the total, the highest first. A tie is broken by the main subjects of
  the class and then by all the subjects; students still tied share the rank and the
  next rank skips the shared positions (1, 1, 3).
- A score below the minimum score (KKM) of its subject is shown on a red background.
- The report cards themselves are unchanged.
