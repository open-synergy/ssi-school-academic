# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolReportCardLine(models.Model):
    """Represents one subject row of a report card.

    A line holds the final score of the student for one subject, the
    minimum score (KKM) of that subject on the grade of the report card
    and the predicate the final score earns. The final score is filled
    by the compute scores action of the report card from the score
    sheets that are done.
    """

    _name = "school_report_card_line"
    _description = "School Report Card Line"
    _order = "report_card_id, subject_id"

    report_card_id = fields.Many2one(
        string="# Report Card",
        comodel_name="school_report_card",
        required=True,
        ondelete="cascade",
        help="Report card this line belongs to.",
    )
    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        required=True,
        ondelete="restrict",
        help="Subject the final score is given for.",
    )
    subject_group = fields.Selection(
        string="Subject Group",
        related="subject_id.subject_group",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Group of the selected Subject on the report card.",
    )
    final_score = fields.Float(
        string="Final Score",
        readonly=True,
        help="Final score of the subject. It is filled by the Compute "
        "Scores button of the report card, not typed by hand.",
    )
    minimum_score = fields.Float(
        string="Minimum Score",
        compute="_compute_minimum_score",
        store=True,
        compute_sudo=True,
        help="Minimum score (KKM) of the subject on the grade of the "
        "report card. It is 0 when the subject has no minimum score "
        "for that grade.",
    )
    predicate_line_id = fields.Many2one(
        string="Predicate",
        comodel_name="school_score_predicate_line",
        compute="_compute_predicate_line_id",
        store=True,
        compute_sudo=True,
        help="Predicate the final score earns in the predicate table of "
        "the grade. It is empty when the grade has no predicate table.",
    )
    learning_objective = fields.Text(
        string="Learning Objective Achievement",
        help="Description of the learning objectives the student "
        "achieved, written by hand.",
    )

    @api.depends(
        "subject_id",
        "report_card_id.grade_id",
        "subject_id.minimum_score_ids.grade_id",
        "subject_id.minimum_score_ids.minimum_score",
    )
    def _compute_minimum_score(self):
        """Compute the minimum score of the subject on the grade.

        Looks for the minimum score line of the subject that belongs to
        the grade of the report card; 0 when there is none.
        """
        for record in self:
            result = 0.0
            grade = record.report_card_id.grade_id
            for line in record.subject_id.minimum_score_ids:
                if line.grade_id == grade:
                    result = line.minimum_score
            record.minimum_score = result

    @api.depends("final_score", "report_card_id.grade_id")
    def _compute_predicate_line_id(self):
        """Compute the predicate the final score earns.

        Takes the active predicate table of the grade and asks it for
        the line of the final score; empty when no table applies.
        """
        predicate_model = self.env["school_score_predicate"]
        for record in self:
            result = self.env["school_score_predicate_line"]
            table = predicate_model._get_predicate_for_grade(
                record.report_card_id.grade_id
            )
            if table:
                result = table.get_predicate_line(record.final_score)
            record.predicate_line_id = result

    @api.constrains("report_card_id", "subject_id")
    def _check_unique_subject(self):
        """Check that a subject appears once per report card.

        :raises ValidationError: when another line of the same report
            card has the same subject.
        """
        for record in self:
            domain = [
                ("id", "!=", record.id),
                ("report_card_id", "=", record.report_card_id.id),
                ("subject_id", "=", record.subject_id.id),
            ]
            if self.search_count(domain):
                error_message = (
                    _(
                        """
Context: Save report card line
Database ID: %s
Problem: Each subject may only appear once per report card.
Solution: Remove the duplicate line
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    def _get_component_scores(self):
        """Collect the scores of the student for the subject.

        Reads the lines of the score sheets that are done for the same
        enrollment, subject and academic term as this line. Only lines
        that were scored count, so a score of 0 is included and a line
        that was never filled is skipped. Also used by the report card
        print.

        :return: score per component, ``{component_id: score}``.
        :rtype: dict
        """
        self.ensure_one()
        card = self.report_card_id
        # The score sheets are owned by their teachers; the report card
        # reads them for the homeroom teacher, so sudo is needed.
        lines = (
            self.env["school_score_sheet_line"]
            .sudo()
            .search(
                [
                    ("sheet_id.state", "=", "done"),
                    ("sheet_id.subject_id", "=", self.subject_id.id),
                    ("sheet_id.academic_term_id", "=", card.academic_term_id.id),
                    ("enrollment_id", "=", card.enrollment_id.id),
                    ("is_scored", "=", True),
                ]
            )
        )
        return {line.component_id.id: line.score for line in lines}
