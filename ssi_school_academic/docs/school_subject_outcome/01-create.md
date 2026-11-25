# Create Subject Outcome

> **Module:** `ssi_school_academic`\
> **Model:** `school_subject_outcome`\
> **Menu:** School > Configuration > Subject & Scoring > Subject Outcomes\
> **Actor:** user in group `Subject Outcome`

## Pre-Condition

- **Data:** The **Subject**, the **Grade** and the **Academic Term** the outcome is for
  already exist.
- **Access:** User is in group `Subject Outcome`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Subject Outcomes** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the learning outcome (CP).
   - **Code** _(required)_: Enter a unique code identifying this record, or enter **/**
     if you do not need a unique identifier.
   - **Subject** _(required)_: Select the subject.
   - **Grade** _(required)_: Select the grade.
   - **Academic Term** _(required)_: Select the academic term (one term is one
     semester).
4. Open the **Learning Objectives** tab.
5. Click **Add a line** for each learning objective (TP), and fill in the line:
   - **Code** _(required)_: Enter the short code of the objective, for example "TP 1".
   - **Description** _(required)_: Enter the sentence printed on the report card.
   - **Sequence**: Drag the line to set the order of the objectives.
6. Click **Save**.

## Post-Condition

- A new Subject Outcome record is created and active, with its learning objectives.
- Only one active record can exist for the same subject, grade and academic term; a
  second one is refused until the first is archived.
- The **Score Sheet Components** column of an objective stays empty until a teacher
  chooses it on a score sheet.
