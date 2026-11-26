# Create Teaching Assignment

> **Module:** `ssi_school_academic_operating_unit`\
> **Extends:** ssi_school_academic — model `school_teaching_assignment`, action `01-create`

## Additional Pre-Condition

- **Access:** The user is a member of the **Operating Unit / Multiple Operating Units**
  group (`operating_unit.group_multi_operating_unit`). Without this group the Operating
  Units field described below is not rendered on the form — there is no error message,
  the field simply does not appear.
- **Module:** `ssi_school_academic_operating_unit` is installed.

## Additional Fields

When this module is installed, the create form gains one field, shown only to users in
the **Operating Unit / Multiple Operating Units** group
(`operating_unit.group_multi_operating_unit`):

- **Operating Unit**: The operating units the teaching assignment belongs to. Displayed
  after the **Company** field. Select one or more units, or leave it empty to make the
  assignment visible to every unit. The lines of the assignment have no operating unit
  of their own; they follow the assignment. The score sheets made from the assignment by
  the generate wizard get the operating unit of the homeroom of each line when the
  homeroom has one. When the homeroom has none, they get the operating unit of the
  assignment if it has exactly one unit, and the default operating unit of the user who
  runs the wizard otherwise. The assignment made by the copy wizard keeps the operating
  units of the source assignment.

## Modified — Record Visibility

- The teaching assignments list is filtered by operating unit (record rule). A user only
  sees the teaching assignments that have no operating unit, or that have at least one
  of the operating units assigned to that user. This is not a Flow step.
