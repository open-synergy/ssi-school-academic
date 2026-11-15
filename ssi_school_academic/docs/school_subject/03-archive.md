# Archive Subject

> **Module:** `ssi_school_academic`\
> **Model:** `school_subject`\
> **Menu:** School > Configuration > Subject & Scoring > Subjects\
> **Actor:** user in group `Subject`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Subject is currently active.
- **Access:** User is in group `Subject`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Subjects** menu.
2. Select the record to archive (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The record is archived and no longer appears in the default list view.
- Archived Subjects cannot be selected in new records that reference a Subject.
- Records that already use this Subject can still be viewed.
