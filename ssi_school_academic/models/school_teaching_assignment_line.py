# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolTeachingAssignmentLine(models.Model):
    """Represents one homeroom and subject a teacher teaches.

    A line of a teaching assignment names the homeroom, the subject,
    the role of the teacher (main or assistant) and the weekly hours.
    The score sheets generated from a main line are linked back to it.
    Only one main teacher may exist for the same homeroom, subject and
    academic term, and a teacher may teach a subject of a homeroom only
    once.
    """

    _name = "school_teaching_assignment_line"
    _description = "School Teaching Assignment Line"
    _order = "assignment_id, grade_class_id, subject_id, id"

    assignment_id = fields.Many2one(
        string="Teaching Assignment",
        comodel_name="school_teaching_assignment",
        required=True,
        ondelete="cascade",
        help="Teaching assignment this line belongs to.",
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        related="assignment_id.teacher_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Teacher of the selected Teaching Assignment.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        related="assignment_id.academic_term_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Academic term of the selected Teaching Assignment.",
    )
    homeroom_id = fields.Many2one(
        string="Class Group",
        comodel_name="school_homeroom",
        required=True,
        ondelete="restrict",
        domain="[('state', '!=', 'cancel')]",
        help="Homeroom the teacher teaches. Only homerooms that are "
        "not cancelled can be chosen; the form narrows them further to "
        "the academic term of the assignment.",
    )
    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        related="homeroom_id.grade_class_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Grade class of the selected Homeroom.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        related="homeroom_id.grade_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Grade of the selected Homeroom. It decides which "
        "subjects can be chosen.",
    )
    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        required=True,
        ondelete="restrict",
        domain="[('grade_ids', '=', grade_id)]",
        help="Subject the teacher teaches. Only subjects taught in the "
        "Grade of the Homeroom can be chosen.",
    )
    role = fields.Selection(
        string="Role",
        selection=[
            ("main", "Main"),
            ("assistant", "Assistant"),
        ],
        required=True,
        default="main",
        help="Role of the teacher in this subject. The main teacher "
        "gives the scores and owns the score sheet; an assistant "
        "teacher may only read it.",
    )
    weekly_hours = fields.Integer(
        string="Weekly Hours",
        help="Number of lesson hours (JP) the teacher teaches the "
        "subject in this homeroom per week.",
    )
    score_sheet_ids = fields.One2many(
        string="Score Sheets",
        comodel_name="school_score_sheet",
        inverse_name="teaching_assignment_line_id",
        help="Score sheets that were created from this line.",
    )

    def name_get(self):
        """Return the display name of the lines as the superuser.

        The name joins the teacher, the grade class and the subject.
        It is read as the superuser, so a user who may open a record
        that points at a line never gets an access error for the name,
        even when a record rule hides the line itself.

        :return: list of ``(id, name)`` tuples
        """
        result = []
        for record in self.sudo():
            name = "%s / %s / %s" % (
                record.teacher_id.name or "",
                record.grade_class_id.name or "",
                record.subject_id.name or "",
            )
            result.append((record.id, name))
        return result

    def _sync_draft_score_sheet(self):
        """Hand the draft score sheet of the main lines to their teacher.

        Only a line whose role is main is handled; an assistant line
        never writes. The draft score sheet that has the same academic
        term, grade class and subject as the line is given the teacher
        of the assignment and is linked to the line. The sheets are
        found and written as the superuser, because a user of the
        teaching assignment may not write them. A sheet that is not
        draft is never touched.
        """
        sheet_model = self.env["school_score_sheet"].sudo()
        for record in self.filtered(lambda r: r.role == "main"):
            teacher = record.assignment_id.teacher_id
            sheets = sheet_model.search(
                [
                    ("state", "=", "draft"),
                    ("academic_term_id", "=", record.academic_term_id.id),
                    ("grade_class_id", "=", record.grade_class_id.id),
                    ("subject_id", "=", record.subject_id.id),
                ]
            )
            sheets = sheets.filtered(
                lambda s, t=teacher, r=record: s.teacher_id != t
                or s.teaching_assignment_line_id != r
            )
            if sheets:
                sheets.write(
                    {
                        "teacher_id": teacher.id,
                        "teaching_assignment_line_id": record.id,
                    }
                )

    @api.model_create_multi
    def create(self, vals_list):
        """Create the lines and sync the draft score sheet of main lines.

        The sync runs after the constraints, so a line that is refused
        never moves a score sheet.

        :param list vals_list: values of the lines to create.
        :return: the created lines
        :rtype: recordset
        """
        records = super().create(vals_list)
        records._sync_draft_score_sheet()
        return records

    def write(self, vals):
        """Write the lines and sync the draft score sheet on a new main role.

        The sync runs only when the role is written, and only for the
        lines that are main after the write.

        :param dict vals: values to write.
        :return: True
        :rtype: bool
        """
        result = super().write(vals)
        if vals.get("role") == "main":
            self._sync_draft_score_sheet()
        return result

    def _has_active_score_sheet(self):
        """Tell whether a score sheet that is not cancelled uses the line.

        A score sheet uses the line when it has the same academic term,
        grade class and subject, whatever its teacher and whatever the
        role of the line. The sheets are searched as the superuser,
        because a user of the teaching assignment may not read them.

        :return: True when such a score sheet exists
        :rtype: bool
        """
        self.ensure_one()
        domain = [
            ("state", "!=", "cancel"),
            ("academic_term_id", "=", self.academic_term_id.id),
            ("grade_class_id", "=", self.grade_class_id.id),
            ("subject_id", "=", self.subject_id.id),
        ]
        return bool(self.env["school_score_sheet"].sudo().search_count(domain))

    def _check_no_active_score_sheet(self, context):
        """Refuse to delete when a score sheet that is not cancelled exists.

        :param str context: name of the deleted record, shown in the
            ``Context`` line of the error message.
        :raises UserError: when a line has a score sheet that is not
            cancelled for the same term, grade class and subject.
        """
        for record in self:
            if record._has_active_score_sheet():
                error_message = (
                    _(
                        """
Context: Delete %s
Database ID: %s
Problem: A score sheet that is not cancelled exists for this term, class and subject.
Solution: Cancel or delete the score sheet first
"""
                    )
                    % (context, record.id)
                )
                raise UserError(error_message)

    def unlink(self):
        """Delete the lines and release the cancelled score sheets.

        A line is refused when a score sheet that is not cancelled
        exists for its academic term, grade class and subject. The
        cancelled score sheets that point at the lines lose that link,
        so the deletion is not blocked by the foreign key.

        :return: True
        :rtype: bool
        :raises UserError: when a line has a score sheet that is not
            cancelled.
        """
        self._check_no_active_score_sheet(_("teaching assignment line"))
        sheets = (
            self.env["school_score_sheet"]
            .sudo()
            .search([("teaching_assignment_line_id", "in", self.ids)])
        )
        sheets.write({"teaching_assignment_line_id": False})
        return super().unlink()

    @api.constrains("role", "homeroom_id", "subject_id", "academic_term_id")
    def _check_unique_main_teacher(self):
        """Check that a subject of a homeroom has one main teacher.

        The lines of every assignment are compared, so two different
        teachers cannot both be the main teacher of the same homeroom,
        subject and academic term.

        :raises ValidationError: when another main line exists for the
            same homeroom, subject and academic term.
        """
        for record in self:
            if record.role != "main":
                continue
            domain = [
                ("id", "!=", record.id),
                ("role", "=", "main"),
                ("homeroom_id", "=", record.homeroom_id.id),
                ("subject_id", "=", record.subject_id.id),
                ("academic_term_id", "=", record.academic_term_id.id),
            ]
            if self.sudo().search_count(domain):
                error_message = (
                    _(
                        """
Context: Save teaching assignment line
Database ID: %s
Problem: This subject of the homeroom already has a main teacher in this term.
Solution: Set the role to assistant, or change the line of the other teacher
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("teacher_id", "homeroom_id", "subject_id")
    def _check_unique_teacher_subject(self):
        """Check that a teacher teaches a subject of a homeroom once.

        :raises ValidationError: when the same teacher has another line
            for the same homeroom and subject.
        """
        for record in self:
            domain = [
                ("id", "!=", record.id),
                ("teacher_id", "=", record.teacher_id.id),
                ("homeroom_id", "=", record.homeroom_id.id),
                ("subject_id", "=", record.subject_id.id),
            ]
            if self.sudo().search_count(domain):
                error_message = (
                    _(
                        """
Context: Save teaching assignment line
Database ID: %s
Problem: This teacher already teaches this subject in this homeroom.
Solution: Edit the existing line instead of adding a new one
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("subject_id", "grade_id")
    def _check_subject_grade(self):
        """Check that the subject is taught in the grade of the homeroom.

        :raises ValidationError: when the grades of the subject do not
            include the grade of the homeroom.
        """
        for record in self:
            if record.grade_id not in record.subject_id.grade_ids:
                error_message = (
                    _(
                        """
Context: Save teaching assignment line
Database ID: %s
Problem: The subject is not taught in the grade of the homeroom.
Solution: Choose a subject that is taught in the grade of the homeroom
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
