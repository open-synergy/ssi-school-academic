# Archive Report Card Type

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card_type`\
> **Menu:** School > Configuration > Subject & Scoring > Report Card Types\
> **Actor:** user in group `Report Card Type`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Report Card Type is currently active.
- **Access:** User is in group `Report Card Type`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Report Card Types** menu.
2. Select the record to archive (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The record is archived and no longer appears in the default list view.
- Archived Report Card Types cannot be selected in new records that reference a Report
  Card Type.
- Records that already use this Report Card Type can still be viewed.
