# Archive Score Predicate

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_predicate`\
> **Menu:** School > Configuration > Subject & Scoring > Score Predicates\
> **Actor:** user in group `Score Predicate`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Score Predicate is currently active.
- **Access:** User is in group `Score Predicate`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Score Predicates** menu.
2. Select the record to archive (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The record is archived and no longer appears in the default list view.
- Its Grades are free to join another active Score Predicate table.
- An archived table is no longer used to match scores to predicates.
