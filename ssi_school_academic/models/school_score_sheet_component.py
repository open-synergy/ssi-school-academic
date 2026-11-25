# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolScoreSheetComponent(models.Model):
    """Represents one score component of a score sheet.

    A record links a score sheet to one daily test or assignment
    component, and holds the learning objectives (TP) that component
    measures on that sheet. The objectives must belong to the learning
    outcome of the subject, the grade and the academic term of the
    sheet.
    """

    _name = "school_score_sheet_component"
    _description = "School Score Sheet Component"
    _order = "sheet_id, component_id"

    sheet_id = fields.Many2one(
        string="Score Sheet",
        comodel_name="school_score_sheet",
        required=True,
        ondelete="cascade",
        help="Score sheet this component belongs to.",
    )
    component_id = fields.Many2one(
        string="Score Component",
        comodel_name="school_score_component",
        required=True,
        ondelete="restrict",
        domain="[('category', 'in', ['daily_test', 'assignment'])]",
        help="Daily test or assignment component of the sheet.",
    )
    objective_ids = fields.Many2many(
        string="Learning Objectives",
        comodel_name="school_subject_outcome_objective",
        relation="school_score_sheet_component_objective_rel",
        column1="sheet_component_id",
        column2="objective_id",
        help="Learning objectives (TP) this component measures. Only "
        "objectives of the subject, the grade and the academic term of "
        "the score sheet can be chosen.",
    )

    def name_get(self):
        """Return the display name of each record.

        The name is the score component followed by the number of the
        score sheet, for example ``UH 1 (SSS/2026/000018)``. A draft
        sheet has no number yet and shows ``/``.

        The names are read with ``sudo()``: the display name is shown
        wherever the component is a tag, for example on the learning
        objective form, and the user may not read the score sheet
        itself because of its record rule. Only the name string leaves
        this method; no elevated recordset is returned.

        :return: list of ``(id, display name)`` pairs.
        :rtype: list
        """
        result = []
        for record in self.sudo():
            name = "%s (%s)" % (
                record.component_id.name or "",
                record.sheet_id.name or "",
            )
            result.append((record.id, name))
        return result

    @api.constrains("sheet_id", "component_id")
    def _check_unique_component(self):
        """Check that a sheet has one record per component.

        :raises ValidationError: when another record of the same sheet
            has the same score component.
        """
        for record in self:
            domain = [
                ("id", "!=", record.id),
                ("sheet_id", "=", record.sheet_id.id),
                ("component_id", "=", record.component_id.id),
            ]
            if self.search_count(domain):
                error_message = (
                    _(
                        """
Context: Save score sheet component
Database ID: %s
Problem: Component %s may only appear once per score sheet.
Solution: Remove the duplicate component
"""
                    )
                    % (record.id, record.display_name)
                )
                raise ValidationError(error_message)

    @api.constrains("objective_ids", "sheet_id")
    def _constrains_objective_scope(self):
        """Check the objectives against the scope of the sheet.

        :raises ValidationError: when an objective does not belong to
            the subject, grade and academic term of the sheet.
        """
        self._check_objective_scope()

    def _check_objective_scope(self):
        """Raise when an objective is outside the scope of the sheet.

        Shared by the constraint of this model and by the constraint of
        the score sheet, which runs it when the subject, the grade class
        or the academic term of the sheet changes.

        :raises ValidationError: when an objective belongs to another
            subject, grade or academic term than the sheet.
        """
        for record in self:
            sheet = record.sheet_id
            for objective in record.objective_ids:
                if (
                    objective.subject_id != sheet.subject_id
                    or objective.grade_id != sheet.grade_class_id.grade_id
                    or objective.academic_term_id != sheet.academic_term_id
                ):
                    error_message = (
                        _(
                            """
Context: Save score sheet component
Database ID: %s
Problem: Objective %s is outside the subject, grade, and term of sheet component %s.
Solution: Choose only objectives of the same subject, grade, and term as the sheet
"""
                        )
                        % (record.id, objective.display_name, record.display_name)
                    )
                    raise ValidationError(error_message)
