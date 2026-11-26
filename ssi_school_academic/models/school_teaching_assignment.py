# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolTeachingAssignment(models.Model):
    """Represents what one teacher teaches in one academic term.

    A teaching assignment is the master data of one teacher and one
    academic term. Its lines list the homerooms the teacher teaches,
    the subject of each homeroom, the role of the teacher (main or
    assistant) and the weekly hours. The assignment is the source the
    score sheets of the main teacher are generated from, and it tells
    which score sheets an assistant teacher may read. Only one
    assignment may exist for the same teacher and academic term.
    """

    _name = "school_teaching_assignment"
    _inherit = ["mixin.master_data"]
    _description = "School Teaching Assignment"
    _order = "academic_term_id, teacher_id, id"

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
        help="Company the teaching assignment belongs to.",
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        required=True,
        ondelete="restrict",
        help="Teacher whose teaching assignment is recorded.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        ondelete="restrict",
        default=lambda self: self._default_academic_term_id(),
        help="Academic term the teaching assignment is valid for. One "
        "academic term is one semester.",
    )
    line_ids = fields.One2many(
        string="Lines",
        comodel_name="school_teaching_assignment_line",
        inverse_name="assignment_id",
        help="Homerooms and subjects the teacher teaches in the term, "
        "each with the role of the teacher and the weekly hours.",
    )
    main_weekly_hours = fields.Integer(
        string="Main Weekly Hours",
        compute="_compute_weekly_hours",
        store=True,
        compute_sudo=True,
        help="Total weekly hours of the lines where the teacher is the "
        "main teacher.",
    )
    assistant_weekly_hours = fields.Integer(
        string="Assistant Weekly Hours",
        compute="_compute_weekly_hours",
        store=True,
        compute_sudo=True,
        help="Total weekly hours of the lines where the teacher is an "
        "assistant teacher.",
    )
    total_weekly_hours = fields.Integer(
        string="Total Weekly Hours",
        compute="_compute_weekly_hours",
        store=True,
        compute_sudo=True,
        help="Total weekly hours of all the lines, whatever the role "
        "of the teacher.",
    )

    @api.model
    def _default_academic_term_id(self):
        """Return the first academic term that is on progress.

        Shared with the score sheet, so both documents offer the same
        default term.

        :return: a ``school_academic_term`` record, empty when no term
            is on progress
        """
        return self.env["school_academic_term"].search(
            [("state", "=", "open")], limit=1
        )

    @api.depends(
        "line_ids.role",
        "line_ids.weekly_hours",
    )
    def _compute_weekly_hours(self):
        """Sum the weekly hours of the lines per role and in total.

        The main and the assistant hours add the lines of that role,
        and the total adds every line.
        """
        for record in self:
            main_hours = 0
            assistant_hours = 0
            for line in record.line_ids:
                if line.role == "main":
                    main_hours += line.weekly_hours
                else:
                    assistant_hours += line.weekly_hours
            record.main_weekly_hours = main_hours
            record.assistant_weekly_hours = assistant_hours
            record.total_weekly_hours = main_hours + assistant_hours

    @api.constrains("teacher_id", "academic_term_id")
    def _check_unique_teacher_term(self):
        """Check that a teacher has one assignment per academic term.

        :raises ValidationError: when another assignment exists for the
            same teacher and academic term.
        """
        for record in self:
            domain = [
                ("id", "!=", record.id),
                ("teacher_id", "=", record.teacher_id.id),
                ("academic_term_id", "=", record.academic_term_id.id),
            ]
            if self.search_count(domain):
                error_message = (
                    _(
                        """
Context: Save teaching assignment
Database ID: %s
Problem: This teacher already has a teaching assignment in this term.
Solution: Edit the existing teaching assignment, or archive it first
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
