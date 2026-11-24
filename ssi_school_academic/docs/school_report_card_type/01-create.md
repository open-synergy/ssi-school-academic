# Create Report Card Type

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card_type`\
> **Menu:** School > Configuration > Subject & Scoring > Report Card Types\
> **Actor:** user in group `Report Card Type`

## Pre-Condition

- **Data:** The **Score Components** used by the report card already exist, because a
  report card type can only average or weight existing components.
- **Access:** User is in group `Report Card Type`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Report Card Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the report card type (e.g. "Mid-Term").
   - **Code** _(required)_: Enter a unique code identifying this type, or enter **/** if
     you do not need a unique identifier.
   - **Term Type** _(required)_: Select **Mid-Term** or **Final**.
4. On the **Calculation** tab, set how the final score is calculated:
   - **Averaged Components**: Select the components whose scores are averaged (e.g. "UH
     1" and "Tugas 1").
   - **Average Weight (%)**: Enter the weight, in percent, of that average.
   - **Rounding Threshold** _(required)_: Defaults to **0.56**. A final score whose
     decimal part reaches this value is rounded up.
5. Still on the **Calculation** tab, click **Add a line** for every other component and
   fill in the line:
   - **Component** _(required)_: Select the component (e.g. "PTS").
   - **Weight (%)** _(required)_: Enter the weight, in percent, of the component.
6. Optionally, on the **Display** tab, click **Add a line** under **Printed Columns**
   for every score component column printed on the Mid-Term report card (at most four),
   and fill in the line:
   - **Component** _(required)_: Select the component (e.g. "UH 1"). A component can be
     printed once per report card type.
   - **Print Title**: Enter the title printed above the column (e.g. "SUM1"). Leave it
     empty to print the name of the component.
   - **Sequence**: Drag the handle of the line to set its position among the columns.
7. Click **Save**.

## Post-Condition

- A new Report Card Type record is created and active.
- The Mid-Term report card of this type prints exactly the **Printed Columns** lines, in
  order, plus the final score.
- Saving is rejected with an error message when the average weight plus the line weights
  do not total 100%, when a component is both averaged and weighted (or weighted on two
  lines), when an average weight is set without averaged components, when the rounding
  threshold is not between 0 and 1, when more than four printed columns are set, or when
  a component is printed on two columns.
