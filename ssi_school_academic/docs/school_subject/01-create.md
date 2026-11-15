# Create Subject

> **Module:** `ssi_school_academic`\
> **Model:** `school_subject`\
> **Menu:** School > Configuration > Subject & Scoring > Subjects\
> **Actor:** user in group `Subject`

## Pre-Condition

- **Data:** At least one **Grade** already exists, because the subject can only apply to
  existing Grades.
- **Access:** User is in group `Subject`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Subjects** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the subject (e.g. "Mathematics").
   - **Code** _(required)_: Enter a unique code identifying this subject, or enter **/**
     if you do not need a unique identifier.
4. On the **Applicability** tab, set the classification of the subject:
   - **Subject Group** _(required)_: Defaults to **General**. Select **Vocational** for
     a vocational subject.
   - **Applicable Grades**: Select every Grade the subject is taught on.
5. On the **Minimum Score** tab, click **Add a line** and fill in the line:
   - **Grade** _(required)_: Select one of the Applicable Grades.
   - **Minimum Score** _(required)_: Enter the minimum score (KKM) from 0 to 100.
6. Click **Save**.

## Post-Condition

- A new Subject record is created and active.
- Each Minimum Score line is saved with the Subject. A Grade can appear on only one
  line, the score must be between 0 and 100, and the Grade must be one of the Applicable
  Grades — otherwise saving is rejected with an error message.
