# Generate Score Sheets from Teaching Assignment

> **Module:** `ssi_school_academic`\
> **Model:** `school_teaching_assignment`\
> **Menu:** School > Configuration > Subject & Scoring > Teaching Assignments\
> **Actor:** user in group `Teaching Assignment`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Teaching Assignment exists and has at least one line whose role is
  **Main**.
- **Data:** The teacher of the assignment has an employee that is linked to a user.
- **Config:** No score sheet that is not cancelled exists yet for the term, class and
  subject of the line, otherwise that line is skipped.
- **Access:** User is in group `Teaching Assignment`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Teaching Assignments** menu.
2. Open the Teaching Assignment, or tick several assignments in the list.
3. Click **Action** and choose **Generate Score Sheets**. A dialog opens with the chosen
   assignments.
4. Click the **Generate** button.
5. Read the **Result**: it gives the number of score sheets created and, for each line
   that was skipped, the reason.
6. Click **Close**.

## Post-Condition

- One score sheet in **Draft** status is created for every **Main** line that had none,
  with the term, class, subject and teacher of the line, and linked to the line.
- The score sheet is owned by the user of the teacher, so only that teacher sees it.
- A line that already has a score sheet that is not cancelled, and a teacher without a
  user, are skipped and named in the **Result**. Lines whose role is **Assistant** get
  no score sheet.
