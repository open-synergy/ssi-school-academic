# Copy Teaching Assignments from the Previous Term

> **Module:** `ssi_school_academic`\
> **Model:** `school_teaching_assignment`\
> **Menu:** School > Configuration > Subject & Scoring > Copy Teaching Assignments\
> **Actor:** user in group `Teaching Assignment`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The Teaching Assignments of the source term exist.
- **Data:** The homerooms of the target term exist, with the same grade classes as the
  lines to copy.
- **Access:** User is in group `Teaching Assignment`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Copy Teaching Assignments**
   menu. A dialog opens.
2. Fill in the required fields:
   - **Source Term** _(required)_: Select the term whose assignments are copied. Every
     assignment of that term is offered in **Teaching Assignments**; remove from there
     the ones that must not be copied.
   - **Target Term** _(required)_: Select the term the assignments are copied to. It
     must differ from the source term.
3. Click the **Copy** button.
4. Read the **Result**: it gives the number of assignments and lines copied and, for
   each item that was skipped, the reason.
5. Click **Close**.

## Post-Condition

- A Teaching Assignment is created in the target term for every teacher who had none
  there. Its lines are moved to the homeroom of the target term that has the same grade
  class, and keep the subject, the role and the weekly hours.
- A line is skipped when the target term has no such homeroom or more than one, or when
  its subject already has a main teacher in the target term. An assignment is skipped
  when the teacher already has one in the target term. Everything skipped is named in
  the **Result**.
