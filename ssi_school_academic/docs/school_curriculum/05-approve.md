# Approve School Curriculum

> **Module:** `ssi_school_academic`\
> **Model:** `school_curriculum`\
> **Menu:** School > Configuration > Subject & Scoring > Curriculums\
> **Actor:** approver of the approval level\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` for state `confirm`; the
  actor is an active approver of the document.
- **Record:** The school has no other curriculum that is **On Progress**.
- **Access:** User is the active approver.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Curriculums** menu.
2. Open the curriculum to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **On Progress**, shown on the statusbar, when every approval level
  is fulfilled.
- A document number is assigned.
- Approving is rejected with an error when another curriculum of the same school is
  already **On Progress**.
