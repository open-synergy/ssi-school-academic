# Finish School Curriculum

> **Module:** `ssi_school_academic`\
> **Model:** `school_curriculum`\
> **Menu:** School > Configuration > Subject & Scoring > Curriculums\
> **Actor:** user in group `User`\
> **State:** `open` → `done`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` for this model grants `done_ok` for state
  `open` to the actor's group.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Curriculums** menu.
2. Open the curriculum to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**, shown on the statusbar.
- The school can now open another curriculum.
