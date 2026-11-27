# Cancel School Curriculum

> **Module:** `ssi_school_academic`\
> **Model:** `school_curriculum`\
> **Menu:** School > Configuration > Subject & Scoring > Curriculums\
> **Actor:** user in group `Validator`\
> **State:** `draft` | `confirm` | `open` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **On Progress**.
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Data:** A **Cancellation Reason** that can be used for this model exists.
- **Access:** User is in group `Validator`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Curriculums** menu.
2. Open the curriculum to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**, shown on the statusbar.
- A new curriculum for the same School and Academic Year can be created.
