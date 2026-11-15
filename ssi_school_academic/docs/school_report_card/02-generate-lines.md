# Generate Lines of School Report Card

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card`\
> **Menu:** School > Classroom > Report Cards\
> **Actor:** user in group `User`\
> **State:** `draft` (unchanged)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Data:** At least one active **Subject** is taught in the Grade of the report card.
- **Config:** An active `policy.template` for this model grants `generate_lines_ok` for
  state `draft` to the actor's group.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Report Cards** menu.
2. Open the record to fill.
3. Click the **Generate Lines** button.
4. Click **OK** on the confirmation dialog.
5. Open the **Subjects** tab.

## Post-Condition

- Every line of the report card is replaced by new lines: one line per active subject
  taught in the Grade.
- Each line shows the **Final Score** computed from the score sheets that are done, the
  **Minimum Score**, and the **Predicate** of that score.
- Subjects not taught in the Grade get no line.
- Status stays **Draft**.
