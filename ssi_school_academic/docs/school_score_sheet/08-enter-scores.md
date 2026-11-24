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
- **Config:** The subject has a minimum score (KKM) for the grade of the class, to see
  the red mark. Without it the minimum score is `0` and no cell turns red.
- **Config:** Exactly one active report card type of the term type **Final**, and one of
  the term type **Mid-Term**, to see the calculated columns. Otherwise those columns
  stay empty and show a warning.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Score Sheets** menu.
2. Open the record to fill.
3. Click the **Edit** button.
4. Open the **Scores** tab. The scores are shown as a grid: one row per student, one
   column per score component in the order of the component sequence, and the calculated
   columns **Average**, **Mid Score** and **Final Score**.
5. Click the **Score** cell of the first student under the first component and type `0`.
6. Press **Tab**. The focus moves to the next cell of the same student, and the typed
   score is kept.
7. Type a number above zero in that cell, for example `90`.
8. Click the **Save** button.

Other keys move the focus between the cells while the sheet is in edit mode:
**Shift+Tab** goes to the previous cell, **Enter** and the **Down** arrow go to the same
component of the next student, the **Up** arrow to the previous student, and the
**Left** and **Right** arrows to the neighbour cell.

## Post-Condition

- The cell where `0` was typed shows `0.00` and counts as scored, so the zero takes part
  in the average and the final score of the report card.
- The cell where the number above zero was typed shows that number and counts as scored.
- The cells whose **Score** was not touched stay empty and do not count.
- A **Score** that is emptied and saved shows an empty cell again and does not count.
- A scored cell below the minimum score of the subject is shown in red, and so is a
  calculated cell below it. An empty cell is never red.
- The calculated columns follow the same formulas as the report card. A student with no
  score for a column leaves that cell empty; it is not shown as `0`.
- Status stays **Draft**.
- When the sheet is not **Draft**, the grid is read only.
