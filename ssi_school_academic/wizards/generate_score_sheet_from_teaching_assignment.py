# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class GenerateScoreSheetFromTeachingAssignment(models.TransientModel):
    """Creates the score sheets of the main teachers in one go.

    The user picks one or more teaching assignments. For every main
    line of them the wizard creates a draft score sheet for the term,
    grade class and subject of the line, owned by the user of the
    teacher, so only that teacher sees it. A line that already has a
    live score sheet, and a teacher who has no user, are skipped. The
    skipped lines are written to the result note, which the wizard shows
    after it ran.
    """

    _name = "generate_score_sheet_from_teaching_assignment"
    _description = "Generate Score Sheet From Teaching Assignment"

    assignment_ids = fields.Many2many(
        string="Teaching Assignments",
        comodel_name="school_teaching_assignment",
        relation="generate_score_sheet_assignment_rel",
        column1="wizard_id",
        column2="assignment_id",
        help="Teaching assignments whose main lines get a score sheet.",
    )
    result_note = fields.Text(
        string="Result",
        readonly=True,
        help="What the wizard did: the number of score sheets created "
        "and every line that was skipped, with the reason.",
    )

    @api.model
    def default_get(self, fields_list):
        """Prefill the wizard with the assignments it was opened from.

        :param fields_list: field names requested by the client
        :return: dict of default values
        """
        res = super().default_get(fields_list)
        if self.env.context.get("active_model") == "school_teaching_assignment":
            active_ids = self.env.context.get("active_ids")
            if active_ids:
                res["assignment_ids"] = [(6, 0, active_ids)]
        return res

    def action_generate(self):
        """Create the score sheets and show the result again.

        The teaching assignments are checked with the rights of the
        user before the sheets are created as the superuser, so a user
        cannot generate sheets for assignments that user cannot read.

        :return: an ``ir.actions.act_window`` dict reopening the wizard
        """
        self.mapped("assignment_ids").check_access_rights("read")
        self.mapped("assignment_ids").check_access_rule("read")
        for record in self.sudo():
            result = record._generate_score_sheets()
        return result

    def _generate_score_sheets(self):
        """Create a draft score sheet for each main line without one.

        Side effect: writes the outcome on ``result_note``.

        :return: an ``ir.actions.act_window`` dict reopening the wizard
        """
        self.ensure_one()
        sheet_model = self.env["school_score_sheet"]
        created = 0
        notes = []
        for line in self.assignment_ids.mapped("line_ids"):
            if line.role != "main":
                continue
            label = line.display_name
            if sheet_model.search_count(self._get_existing_sheet_criteria(line)):
                notes.append(_("Skipped %s: a score sheet already exists.") % (label,))
                continue
            if not line.teacher_id.employee_id.user_id:
                notes.append(_("Skipped %s: the teacher has no user.") % (label,))
                continue
            sheet_model.create(self._prepare_score_sheet_values(line))
            created += 1
        notes.insert(0, _("Score sheets created: %s") % (created,))
        self.write({"result_note": "\n".join(notes)})
        return {
            "type": "ir.actions.act_window",
            "name": self._description,
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    def _get_existing_sheet_criteria(self, line):
        """Return the domain of the score sheets that block a line.

        Extension point: a score sheet that is not cancelled for the
        same academic term, grade class and subject as the line.

        :param line: the ``school_teaching_assignment_line`` record
        :return: domain for ``school_score_sheet``
        """
        self.ensure_one()
        return [
            ("state", "!=", "cancel"),
            ("academic_term_id", "=", line.academic_term_id.id),
            ("grade_class_id", "=", line.grade_class_id.id),
            ("subject_id", "=", line.subject_id.id),
        ]

    def _prepare_score_sheet_values(self, line):
        """Build the values of the score sheet made for a line.

        Extension point. The sheet is owned by the user of the teacher
        of the line, so the record rule shows it to that teacher only.

        :param line: the ``school_teaching_assignment_line`` record
        :return: dict of ``school_score_sheet`` values
        """
        self.ensure_one()
        return {
            "academic_term_id": line.academic_term_id.id,
            "grade_class_id": line.grade_class_id.id,
            "subject_id": line.subject_id.id,
            "teacher_id": line.teacher_id.id,
            "teaching_assignment_line_id": line.id,
            "user_id": line.teacher_id.employee_id.user_id.id,
        }
