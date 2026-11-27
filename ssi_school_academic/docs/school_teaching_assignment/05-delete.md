# Delete Teaching Assignment

> **Module:** `ssi_school_academic`\
> **Model:** `school_teaching_assignment`\
> **Menu:** School > Configuration > Subject & Scoring > Teaching Assignments\
> **Actor:** user in group `Teaching Assignment`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Teaching Assignment already exists.
- **Data:** No score sheet that is not cancelled exists for the term, the grade class
  and the subject of any line of the assignment. The main and the assistant lines are
  guarded alike. A score sheet that was made by hand, without a link to the line, counts
  too. A cancelled score sheet does not count.
- **Access:** User is in group `Teaching Assignment`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Teaching Assignments** menu.
2. Find and open the record to delete.
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The Teaching Assignment and its lines are permanently removed from the system.
- The cancelled score sheets that pointed at a line are kept, and their **Teaching
  Assignment Line** is now empty.
- If a score sheet that is not cancelled exists for the term, the grade class and the
  subject of a line, the deletion is refused with an error message, and nothing is
  deleted. Cancel or delete that score sheet first, then delete the assignment again.
  The same refusal applies when a single line is deleted from the **Lines** tab.
