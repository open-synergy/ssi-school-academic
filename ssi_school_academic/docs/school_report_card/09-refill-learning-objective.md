# Refill Learning Objective of School Report Card

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card`\
> **Menu:** School > Classroom > Report Cards\
> **Actor:** user in group `User`\
> **State:** `draft` (unchanged)\
> **Requires:** `02-generate-lines`

## Pre-Condition

- **Record:** Status is **Draft**, and the report card has lines.
- **Data:** The score sheets of the subjects for the same Academic Term are **Done**,
  and their daily tests and assignments have learning objectives chosen
  (`09-choose-objectives` of the score sheet).
- **Config:** An active `policy.template` for this model grants
  `refill_learning_objective_ok` for state `draft` to the actor's group.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Report Cards** menu.
2. Open the record to refill.
3. Click the **Refill Learning Objective** button.
4. Click **OK** on the confirmation dialog.
5. Open the **Subjects** tab.

## Post-Condition

- The **Learning Objective Achievement** of every line is replaced by the descriptions
  of the objectives of the daily tests and assignments the student was scored for, one
  per line, in the order of the objectives and without repeats. The text typed by hand
  is overwritten.
- A subject without a scored daily test or assignment gets an empty text.
- The text stays editable by hand.
- Status stays **Draft**.
