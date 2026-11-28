# Unlock Column of School Score Sheet

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_sheet`\
> **Menu:** School > Classroom > Score Sheets\
> **Actor:** user in group `Validator`\
> **State:** `draft` (unchanged)\
> **Requires:** `10-lock-column`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Data:** The **Columns** tab lists a column that is locked.
- **Config:** An active `policy.template` for this model grants `unlock_column_ok` for
  state `draft` to the actor's group.
- **Access:** User is in group `Validator`.

## Flow

1. Open the **School > Classroom > Score Sheets** menu.
2. Open the record to unlock.
3. Open the **Columns** tab.
4. Click the **Unlock Column** button on the row of the column to unlock.

## Post-Condition

- The row shows **Locked** unticked, and its button changes from **Unlock Column** to
  **Lock Column**.
- The scores of that column can be changed again in the **Scores** tab.
- A report card no longer reads the scores of that column.
- Status stays **Draft**.
