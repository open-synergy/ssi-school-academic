# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolScoreSheetLine(models.Model):
    """Represents one score of a student on a score sheet.

    A line holds the score of one enrollment for one score component,
    for example the score of a student for the first daily test. A line
    without a score has not been scored yet, which is not the same as a
    score of zero. A line whose column is locked on the score sheet is
    locked too: it cannot be changed, added or removed.
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
    is_scored = fields.Boolean(
        string="Scored",
        default=False,
        readonly=True,
        help="Set when a score was entered, zero included, and cleared "
        "when the score is emptied. A float field reads 0.0 for both "
        "an empty score and a zero score, so this flag tells them "
        "apart.",
    )
    is_locked = fields.Boolean(
        string="Locked",
        compute="_compute_is_locked",
        store=True,
        compute_sudo=True,
        help="Set when the column of this line is locked on the score "
        "sheet. The report card reads only the scores of locked "
        "columns, and the score of a locked line cannot be changed.",
    )

    @api.depends(
        "sheet_id",
        "component_id",
        "sheet_id.column_ids.is_locked",
        "sheet_id.column_ids.component_id",
    )
    def _compute_is_locked(self):
        """Compute whether the column of the line is locked.

        The line is locked when the sheet has a locked column record for
        the score component of the line.
        """
        for record in self:
            result = False
            for column in record.sheet_id.column_ids:
                if column.component_id == record.component_id and column.is_locked:
                    result = True
            record.is_locked = result

    @api.model_create_multi
    def create(self, vals_list):
        """Create lines and set the scored flag of each one.

        A line cannot be created in a locked column. The column record
        of each new line is added when the sheet has none yet.

        :param list vals_list: values of the lines to create.
        :return: the new lines.
        :rtype: recordset of ``school_score_sheet_line``
        :raises UserError: when a line is added to a locked column.
        """
        for vals in vals_list:
            self._check_target_unlocked(vals.get("sheet_id"), vals.get("component_id"))
            if "score" in vals:
                vals["is_scored"] = self._is_score_filled(vals["score"])
        result = super().create(vals_list)
        if not self.env.context.get("skip_column_upsert"):
            result.mapped("sheet_id")._upsert_component_records()
        return result

    def write(self, vals):
        """Write lines and keep the scored flag in step with the score.

        The score, the enrollment and the component of a locked line
        cannot be changed, and a line cannot move into a locked column.

        :param dict vals: values to write.
        :return: True
        :rtype: bool
        :raises UserError: when a locked line or column is touched.
        """
        if {"score", "enrollment_id", "component_id", "sheet_id"} & set(vals):
            self._check_not_locked()
            if "component_id" in vals or "sheet_id" in vals:
                for record in self:
                    self._check_target_unlocked(
                        vals.get("sheet_id", record.sheet_id.id),
                        vals.get("component_id", record.component_id.id),
                    )
        if "score" in vals:
            vals = dict(vals, is_scored=self._is_score_filled(vals["score"]))
        result = super().write(vals)
        if "component_id" in vals or "sheet_id" in vals:
            self.mapped("sheet_id")._upsert_component_records()
        return result

    def unlink(self):
        """Delete lines, refusing the lines of a locked column.

        :return: True
        :rtype: bool
        :raises UserError: when a line of a locked column is deleted.
        """
        self._check_not_locked()
        return super().unlink()

    def _check_not_locked(self):
        """Raise when one of the lines is locked.

        :raises UserError: when a line belongs to a locked column.
        """
        for record in self:
            if record.is_locked:
                error_message = (
                    _(
                        """
Context: Change score line
Database ID: %s
Problem: The column %s is locked, so its scores cannot be changed.
Solution: Unlock the column on the score sheet before changing its scores
"""
                    )
                    % (record.id, record.component_id.display_name)
                )
                raise UserError(error_message)

    @api.model
    def _check_target_unlocked(self, sheet_id, component_id):
        """Raise when a score sheet column is locked.

        :param int sheet_id: id of the score sheet, may be empty
        :param int component_id: id of the score component, may be empty
        :raises UserError: when the column of the sheet is locked.
        """
        if not sheet_id or not component_id:
            return
        column = (
            self.env["school_score_sheet_component"]
            .sudo()
            .search(
                [
                    ("sheet_id", "=", sheet_id),
                    ("component_id", "=", component_id),
                    ("is_locked", "=", True),
                ],
                limit=1,
            )
        )
        if column:
            error_message = (
                _(
                    """
Context: Add score line
Database ID: %s
Problem: The column %s is locked, so no line can be added to it.
Solution: Unlock the column on the score sheet before adding lines
"""
                )
                % (sheet_id, column.component_id.display_name)
            )
            raise UserError(error_message)

    @api.model
    def _is_score_filled(self, score):
        """Tell whether a written score value counts as entered.

        A zero is an entered score. Only ``False`` and ``None`` mean the
        score was emptied, so the test cannot use Python truthiness,
        which treats ``0.0`` as false.

        :param score: the value written to ``score``.
        :return: True when the score was entered, zero included.
        :rtype: bool
        """
        return score is not False and score is not None

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
