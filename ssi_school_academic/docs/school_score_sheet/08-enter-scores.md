# Enter Scores of School Score Sheet

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_sheet`\
> **Menu:** School > Classroom > Score Sheets\
> **Actor:** user in group `User`\
> **State:** `draft` (unchanged)\
> **Requires:** `02-generate-lines`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Data:** The sheet has lines, generated with `02-generate-lines`, and the **Score**
  of those lines is still empty.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Score Sheets** menu.
2. Open the record to fill.
3. Click the **Edit** button.
4. Open the **Scores** tab.
5. Click the **Score** cell of a line and type `0`.
6. Click the **Score** cell of another line and type a number above zero, for example
   `90`.
7. Click the **Save** button.

## Post-Condition

- The line where `0` was typed shows `0.00` and counts as scored, so the zero takes part
  in the average and the final score of the report card.
- The line where the number above zero was typed shows that number and counts as scored.
- The lines whose **Score** was not touched stay empty and do not count.
- A **Score** that is emptied and saved shows an empty cell again and does not count.
- Status stays **Draft**.
