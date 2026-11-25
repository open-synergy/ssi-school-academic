# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolSubjectOutcomeObjective(models.Model):
    """Represents one learning objective (TP) of a learning outcome.

    A learning objective has a code and a description. The teacher
    links it to the daily tests and assignments of a score sheet, and
    the description is printed as the learning objective achievement of
    the report card.
    """

    _name = "school_subject_outcome_objective"
    _description = "School Subject Outcome Objective"
    _rec_name = "code"
    _order = "outcome_id, sequence, id"

    outcome_id = fields.Many2one(
        string="Learning Outcome",
        comodel_name="school_subject_outcome",
        required=True,
        ondelete="cascade",
        help="Learning outcome this objective belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Order of the objective. It sets the order of the "
        "descriptions on the report card.",
    )
    code = fields.Char(
        string="Code",
        required=True,
        help="Short code of the learning objective.",
    )
    description = fields.Text(
        string="Description",
        required=True,
        help="Description of the learning objective. It is printed as "
        "the learning objective achievement of the report card.",
    )
    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        related="outcome_id.subject_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Subject of the selected Learning Outcome.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        related="outcome_id.grade_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Grade of the selected Learning Outcome.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        related="outcome_id.academic_term_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Academic term of the selected Learning Outcome.",
    )
    score_sheet_component_ids = fields.Many2many(
        string="Score Sheet Components",
        comodel_name="school_score_sheet_component",
        relation="school_score_sheet_component_objective_rel",
        column1="objective_id",
        column2="sheet_component_id",
        readonly=True,
        help="Daily tests and assignments of the score sheets that "
        "measure this objective. They are chosen on the score sheet.",
    )
