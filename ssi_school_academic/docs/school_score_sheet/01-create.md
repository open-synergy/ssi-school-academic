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
- **Data:** _(Optional)_ The **Teacher** has a **Teaching Assignment** with a **Main**
  line for the class and subject in the term.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Score Sheets** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Teaching Assignment Line**: Select the main line of the teaching assignment this
     sheet is made for. It fills the term, class, subject and teacher. Leave it empty
     for a score sheet that is not made from an assignment.
   - **Grade Class** _(required)_: Select the class the scores are given to. **Grade**
     is filled from the class. A teacher who has main lines is offered the classes of
     those lines only, and the line and the subject are filled when the class has one
     main line.
   - **Academic Term** _(required)_: Select the term of the scores. It defaults to the
     first term that is on progress.
   - **Teacher** _(required)_: Select the teacher who gives the scores. It defaults to
     the teacher of the logged in user.
   - **Subject** _(required)_: Select the subject. Only subjects applicable to the
     **Grade** are offered, and a teacher who has main lines is offered the subjects of
     those lines.
   - **Date**: Defaults to today's date.
4. Click **Save**.

## Post-Condition

- A new School Score Sheet record is created in **Draft** status.
- **Academic Year** is filled from the Academic Term.
- The score sheet is linked to the chosen Teaching Assignment Line, if any.
- Saving is rejected with an error when another score sheet that is not cancelled exists
  for the same Subject, Grade Class, and Academic Term.
