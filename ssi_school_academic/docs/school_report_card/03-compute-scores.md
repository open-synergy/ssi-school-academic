# Compute Scores of School Report Card

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card`\
> **Menu:** School > Classroom > Report Cards\
> **Actor:** user in group `User`\
> **State:** `draft` (unchanged)\
> **Requires:** `02-generate-lines`

## Pre-Condition

- **Record:** Status is **Draft**, and the report card has lines.
- **Data:** The score sheets of the subjects for the same Academic Term are **Done**.
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

- The **Final Score** of every line is computed again from the score sheets that are
  done.
- A score of 0 that was entered counts in the average; a score that was left empty does
  not.
- A line whose subject has no entered score at all shows **-** as its Final Score and
  has no Predicate; the line stays on the report card.
- The **Predicate** of every other line follows its Final Score.
- Status stays **Draft**.
