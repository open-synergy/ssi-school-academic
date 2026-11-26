# Edit Teaching Assignment

> **Module:** `ssi_school_academic`\
> **Model:** `school_teaching_assignment`\
> **Menu:** School > Configuration > Subject & Scoring > Teaching Assignments\
> **Actor:** user in group `Teaching Assignment`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Teaching Assignment already exists.
- **Access:** User is in group `Teaching Assignment`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Teaching Assignments** menu.
2. Find and open the record to edit, then click **Edit**.
3. Open the **Lines** tab and change the **Weekly Hours** of a line.
4. Click **Save**.

## Post-Condition

- The line is updated and the three weekly hours totals are recomputed.
- The score sheets already made from the line are kept.
