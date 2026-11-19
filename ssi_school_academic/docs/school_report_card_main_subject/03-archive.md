# Archive Report Card Main Subject

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card_main_subject`\
> **Menu:** School > Configuration > Subject & Scoring > Main Subjects\
> **Actor:** user in group `Report Card Main Subject`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Report Card Main Subject is currently active.
- **Access:** User is in group `Report Card Main Subject`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Main Subjects** menu.
2. Select the record to archive (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The record is archived and no longer appears in the default list view.
- An archived record is no longer used to pick the main subjects of a class.
- A new active record can be created for the same grade and expertise program.
