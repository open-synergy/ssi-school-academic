# Archive Score Component

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_component`\
> **Menu:** School > Configuration > Subject & Scoring > Score Components\
> **Actor:** user in group `Score Component`\
> **Active:** `true` → `false`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Score Component is currently active.
- **Access:** User is in group `Score Component`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Score Components** menu.
2. Select the record to archive (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The record is archived and no longer appears in the default list view.
- Archived Score Components cannot be selected in new records that reference a Score
  Component.
- Records that already use this Score Component can still be viewed.
