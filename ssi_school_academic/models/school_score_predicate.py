# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class SchoolScorePredicate(models.Model):
    """
    Represents a score predicate table, e.g. A, B, C and D.
    It stores the grades the table applies to and the predicate lines,
    each with the minimum score that earns the predicate.
    """

    _name = "school_score_predicate"
    _inherit = ["mixin.master_data"]
    _description = "School Score Predicate"

    grade_ids = fields.Many2many(
        string="Applicable Grades",
        comodel_name="school_grade",
        relation="school_score_predicate_grade_rel",
        column1="predicate_id",
        column2="grade_id",
        required=True,
        help=(
            "Grades this predicate table applies to. A grade can belong "
            "to only one active predicate table."
        ),
    )
    line_ids = fields.One2many(
        string="Predicate Lines",
        comodel_name="school_score_predicate_line",
        inverse_name="predicate_id",
        help="Predicate earned from a minimum score, one line per predicate.",
    )

    @api.constrains("grade_ids", "active")
    def _check_grade_single_active_table(self):
        """Reject a grade that belongs to two active predicate tables.

        :raises ValidationError: when
            ``_check_grade_single_active_table_condition`` returns
            False.
        """
        for record in self.sudo():
            if not record._check_grade_single_active_table_condition():
                error_message = (
                    _(
                        """
Context: Validate score predicate
Database ID: %s
Problem: A grade may only belong to one active predicate table.
Solution: Remove the grade from the other active predicate table or archive it
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    def _check_grade_single_active_table_condition(self):
        """Tell whether no other active table shares a grade with this.

        Extension point: override to allow overlapping grades without
        touching the error message.

        :return: True when the table is archived or no other active
            table uses any of its grades; never raises.
        """
        self.ensure_one()
        if not self.active:
            return True
        criteria = [
            ("id", "!=", self.id),
            ("active", "=", True),
            ("grade_ids", "in", self.grade_ids.ids),
        ]
        return self.search_count(criteria) == 0

    def get_predicate_line(self, score):
        """Return the predicate line that applies to a score.

        The line with the highest minimum score that is not above the
        score wins. Scores are compared to two decimals.

        :param float score: score to look up, from 0 to 100.
        :return: the matching predicate line, or an empty recordset
            when no line has a minimum score at or below the score.
        :rtype: recordset of ``school_score_predicate_line``
        """
        self.ensure_one()
        candidates = self.line_ids.filtered(
            lambda line: float_compare(line.min_score, score, precision_digits=2) <= 0
        )
        return candidates.sorted("min_score", reverse=True)[:1]

    @api.model
    def _get_predicate_for_grade(self, grade):
        """Return the active predicate table that applies to a grade.

        :param grade: grade to look up.
        :type grade: recordset of ``school_grade``
        :return: the active predicate table that includes the grade, or
            an empty recordset when no active table includes it.
        :rtype: recordset of ``school_score_predicate``
        """
        return self.search(
            [("active", "=", True), ("grade_ids", "in", grade.ids)], limit=1
        )
