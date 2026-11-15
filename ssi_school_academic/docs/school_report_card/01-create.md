# Create School Report Card

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card`\
> **Menu:** School > Classroom > Report Cards\
> **Actor:** user in group `User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** An **Open** enrollment and a **Report Card Type** already exist.
- **Config:** No other report card that is not cancelled exists for the same enrollment
  and Report Card Type.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Classroom > Report Cards** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Enrollment** _(required)_: Select the open enrollment of the student. Only open
     enrollments are offered. **Student**, **Academic Year**, **Academic Term**,
     **Grade**, **Grade Class**, and **Homeroom** are filled from the enrollment.
   - **Report Card Type** _(required)_: Select the kind of report card, for example
     Mid-Term or Final.
   - **Print City**: Enter the city printed next to the signature.
   - **Print Date**: Defaults to today's date.
4. Click **Save**.

## Post-Condition

- A new School Report Card record is created in **Draft** status.
- Saving is rejected with an error when the enrollment is not open.
- Saving is rejected with an error when another report card that is not cancelled exists
  for the same enrollment and Report Card Type.
