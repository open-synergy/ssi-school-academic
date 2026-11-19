# Edit Report Card Main Subject

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card_main_subject`\
> **Menu:** School > Configuration > Subject & Scoring > Main Subjects\
> **Actor:** user in group `Report Card Main Subject`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Report Card Main Subject already exists.
- **Access:** User is in group `Report Card Main Subject`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Main Subjects** menu.
2. Find and open the record to edit, then click **Edit**.
3. Change the **Expertise Program** and the **Main Subjects**.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- The record is refused if another active record has the same grade and expertise
  program, or if no main subject is left.
