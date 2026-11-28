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
    by the compute scores action of the report card from the locked
    score columns of the score sheets. A copy of the component scores
    is kept on the line when the scores are computed, so the printed
    report card does not change when a score sheet changes later. A
    line whose subject has no entered score at all is not scored: it
    has no final score and no predicate.
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
    is_scored = fields.Boolean(
        string="Scored",
        readonly=True,
        default=False,
        help="Set by the Compute Scores button of the report card when "
        "the subject has at least one entered score, a typed zero "
        "included. A line that is not scored has no final score and no "
        "predicate.",
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
    score_ids = fields.One2many(
        string="Component Scores",
        comodel_name="school_report_card_line_score",
        inverse_name="line_id",
        readonly=True,
        help="Copy of the score of each component, taken when the "
        "scores of the report card were computed. The print reads it, "
        "so it does not change when a score sheet changes later.",
    )
    learning_objective = fields.Text(
        string="Learning Objective Achievement",
        help="Description of the learning objectives the student "
        "achieved. It is filled from the learning objectives of the "
        "daily tests and assignments that were scored, and it can still "
        "be edited by hand. Computing the scores only fills an empty "
        "text; the Refill Learning Objective button overwrites it.",
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

    @api.depends("final_score", "is_scored", "report_card_id.grade_id")
    def _compute_predicate_line_id(self):
        """Compute the predicate the final score earns.

        Takes the active predicate table of the grade and asks it for
        the line of the final score; empty when no table applies or
        when the line is not scored.
        """
        predicate_model = self.env["school_score_predicate"]
        for record in self:
            result = self.env["school_score_predicate_line"]
            table = predicate_model._get_predicate_for_grade(
                record.report_card_id.grade_id
            )
            if table and record.is_scored:
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

    def _get_scored_line_domain(self):
        """Return the domain of the score sheet lines of this line.

        Only lines that were scored, in a locked column, on the score
        sheets that are not cancelled, for the same enrollment, subject
        and academic term as this line.

        :return: domain for ``school_score_sheet_line``
        :rtype: list
        """
        self.ensure_one()
        card = self.report_card_id
        return [
            ("is_locked", "=", True),
            ("sheet_id.state", "!=", "cancel"),
            ("sheet_id.subject_id", "=", self.subject_id.id),
            ("sheet_id.academic_term_id", "=", card.academic_term_id.id),
            ("enrollment_id", "=", card.enrollment_id.id),
            ("is_scored", "=", True),
        ]

    def _get_component_scores(self):
        """Collect the scores of the student for the subject.

        Reads the lines of the locked columns of the score sheets for
        the same enrollment, subject and academic term as this line.
        Only lines that were scored count, so a score of 0 is included
        and a line that was never filled is skipped. The compute scores
        action of the report card copies the result to ``score_ids``.

        :return: score per component, ``{component_id: score}``.
        :rtype: dict
        """
        self.ensure_one()
        # The score sheets are owned by their teachers; the report card
        # reads them for the homeroom teacher, so sudo is needed.
        lines = (
            self.env["school_score_sheet_line"]
            .sudo()
            .search(self._get_scored_line_domain())
        )
        return {line.component_id.id: line.score for line in lines}

    def _get_printed_component_scores(self):
        """Return the copied scores of the line, for the print.

        Reads ``score_ids``, the copy taken when the scores were
        computed, so a score sheet that changes or is cancelled later
        does not change the print.

        :return: score per component, ``{component_id: score}``.
        :rtype: dict
        """
        self.ensure_one()
        return {score.component_id.id: score.score for score in self.score_ids}

    def _prepare_score_commands(self, component_scores):
        """Build the commands that replace the copied scores.

        :param dict component_scores: ``{component_id: score}``
        :return: x2many commands for ``score_ids``: remove all, then
            one new record per component.
        :rtype: list
        """
        self.ensure_one()
        commands = [(5, 0, 0)]
        for component_id in sorted(component_scores):
            commands.append(
                (
                    0,
                    0,
                    {
                        "component_id": component_id,
                        "score": component_scores[component_id],
                    },
                )
            )
        return commands

    def _get_learning_objective_text(self):
        """Build the learning objective text from the scored cells.

        Takes the learning objectives chosen on the daily test and
        assignment components that the student was scored for, in the
        locked columns of the score sheets. Each objective appears once, in the
        order of the objectives, one description per line. A subject
        without such a cell gives an empty text.

        :return: the descriptions separated by new lines, or an empty
            string.
        :rtype: str
        """
        self.ensure_one()
        sheet_lines = (
            self.env["school_score_sheet_line"]
            .sudo()
            .search(
                self._get_scored_line_domain()
                + [("component_id.category", "in", ["daily_test", "assignment"])]
            )
        )
        cells = {(sl.sheet_id.id, sl.component_id.id) for sl in sheet_lines}
        components = (
            self.env["school_score_sheet_component"]
            .sudo()
            .search([("sheet_id", "in", sheet_lines.mapped("sheet_id").ids)])
        )
        objectives = components.filtered(
            lambda c: (c.sheet_id.id, c.component_id.id) in cells
        ).mapped("objective_ids")
        objectives = objectives.sorted(key=lambda o: (o.sequence, o.id))
        return "\n".join(objectives.mapped("description"))

    def _refill_learning_objective(self, overwrite):
        """Fill the learning objective text of the lines.

        :param bool overwrite: when False a line that already has a text
            is left as it is; when True every line gets the built text,
            an empty one included.
        :return: nothing
        """
        for record in self:
            if record.learning_objective and not overwrite:
                continue
            text = record._get_learning_objective_text()
            if text != (record.learning_objective or ""):
                record.write({"learning_objective": text or False})
