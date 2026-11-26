# Create Teaching Assignment

> **Module:** `ssi_school_academic`\
> **Model:** `school_teaching_assignment`\
> **Menu:** School > Configuration > Subject & Scoring > Teaching Assignments\
> **Actor:** user in group `Teaching Assignment`

## Pre-Condition

- **Data:** The **Teacher** and the **Academic Term** the assignment is for already
  exist.
- **Data:** A **Homeroom** that is not cancelled exists in that academic term for every
  class the teacher teaches, and the **Subject** is taught in the Grade of the homeroom.
- **Config:** The teacher has no other teaching assignment in the same academic term.
- **Access:** User is in group `Teaching Assignment`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Teaching Assignments** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the assignment, for example the teacher
     and the term.
   - **Code** _(required)_: Enter a unique code identifying this record, or enter **/**
     if you do not need a unique identifier.
   - **Teacher** _(required)_: Select the teacher.
   - **Academic Term** _(required)_: Select the academic term (one term is one
     semester). It defaults to the first term that is on progress.
4. Open the **Lines** tab.
5. Click **Add a line** for each homeroom and subject the teacher teaches, and fill in
   the line:
   - **Homeroom** _(required)_: Select the homeroom. Only homerooms of the academic term
     that are not cancelled are offered. **Grade Class** is filled from the homeroom.
   - **Subject** _(required)_: Select the subject. Only subjects taught in the Grade of
     the homeroom are offered.
   - **Role** _(required)_: Select **Main** for the teacher who gives the scores, or
     **Assistant** for a teacher who only reads the score sheet. It defaults to
     **Main**.
   - **Weekly Hours**: Enter the number of lesson hours (JP) per week.
6. Click **Save**.

## Post-Condition

- A new Teaching Assignment record is created and active, with its lines.
- **Main Weekly Hours**, **Assistant Weekly Hours** and **Total Weekly Hours** show the
  sum of the weekly hours of the lines per role and in total.
- Saving is rejected when the teacher already has an assignment in the same academic
  term, when the subject of the homeroom already has another main teacher, when the
  teacher already teaches the subject in the homeroom, or when the subject is not taught
  in the Grade of the homeroom.
- The **Teaching Assignments** tab of the homeroom lists the line.
