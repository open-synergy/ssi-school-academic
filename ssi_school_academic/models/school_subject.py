# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolSubject(models.Model):
    """
    Represents a subject taught at the school, e.g. Mathematics.
    It stores the subject group printed on the report card, the grades
    the subject applies to, and the minimum score (KKM) a student must
    reach on each of those grades to pass the subject.
    """

    _name = "school_subject"
    _inherit = ["mixin.master_data"]
    _description = "School Subject"

    subject_group = fields.Selection(
        string="Subject Group",
        selection=[
            ("general", "General"),
            ("vocational", "Vocational"),
        ],
        default="general",
        required=True,
        help=(
            "Group the subject belongs to on the report card: "
            "General = general subject group, "
            "Vocational = vocational subject group."
        ),
    )
    # grade_ids must be declared before minimum_score_ids: relational
    # fields are created in declaration order, and a minimum score line
    # checks its grade against the applicable grades of the subject.
    grade_ids = fields.Many2many(
        string="Applicable Grades",
        comodel_name="school_grade",
        help=(
            "Grades this subject is taught on. A minimum score can only "
            "be set for one of these grades."
        ),
    )
    minimum_score_ids = fields.One2many(
        string="Minimum Scores",
        comodel_name="school_subject_minimum_score",
        inverse_name="subject_id",
        help=("Minimum score (KKM) of the subject, one line per applicable " "grade."),
    )

    @api.constrains("grade_ids")
    def _check_minimum_score_grade_ids(self):
        """Reject removing a grade that still has a minimum score.

        Re-runs the applicable grade check of every minimum score line,
        so a line left on a grade the subject no longer applies to is
        refused. The check runs after all values of the save are
        written, so removing a grade and its line together passes.

        :raises ValidationError: when a minimum score line is on a grade
            outside ``grade_ids``.
        """
        for record in self.sudo():
            record.minimum_score_ids._check_minimum_score_applicable_grade()
