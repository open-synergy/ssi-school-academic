# Cancel School Report Card

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card`\
> **Menu:** School > Classroom > Report Cards\
> **Actor:** user in group `Validator`\
> **State:** `draft` | `confirm` | `reject` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Rejected**.
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User is in group `Validator`.

## Flow

1. Open the **School > Classroom > Report Cards** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**, shown on the statusbar.
- A new report card for the same enrollment and Report Card Type can be created.
