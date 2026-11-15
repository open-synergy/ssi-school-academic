# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolScorePredicateLine(models.Model):
    """
    Detail line of ``school_score_predicate``.
    One line stores one predicate, e.g. "A", and the minimum score a
    student must reach to earn it.
    """

    _name = "school_score_predicate_line"
    _description = "School Score Predicate Line"
    _order = "min_score desc, id"

    predicate_id = fields.Many2one(
        string="# Predicate Table",
        comodel_name="school_score_predicate",
        required=True,
        ondelete="cascade",
        help="Predicate table this line belongs to.",
    )
    name = fields.Char(
        string="Predicate",
        required=True,
        help="Predicate code printed on the report card, e.g. A.",
    )
    description = fields.Char(
        string="Description",
        help="Meaning of the predicate, e.g. Very Good.",
    )
    min_score = fields.Float(
        string="Minimum Score",
        required=True,
        help="Lowest score, from 0 to 100, that earns this predicate.",
    )

    @api.constrains("predicate_id", "min_score")
    def _check_min_score_unique(self):
        """Reject a minimum score used twice in one predicate table.

        :raises ValidationError: when ``_check_min_score_unique_condition``
            returns False.
        """
        for line in self.sudo():
            if not line._check_min_score_unique_condition():
                error_message = (
                    _(
                        """
Context: Validate score predicate line
Database ID: %s
Problem: Minimum scores within a predicate table must be unique.
Solution: Change or remove the lines that share the same minimum score
"""
                    )
                    % (line.id,)
                )
                raise ValidationError(error_message)

    def _check_min_score_unique_condition(self):
        """Tell whether the minimum score is used once in the table.

        Extension point: override to allow repeated minimum scores
        without touching the error message.

        :return: True when no other line of the table has the same
            minimum score; never raises.
        """
        self.ensure_one()
        criteria = [
            ("predicate_id", "=", self.predicate_id.id),
            ("min_score", "=", self.min_score),
            ("id", "!=", self.id),
        ]
        return self.search_count(criteria) == 0

    @api.constrains("min_score")
    def _check_min_score_range(self):
        """Reject a minimum score outside the 0 to 100 range.

        :raises ValidationError: when ``_check_min_score_range_condition``
            returns False.
        """
        for line in self.sudo():
            if not line._check_min_score_range_condition():
                error_message = (
                    _(
                        """
Context: Validate score predicate line
Database ID: %s
Problem: Minimum score must be between 0 and 100.
Solution: Enter a minimum score from 0 to 100
"""
                    )
                    % (line.id,)
                )
                raise ValidationError(error_message)

    def _check_min_score_range_condition(self):
        """Tell whether the minimum score is between 0 and 100.

        Extension point: override to change the accepted range without
        touching the error message.

        :return: True when ``min_score`` is within 0 and 100 inclusive;
            never raises.
        """
        self.ensure_one()
        return 0.0 <= self.min_score <= 100.0
