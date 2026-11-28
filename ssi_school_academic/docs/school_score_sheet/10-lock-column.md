# Lock Column of School Score Sheet

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_sheet`\
> **Menu:** School > Classroom > Score Sheets\
> **Actor:** user in group `User`\
> **State:** `draft` (unchanged)\
> **Requires:** `02-generate-lines`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Data:** The sheet has lines, generated with `02-generate-lines`, so the **Columns**
  tab lists a column that is not locked.
- **Config:** An active `policy.template` for this model grants `lock_column_ok` for
  state `draft` to the actor's group.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Score Sheets** menu.
2. Open the record to lock.
3. Open the **Columns** tab.
4. Click the **Lock Column** button on the row of the column to lock.

## Post-Condition

- The row shows **Locked** ticked, and its button changes from **Lock Column** to
  **Unlock Column** for a user who may unlock.
- The scores of that column are read only in the **Scores** tab and cannot be changed,
  added or deleted.
- **Generate Lines** is rejected while a column is locked.
- A report card reads the scores of the locked column, even while the sheet is
  **Draft**.
- Status stays **Draft**.
