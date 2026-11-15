# Edit Report Card Type

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card_type`\
> **Menu:** School > Configuration > Subject & Scoring > Report Card Types\
> **Actor:** user in group `Report Card Type`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Report Card Type already exists.
- **Access:** User is in group `Report Card Type`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Report Card Types** menu.
2. Find and open the record to edit, then click **Edit**.
3. Change the **Name**.
4. On the **Calculation** tab, change the **Rounding Threshold** (a value above 0 and
   below 1).
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- When you change a weight, keep the average weight plus the line weights at 100%;
  otherwise saving is rejected.
