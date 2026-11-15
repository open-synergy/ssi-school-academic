# Reject School Score Sheet

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_sheet`\
> **Menu:** School > Classroom > Score Sheets\
> **Actor:** approver on the pending approval level\
> **State:** `confirm` → `reject`\
> **Requires:** `03-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `reject_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**.

## Flow

1. Open the **School > Classroom > Score Sheets** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**, shown on the statusbar.
- The scores are untouched.
