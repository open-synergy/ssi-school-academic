# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolSubjectMinimumScore(models.Model):
    """
    Detail line of ``school_subject``.
    One line stores the minimum score (KKM) a student must reach to pass
    the subject on one grade, so a subject taught on several grades keeps
    one line per grade.
    """

    _name = "school_subject_minimum_score"
    _description = "School Subject Minimum Score"
    _order = "subject_id, id"

    subject_id = fields.Many2one(
        string="# Subject",
        comodel_name="school_subject",
        required=True,
        ondelete="cascade",
        help="Subject this minimum score belongs to.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        ondelete="restrict",
        help="Grade this minimum score applies to.",
    )
    minimum_score = fields.Float(
        string="Minimum Score",
        required=True,
        help=(
            "Minimum score (KKM) a student must reach to pass the subject "
            "on this grade, from 0 to 100."
        ),
    )

    @api.constrains("subject_id", "grade_id")
    def _check_minimum_score_unique_grade(self):
        """Reject a second minimum score of the same grade in a subject.

        :raises ValidationError: when ``_check_minimum_score_unique_grade_condition``
            returns False.
        """
        for line in self.sudo():
            if not line._check_minimum_score_unique_grade_condition():
                error_message = (
                    _(
                        """
Context: Validate subject minimum score
Database ID: %s
Problem: Each grade may only have one minimum score per subject.
Solution: Remove or merge the minimum score lines of the same grade
"""
                    )
                    % (line.id,)
                )
                raise ValidationError(error_message)

    def _check_minimum_score_unique_grade_condition(self):
        """Tell whether the grade is used once in the subject.

        Extension point: override to relax or tighten the rule without
        touching the error message.

        :return: True when no other line of the subject uses the same
            grade; never raises.
        """
        self.ensure_one()
        criteria = [
            ("subject_id", "=", self.subject_id.id),
            ("grade_id", "=", self.grade_id.id),
            ("id", "!=", self.id),
        ]
        return self.search_count(criteria) == 0

    @api.constrains("minimum_score")
    def _check_minimum_score_range(self):
        """Reject a minimum score outside the 0 to 100 range.

        :raises ValidationError: when ``_check_minimum_score_range_condition``
            returns False.
        """
        for line in self.sudo():
            if not line._check_minimum_score_range_condition():
                error_message = (
                    _(
                        """
Context: Validate subject minimum score
Database ID: %s
Problem: Minimum score must be between 0 and 100.
Solution: Enter a minimum score from 0 to 100
"""
                    )
                    % (line.id,)
                )
                raise ValidationError(error_message)

    def _check_minimum_score_range_condition(self):
        """Tell whether the minimum score is between 0 and 100.

        Extension point: override to change the accepted range without
        touching the error message.

        :return: True when ``minimum_score`` is within 0 and 100
            inclusive; never raises.
        """
        self.ensure_one()
        return 0.0 <= self.minimum_score <= 100.0

    @api.constrains("subject_id", "grade_id")
    def _check_minimum_score_applicable_grade(self):
        """Reject a grade that the subject does not apply to.

        :raises ValidationError: when
            ``_check_minimum_score_applicable_grade_condition`` returns
            False.
        """
        for line in self.sudo():
            if not line._check_minimum_score_applicable_grade_condition():
                error_message = (
                    _(
                        """
Context: Validate subject minimum score
Database ID: %s
Problem: Minimum score grade must be one of the applicable grades of the subject.
Solution: Add the grade to the applicable grades of the subject
"""
                    )
                    % (line.id,)
                )
                raise ValidationError(error_message)

    def _check_minimum_score_applicable_grade_condition(self):
        """Tell whether the grade is an applicable grade of the subject.

        Extension point: override to allow grades outside the applicable
        ones without touching the error message.

        :return: True when ``grade_id`` is in ``subject_id.grade_ids``;
            never raises.
        """
        self.ensure_one()
        return self.grade_id in self.subject_id.grade_ids
