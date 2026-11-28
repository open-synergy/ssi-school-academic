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
5. Click the **Score** cell of the first student under the first component, type a
   number, for example `50`, and press **Tab**. The focus moves at once to the next cell
   of the same student, and the typed score is kept.
6. Type a number in that cell, for example `60`, and press **Enter**. The focus moves to
   the same component of the next student, and the typed score is kept.
7. Type a number in that cell, for example `65`, and press the **Down** arrow. The focus
   moves to the same component of the next student.
8. Type a number in that cell, for example `70`, and press the **Up** arrow. The focus
   moves to the same component of the previous student.
9. Type a number in a cell, for example `40`, then click once on another **Score** cell
   and type a number at once, for example `30`. Both numbers are kept, however slow the
   connection is. Press **Tab** to leave the second cell.
10. Fill the whole grid with the **Tab** key only: start at the first cell and press
    **Tab** to go over every cell, row by row. Type a number in the cells to fill, type
    `0` where the score is zero, and only press **Tab** on the cells to leave empty. The
    typed scores stay while the focus moves on. At the last cell, press **Tab**: the
    focus leaves the grid and does not come back to the first cell.
11. Click the **Save** button.

Other keys move the focus between the cells while the sheet is in edit mode:
**Shift+Tab** goes to the previous cell, and the **Left** and **Right** arrows to the
neighbour cell. The grid stays the same while you type: it is not drawn again after a
score is entered, so the focus and the text typed in the next cell are never lost.

## Post-Condition

- Every cell where a number was typed shows that number and counts as scored, so it
  takes part in the average and the final score of the report card.
- A cell where `0` was typed shows `0.00` and counts as scored, like any other number.
- The cells whose **Score** was not touched stay empty and do not count, also the ones
  that the **Tab** key went over.
- A **Score** that is emptied and saved shows an empty cell again and does not count.
- A scored cell below the minimum score of the subject is shown in red, and so is a
  calculated cell below it. An empty cell is never red.
- The calculated columns follow the same formulas as the report card. A student with no
  score for a column leaves that cell empty; it is not shown as `0`.
- Status stays **Draft**.
- A cell of a locked column (`10-lock-column`) is read only, and the keyboard moves over
  it to the next cell that can be edited.
- When the sheet is not **Draft**, the grid is read only.
