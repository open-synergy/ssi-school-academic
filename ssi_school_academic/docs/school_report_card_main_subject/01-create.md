# Create Report Card Main Subject

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card_main_subject`\
> **Menu:** School > Configuration > Subject & Scoring > Main Subjects\
> **Actor:** user in group `Report Card Main Subject`

## Pre-Condition

- **Access:** User is in group `Report Card Main Subject`.
- **Data:** The Grade and the Subjects to choose already exist.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Main Subjects** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the record (e.g. "Grade 10 Main
     Subjects").
   - **Code** _(required)_: Enter a unique code identifying this record, or enter **/**
     if you do not need a unique identifier.
   - **Grade** _(required)_: Select the grade the main subjects apply to.
   - **Expertise Program**: Enter the expertise program exactly as written on the grade
     class. Leave it empty to set the main subjects of the whole grade.
   - **Main Subjects** _(required)_: Select at least one subject.
4. Click **Save**.

## Post-Condition

- A new Report Card Main Subject record is created and active.
- A record with an **Expertise Program** applies to the classes of that grade and
  program. A record with an empty **Expertise Program** applies to every class of the
  grade that has no record of its own program.
- Only one active record is allowed for the same grade and expertise program.
