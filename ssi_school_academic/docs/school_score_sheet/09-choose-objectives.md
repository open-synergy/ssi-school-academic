# Choose Learning Objectives of School Score Sheet

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_sheet`\
> **Menu:** School > Classroom > Score Sheets\
> **Actor:** user in group `User`\
> **State:** `draft` (unchanged)\
> **Requires:** `02-generate-lines`

## Pre-Condition

- **Record:** Status is **Draft**, and the sheet has its components, created by
  `02-generate-lines`.
- **Data:** An active **Subject Outcome** exists for the Subject, the Grade of the Grade
  Class and the Academic Term of the sheet, with at least one learning objective.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Score Sheets** menu.
2. Open the record to fill.
3. Click the **Edit** button.
4. Open the **Learning Objectives** tab. One row is listed for each daily test and
   assignment of the sheet.
5. Click the **Learning Objectives** cell of a row, and choose one or more objectives.
   Only the objectives of the subject, grade and academic term of the sheet are offered.
6. Click the **Save** button.

## Post-Condition

- The chosen objectives are listed on the row of the component.
- On the Subject Outcome, the objective lists the component of this sheet in its **Score
  Sheet Components** column.
- Generating the lines again does not remove the chosen objectives.
- Mid-term and final exams have no row; they are not linked to objectives.
- Status stays **Draft**.
