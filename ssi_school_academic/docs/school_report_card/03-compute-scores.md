# Compute Scores of School Report Card

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card`\
> **Menu:** School > Classroom > Report Cards\
> **Actor:** user in group `User`\
> **State:** `draft` (unchanged)\
> **Requires:** `02-generate-lines`

## Pre-Condition

- **Record:** Status is **Draft**, and the report card has lines.
- **Data:** The score sheets of the subjects for the same Academic Term have their
  columns locked (`10-lock-column` of the score sheet). A sheet does not need to be
  **Done**, and a **Cancelled** sheet is not read.
- **Config:** An active `policy.template` for this model grants `compute_scores_ok` for
  state `draft` to the actor's group.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Report Cards** menu.
2. Open the record to compute.
3. Click the **Compute Scores** button.
4. Click **OK** on the confirmation dialog.
5. Open the **Subjects** tab.

## Post-Condition

- The **Final Score** of every line is computed again from the locked columns of the
  score sheets. A column that is not locked does not count, so a **Mid-Term** report
  card can be computed before the final exam is locked.
- The score of each component is copied to the line. The print reads this copy, so it
  does not change when a score sheet is unlocked or cancelled afterwards.
- A score of 0 that was entered counts in the average; a score that was left empty does
  not.
- A line whose subject has no entered score at all shows **-** as its Final Score and
  has no Predicate; the line stays on the report card.
- The **Predicate** of every other line follows its Final Score.
- The **Learning Objective Achievement** of a line is filled from the learning
  objectives of the scored daily tests and assignments only when it is empty. A text
  that is already there, typed by hand or filled before, is kept; use
  `09-refill-learning-objective` to overwrite it.
- Status stays **Draft**.
