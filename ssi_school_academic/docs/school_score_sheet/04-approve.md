# Approve School Score Sheet

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_sheet`\
> **Menu:** School > Classroom > Score Sheets\
> **Actor:** approver of the approval level\
> **State:** `confirm` → `done`\
> **Requires:** `03-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` for state `confirm`; the
  actor is an active approver of the document.
- **Access:** User is the active approver.

## Flow

1. Open the **School > Classroom > Score Sheets** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**, shown on the statusbar, when every approval level is
  fulfilled.
- A document number is assigned.
