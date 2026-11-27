# Create School Curriculum

> **Module:** `ssi_school_academic`\
> **Model:** `school_curriculum`\
> **Menu:** School > Configuration > Subject & Scoring > Curriculums\
> **Actor:** user in group `User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** A **School**, an **Academic Year**, a **Subject** and a **Grade** the
  subject is applicable to already exist.
- **Config:** No other curriculum that is not cancelled exists for the same School and
  Academic Year.
- **Access:** User is in group `User`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Curriculums** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Title** _(required)_: Enter the name of the curriculum.
   - **School** _(required)_: Select the school the curriculum is run in.
   - **Academic Year** _(required)_: Select the academic year of the curriculum.
   - **Effective Start** _(required)_: Enter the first date the curriculum is in force.
   - **Effective End** _(required)_: Enter the last date the curriculum is in force.
4. On the **Lines** tab, click **Add a line** and fill in:
   - **Subject** _(required)_: Select the subject.
   - **Grade** _(required)_: Select a grade the subject is applicable to.
   - **Weekly Hours** _(required)_: Enter the weekly hours (JP) of one class.
   - **Total Class** _(required)_: Enter the number of classes that take the subject.
5. Click **Save**.

## Post-Condition

- A new School Curriculum record is created in **Draft** status.
- **Category** of each line is filled from the subject group, and **Total Time** is
  **Weekly Hours** times **Total Class**.
- The document number stays `/` until the curriculum is approved.
- Saving is rejected with an error when the school already has a curriculum that is not
  cancelled for the same academic year, when **Effective Start** is later than
  **Effective End**, when a grade is not applicable to its subject, when a subject is
  listed twice for the same grade, or when **Weekly Hours** or **Total Class** is
  below 1.
