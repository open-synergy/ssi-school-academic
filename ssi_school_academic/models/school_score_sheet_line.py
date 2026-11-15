# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolScoreSheetLine(models.Model):
    """Represents one score of a student on a score sheet.

    A line holds the score of one enrollment for one score component,
    for example the score of a student for the first daily test. A line
    without a score has not been scored yet, which is not the same as a
    score of zero.
    """

    _name = "school_score_sheet_line"
    _description = "School Score Sheet Line"
    _order = "student_id, component_id"

    sheet_id = fields.Many2one(
        string="Score Sheet",
        comodel_name="school_score_sheet",
        required=True,
        ondelete="cascade",
        help="Score sheet this line belongs to.",
    )
    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        required=True,
        ondelete="restrict",
        help="Enrollment of the student the score is given to. It must " "be open.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        related="enrollment_id.student_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Student of the selected Enrollment.",
    )
    component_id = fields.Many2one(
        string="Score Component",
        comodel_name="school_score_component",
        required=True,
        ondelete="restrict",
        help="Score component the score is given for, for example " "Daily Test 1.",
    )
    score = fields.Float(
        string="Score",
        help="Score between 0 and 100. Leave it empty while the "
        "student is not scored yet; that is not the same as zero.",
    )

    @api.constrains("score")
    def _check_score_range(self):
        """Check that a score stays between 0 and 100.

        :raises ValidationError: when a score is below 0 or above 100.
        """
        for record in self:
            if record.score < 0.0 or record.score > 100.0:
                error_message = (
                    _(
                        """
Context: Save score
Database ID: %s
Problem: Score must be between 0 and 100.
Solution: Enter a score from 0 to 100
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("sheet_id", "enrollment_id", "component_id")
    def _check_unique_component(self):
        """Check that a student has one score per component.

        :raises ValidationError: when another line of the same sheet
            has the same enrollment and score component.
        """
        for record in self:
            domain = [
                ("id", "!=", record.id),
                ("sheet_id", "=", record.sheet_id.id),
                ("enrollment_id", "=", record.enrollment_id.id),
                ("component_id", "=", record.component_id.id),
            ]
            if self.search_count(domain):
                error_message = (
                    _(
                        """
Context: Save score
Database ID: %s
Problem: Each student may only have one score per component.
Solution: Remove the duplicate line
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("enrollment_id")
    def _constrains_enrollment_open(self):
        """Check that a score is entered for an open enrollment.

        :raises ValidationError: when the enrollment is not open.
        """
        self._check_enrollment_open()

    def _check_enrollment_open(self):
        """Raise when a line belongs to an enrollment that is not open.

        Shared by the constraint of the line and by the check of the
        sheet on confirm, so both apply the same rule.

        :raises ValidationError: when the enrollment is not open.
        """
        for record in self:
            if record.enrollment_id.state != "open":
                error_message = (
                    _(
                        """
Context: Check score line
Database ID: %s
Problem: Scores may only be entered for open enrollments.
Solution: Remove the lines of enrollments that are not open
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
