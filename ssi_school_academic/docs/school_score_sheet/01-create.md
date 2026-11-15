# Create School Score Sheet

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_sheet`\
> **Menu:** School > Classroom > Score Sheets\
> **Actor:** user in group `User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** An **Academic Term**, a **Grade Class**, a **Subject** applicable to the
  Grade of that class, and a **Teacher** already exist.
- **Config:** No other score sheet that is not cancelled exists for the same Subject,
  Grade Class, and Academic Term.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Score Sheets** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Grade Class** _(required)_: Select the class the scores are given to. **Grade**
     is filled from the class.
   - **Academic Term** _(required)_: Select the term of the scores.
   - **Teacher** _(required)_: Select the teacher who gives the scores.
   - **Subject** _(required)_: Select the subject. Only subjects applicable to the
     **Grade** are offered.
   - **Date**: Defaults to today's date.
4. Click **Save**.

## Post-Condition

- A new School Score Sheet record is created in **Draft** status.
- **Academic Year** is filled from the Academic Term.
- Saving is rejected with an error when another score sheet that is not cancelled exists
  for the same Subject, Grade Class, and Academic Term.
