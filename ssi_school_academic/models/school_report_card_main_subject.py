# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolReportCardMainSubject(models.Model):
    """
    Represents the list of main subjects of a grade, optionally of one
    expertise program of that grade. The main subjects are used to break
    a tie in the rank of the students on the score ledger. A record
    without an expertise program is the fallback of the grade: it applies
    to every class of the grade that has no record of its own program.
    """

    _name = "school_report_card_main_subject"
    _inherit = ["mixin.master_data"]
    _description = "Report Card Main Subject"
    _order = "grade_id, expertise_program, id"

    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        ondelete="restrict",
        help="Grade the main subjects apply to.",
    )
    expertise_program = fields.Char(
        string="Expertise Program",
        help=(
            "Expertise program the main subjects apply to, written "
            "exactly as on the grade class. Leave empty to set the "
            "main subjects of the whole grade, used by the classes "
            "whose program has no record of its own."
        ),
    )
    subject_ids = fields.Many2many(
        string="Main Subjects",
        comodel_name="school_subject",
        required=True,
        help=(
            "Subjects that break a tie in the rank of the students. "
            "At least one subject is required."
        ),
    )

    @api.constrains("grade_id", "expertise_program", "active")
    def _check_unique_active_grade_program(self):
        """Reject two active records of the same grade and program.

        An empty program (``False`` or an empty string) counts as one
        single value, so a grade can have only one active fallback
        record. Inactive records are never compared.

        :raises ValidationError: when another active record has the same
            grade and the same expertise program.
        """
        for record in self.filtered(lambda r: r.active):
            others = self.sudo().search(
                [
                    ("id", "!=", record.id),
                    ("grade_id", "=", record.grade_id.id),
                    ("active", "=", True),
                ]
            )
            program = record.expertise_program or ""
            if others.filtered(lambda r: (r.expertise_program or "") == program):
                raise ValidationError(
                    _(
                        "Only one active main subject record is allowed "
                        "for the same grade and expertise program."
                    )
                )

    @api.constrains("subject_ids", "grade_id")
    def _check_subject_ids(self):
        """Reject a record without any main subject.

        :raises ValidationError: when ``subject_ids`` is empty.
        """
        for record in self:
            if not record.subject_ids:
                raise ValidationError(_("At least one main subject is required."))

    @api.model
    def _get_main_subjects(self, grade_class):
        """Return the main subjects that apply to a grade class.

        Looks for the active record of the grade of the class whose
        expertise program is exactly the program of the class. When
        there is none, falls back to the active record of the same grade
        with an empty program. When there is none either, the result is
        empty.

        :param grade_class: ``school_grade_class`` record.
        :return: the main ``school_subject`` records, empty when
            nothing is configured.
        :rtype: recordset of ``school_subject``
        """
        records = self.sudo().search(
            [
                ("grade_id", "=", grade_class.grade_id.id),
                ("active", "=", True),
            ]
        )
        by_program = {(r.expertise_program or ""): r for r in records}
        program = grade_class.expertise_program or ""
        for key in (program, ""):
            if key in by_program:
                return by_program[key].subject_ids.with_env(self.env)
        return self.env["school_subject"]
