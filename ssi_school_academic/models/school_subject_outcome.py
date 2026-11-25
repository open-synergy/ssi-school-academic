# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolSubjectOutcome(models.Model):
    """Represents the learning outcomes (CP) of a subject.

    A learning outcome record is the master data of one subject, one
    grade and one academic term. It holds the list of learning
    objectives (TP) the teachers measure with their daily tests and
    assignments. Only one active record may exist for the same subject,
    grade and academic term.
    """

    _name = "school_subject_outcome"
    _inherit = ["mixin.master_data"]
    _description = "School Subject Outcome"
    _order = "subject_id, grade_id, academic_term_id, id"

    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        required=True,
        ondelete="restrict",
        help="Subject the learning outcome belongs to.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        ondelete="restrict",
        help="Grade the learning outcome belongs to.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        ondelete="restrict",
        help="Academic term the learning outcome is valid for. One "
        "academic term is one semester.",
    )
    objective_ids = fields.One2many(
        string="Learning Objectives",
        comodel_name="school_subject_outcome_objective",
        inverse_name="outcome_id",
        help="Learning objectives (TP) that belong to this learning "
        "outcome, in the order they are printed.",
    )

    @api.constrains("subject_id", "grade_id", "academic_term_id", "active")
    def _check_unique_active_outcome(self):
        """Check that only one active outcome exists per scope.

        :raises ValidationError: when another active record exists for
            the same subject, grade and academic term.
        """
        for record in self:
            if not record.active:
                continue
            domain = [
                ("id", "!=", record.id),
                ("active", "=", True),
                ("subject_id", "=", record.subject_id.id),
                ("grade_id", "=", record.grade_id.id),
                ("academic_term_id", "=", record.academic_term_id.id),
            ]
            if self.search_count(domain):
                error_message = (
                    _(
                        """
Context: Save learning outcome
Database ID: %s
Problem: An active learning outcome already exists for this subject, grade, and term.
Solution: Archive the existing learning outcome, or edit it instead
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
