# Edit School Curriculum

> **Module:** `ssi_school_academic`\
> **Model:** `school_curriculum`\
> **Menu:** School > Configuration > Subject & Scoring > Curriculums\
> **Actor:** user in group `User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Curriculums** menu.
2. Find and open the curriculum to edit.
3. Change the required fields in the header or the **Lines** tab.
4. Click **Save**.

## Post-Condition

- The curriculum is updated with the new values.
- **Category** and **Total Time** of the lines are recomputed.
- The header and the lines cannot be changed once the curriculum has left **Draft**.
