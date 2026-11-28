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
- The draft score sheet of the same term, class and subject follows the main teacher:
  when the **Teacher** of the document is changed, or a main line is added, or the
  **Role** of a line is changed to Main, that draft score sheet is given to the teacher
  of the main line and linked to it. When that teacher has a user account, the
  **Responsible** of the score sheet becomes that user, so the new teacher can open the
  sheet; a teacher without a user account leaves the previous **Responsible** unchanged.
  A line made Assistant moves nothing. A score sheet that is confirmed, done or
  cancelled is never changed.
