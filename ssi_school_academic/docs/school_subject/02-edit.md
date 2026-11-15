# Edit Subject

> **Module:** `ssi_school_academic`\
> **Model:** `school_subject`\
> **Menu:** School > Configuration > Subject & Scoring > Subjects\
> **Actor:** user in group `Subject`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Subject already exists and has a Minimum Score line.
- **Access:** User is in group `Subject`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Subjects** menu.
2. Find and open the record to edit, then click **Edit**.
3. Change the **Name**.
4. On the **Minimum Score** tab, click the **Minimum Score** cell of the line and enter
   the new score from 0 to 100.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- Removing a Grade from **Applicable Grades** does not remove its Minimum Score line;
  keep each line's Grade among the Applicable Grades.
