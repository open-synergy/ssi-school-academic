# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CopyTeachingAssignmentFromPreviousTerm(models.TransientModel):
    """Copies the teaching assignments of one term to another term.

    The user picks a source term, a target term and the assignments to
    copy. For every assignment the wizard creates the assignment of the
    same teacher in the target term, unless the teacher already has one.
    Every line is moved to the homeroom of the target term that has the
    same grade class; the role, the subject and the weekly hours are
    copied. A line is skipped when the target term has no such homeroom
    or more than one, or when it would give a subject of a homeroom a
    second main teacher. The skipped items are written to the result
    note.
    """

    _name = "copy_teaching_assignment_from_previous_term"
    _description = "Copy Teaching Assignment From Previous Term"

    source_term_id = fields.Many2one(
        string="Source Term",
        comodel_name="school_academic_term",
        required=True,
        ondelete="cascade",
        help="Academic term whose teaching assignments are copied.",
    )
    target_term_id = fields.Many2one(
        string="Target Term",
        comodel_name="school_academic_term",
        required=True,
        ondelete="cascade",
        help="Academic term the teaching assignments are copied to. It "
        "must differ from the source term.",
    )
    assignment_ids = fields.Many2many(
        string="Teaching Assignments",
        comodel_name="school_teaching_assignment",
        relation="copy_teaching_assignment_rel",
        column1="wizard_id",
        column2="assignment_id",
        help="Teaching assignments to copy. All the assignments of the "
        "source term are offered when the source term is chosen.",
    )
    result_note = fields.Text(
        string="Result",
        readonly=True,
        help="What the wizard did: the number of assignments and lines "
        "copied and everything that was skipped, with the reason.",
    )

    @api.constrains("source_term_id", "target_term_id")
    def _check_different_terms(self):
        """Check that the target term is not the source term.

        :raises ValidationError: when both terms are the same.
        """
        for record in self:
            if record.source_term_id == record.target_term_id:
                error_message = (
                    _(
                        """
Context: Copy teaching assignment
Database ID: %s
Problem: The target term is the same as the source term.
Solution: Choose a target term that differs from the source term
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.onchange("source_term_id")
    def onchange_assignment_ids(self):
        """Offer every assignment of the source term.

        The choice is replaced each time the source term changes, so
        the assignments of a previous source term never stay.
        """
        self.assignment_ids = False
        if self.source_term_id:
            self.assignment_ids = self.env["school_teaching_assignment"].search(
                [("academic_term_id", "=", self.source_term_id.id)]
            )

    def action_copy(self):
        """Copy the assignments and show the result again.

        :return: an ``ir.actions.act_window`` dict reopening the wizard
        """
        for record in self.sudo():
            result = record._copy_assignments()
        return result

    def _copy_assignments(self):
        """Create the assignments and lines of the target term.

        Side effect: writes the outcome on ``result_note``.

        :return: an ``ir.actions.act_window`` dict reopening the wizard
        """
        self.ensure_one()
        header_model = self.env["school_teaching_assignment"]
        line_model = self.env["school_teaching_assignment_line"]
        count_header = 0
        count_line = 0
        notes = []
        for source in self.assignment_ids:
            if header_model.search_count(
                [
                    ("teacher_id", "=", source.teacher_id.id),
                    ("academic_term_id", "=", self.target_term_id.id),
                ]
            ):
                notes.append(
                    _("Skipped %s: the teacher already has an assignment.")
                    % (source.display_name,)
                )
                continue
            target = header_model.create(
                self._prepare_assignment_values(source, self.target_term_id)
            )
            count_header += 1
            for line in source.line_ids:
                homerooms = self.env["school_homeroom"].search(
                    self._get_target_homeroom_criteria(line)
                )
                label = line.display_name
                if len(homerooms) != 1:
                    notes.append(
                        _("Skipped %s: the target term has %s matching homerooms.")
                        % (label, len(homerooms))
                    )
                    continue
                if line.role == "main" and line_model.search_count(
                    [
                        ("role", "=", "main"),
                        ("homeroom_id", "=", homerooms.id),
                        ("subject_id", "=", line.subject_id.id),
                        ("academic_term_id", "=", self.target_term_id.id),
                    ]
                ):
                    notes.append(
                        _("Skipped %s: the subject already has a main teacher.")
                        % (label,)
                    )
                    continue
                line_model.create(
                    self._prepare_assignment_line_values(line, target, homerooms)
                )
                count_line += 1
        notes.insert(
            0,
            _("Assignments copied: %s, lines copied: %s") % (count_header, count_line),
        )
        self.write({"result_note": "\n".join(notes)})
        return {
            "type": "ir.actions.act_window",
            "name": self._description,
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    def _get_target_homeroom_criteria(self, line):
        """Return the domain of the homerooms a line can move to.

        Extension point: homerooms of the target term that have the
        same grade class as the line and are not cancelled.

        :param line: the source ``school_teaching_assignment_line``
        :return: domain for ``school_homeroom``
        """
        self.ensure_one()
        return [
            ("academic_term_id", "=", self.target_term_id.id),
            ("grade_class_id", "=", line.grade_class_id.id),
            ("state", "!=", "cancel"),
        ]

    def _prepare_assignment_values(self, source, target_term):
        """Build the values of the assignment created in the target term.

        Extension point. The name is the teacher and the target term,
        and the code is ``/`` so no unique code is required.

        :param source: the source ``school_teaching_assignment``
        :param target_term: the target ``school_academic_term``
        :return: dict of ``school_teaching_assignment`` values
        """
        self.ensure_one()
        return {
            "name": "%s - %s" % (source.teacher_id.name, target_term.display_name),
            "code": "/",
            "company_id": source.company_id.id,
            "teacher_id": source.teacher_id.id,
            "academic_term_id": target_term.id,
        }

    def _prepare_assignment_line_values(self, line, target, homeroom):
        """Build the values of a line created in the target assignment.

        Extension point. The role, the subject and the weekly hours are
        copied from the source line.

        :param line: the source ``school_teaching_assignment_line``
        :param target: the new ``school_teaching_assignment``
        :param homeroom: the ``school_homeroom`` of the target term
        :return: dict of ``school_teaching_assignment_line`` values
        """
        self.ensure_one()
        return {
            "assignment_id": target.id,
            "homeroom_id": homeroom.id,
            "subject_id": line.subject_id.id,
            "role": line.role,
            "weekly_hours": line.weekly_hours,
        }
