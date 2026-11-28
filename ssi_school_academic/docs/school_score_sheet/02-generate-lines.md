# Generate Lines of School Score Sheet

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_sheet`\
> **Menu:** School > Classroom > Score Sheets\
> **Actor:** user in group `User`\
> **State:** `draft` (unchanged)\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Data:** At least one enrollment of the Grade Class and Academic Term is **Open**,
  and at least one active **Score Component** exists.
- **Data:** No column is locked. A locked column must be unlocked first
  (`11-unlock-column`).
- **Config:** An active `policy.template` for this model grants `generate_lines_ok` for
  state `draft` to the actor's group.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Score Sheets** menu.
2. Open the record to fill.
3. Click the **Generate Lines** button.
4. Click **OK** on the confirmation dialog.
5. Open the **Scores** tab.

## Post-Condition

- Every line of the sheet is replaced by new lines: one line per open enrollment and per
  active score component, ordered by student and component sequence.
- Enrollments that are not open, and score components that are archived, get no line.
- The **Score** of every new line is empty, which means not yet scored.
- The **Columns** tab lists one row for each score component that has lines, of every
  category, each not locked yet.
- The **Learning Objectives** tab lists one row for each active daily test and
  assignment. A row that already exists is kept with its chosen objectives; only missing
  rows are added.
- Status stays **Draft**.
