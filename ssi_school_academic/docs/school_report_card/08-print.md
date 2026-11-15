# Print School Report Card

> **Module:** `ssi_school_academic`\
> **Model:** `school_report_card`\
> **Menu:** School > Classroom > Report Cards\
> **Actor:** user in group `Viewer`\
> **State:** `done` (unchanged)\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Done**. The report card of a finished enrollment can still be
  printed.
- **Data:** The lines of the report card hold their final scores. The **Phase** of the
  grade, the **NUPTK** of the homeroom teacher, and the address of the school are
  filled, otherwise their places on the print stay empty.
- **Config:** The **Report Card Type** lists the score components to show as columns, up
  to four. A fifth component and the ones after it are not printed.
- **Access:** User is in group `Viewer` of the report card.

## Flow

1. Open the **School > Classroom > Report Cards** menu.
2. Open the record to print.
3. Click the **Print** button in the toolbar.
4. Select **Report Card**.
5. Open the downloaded PDF file.

## Post-Condition

- A PDF file of the report card is downloaded. Its header on every page shows the
  student, the school, the class, the phase and the semester; its footer shows the
  class, the student name, the student ID and the page number.
- A **Mid-Term** report card shows the score component columns of the report card type;
  a **Final** report card shows only the final score and the competency achievement.
- The Co-Curricular, Extracurricular, Homeroom Teacher Note and Parent Response blocks
  are printed only when they are filled. The Absences block is always printed.
- The report card itself is unchanged.
