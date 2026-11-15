# Create School Report Card

> **Module:** `ssi_school_academic_operating_unit`\
> **Extends:** ssi_school_academic — model `school_report_card`, action `01-create`

## Additional Pre-Condition

- **Access:** The user is a member of the **Operating Unit / Multiple Operating Units**
  group (`operating_unit.group_multi_operating_unit`). Without this group the Operating
  Unit field described below is not rendered on the form — there is no error message,
  the field simply does not appear.
- **Module:** `ssi_school_academic_operating_unit` is installed.

## Additional Fields

When this module is installed, the create form gains one field, shown only to users in
the **Operating Unit / Multiple Operating Units** group
(`operating_unit.group_multi_operating_unit`):

- **Operating Unit**: The operating unit the report card belongs to. Displayed after the
  **Company** field. Automatically filled with the default operating unit of the user.
  Change it if needed.

## Modified — Record Visibility

- The report cards list is filtered by operating unit (record rule). A user in the
  **Operating Unit** data ownership group of this module only sees report cards whose
  operating unit is in the list of operating units assigned to that user. This is not a
  Flow step.
