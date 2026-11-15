# Create Score Predicate

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_predicate`\
> **Menu:** School > Configuration > Subject & Scoring > Score Predicates\
> **Actor:** user in group `Score Predicate`

## Pre-Condition

- **Data:** At least one **Grade** already exists, because a predicate table applies to
  existing Grades.
- **Access:** User is in group `Score Predicate`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Score Predicates** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the predicate table (e.g. "Senior High
     Predicate").
   - **Code** _(required)_: Enter a unique code identifying this table, or enter **/**
     if you do not need a unique identifier.
4. On the **Applicability** tab, set the grades:
   - **Applicable Grades** _(required)_: Select every Grade the table applies to.
5. On the **Predicate Lines** tab, click **Add a line** and fill in the line:
   - **Predicate** _(required)_: Enter the predicate code (e.g. "A").
   - **Description**: Enter the meaning of the predicate (e.g. "Very Good").
   - **Minimum Score** _(required)_: Enter the lowest score, from 0 to 100, that earns
     the predicate.
6. Click **Save**.

## Post-Condition

- A new Score Predicate record is created and active.
- Each Predicate Line is saved with the table. A Minimum Score can appear on only one
  line of a table and must be between 0 and 100, otherwise saving is rejected with an
  error message.
- A Grade can belong to only one active Score Predicate table, otherwise saving is
  rejected with an error message.
