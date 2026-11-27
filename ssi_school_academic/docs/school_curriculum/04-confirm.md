# Confirm School Curriculum

> **Module:** `ssi_school_academic`\
> **Model:** `school_curriculum`\
> **Menu:** School > Configuration > Subject & Scoring > Curriculums\
> **Actor:** user in group `User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Curriculums** menu.
2. Open the curriculum to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**, shown on the statusbar.
- Approval records are created for each approver level defined by the approval template.
