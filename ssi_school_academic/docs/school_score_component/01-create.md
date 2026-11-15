# Create Score Component

> **Module:** `ssi_school_academic`\
> **Model:** `school_score_component`\
> **Menu:** School > Configuration > Subject & Scoring > Score Components\
> **Actor:** user in group `Score Component`

## Pre-Condition

- **Access:** User is in group `Score Component`.

## Flow

1. Open the **School > Configuration > Subject & Scoring > Score Components** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of one slot (e.g. "UH 1").
   - **Code** _(required)_: Enter a unique code identifying this component, or enter
     **/** if you do not need a unique identifier.
   - **Category** _(required)_: Select **Daily Test**, **Assignment**, **Mid-Term Exam**
     or **Final Exam**.
   - **Sequence**: Defaults to **10**. Enter a lower number to place the component
     earlier.
4. Click **Save**.

## Post-Condition

- A new Score Component record is created and active.
- One record is one slot. To use three daily tests, create three components with the
  **Daily Test** category.
