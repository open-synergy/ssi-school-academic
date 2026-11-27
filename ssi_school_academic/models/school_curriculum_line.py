# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolCurriculumLine(models.Model):
    """Represents one subject of a grade in a school curriculum.

    A line states how many weekly hours (JP) a subject takes in one
    grade and in how many classes the school runs it. The total time is
    the weekly hours of one class times the number of classes. A
    subject can only be listed for a grade it is applicable to, and
    only once per grade in the same curriculum. The lines can only be
    changed while the curriculum is in draft.
    """

    _name = "school_curriculum_line"
    _description = "School Curriculum Line"
    _order = "curriculum_id, grade_id, subject_id, id"

    curriculum_id = fields.Many2one(
        string="Curriculum",
        comodel_name="school_curriculum",
        required=True,
        ondelete="cascade",
        help="Curriculum this line belongs to.",
    )
    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        required=True,
        ondelete="restrict",
        help="Subject taught. It must be applicable to the grade.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        required=True,
        ondelete="restrict",
        help="Grade the subject is taught in. It must be one of the "
        "applicable grades of the subject.",
    )
    category = fields.Selection(
        string="Category",
        related="subject_id.subject_group",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Subject group of the selected Subject.",
    )
    weekly_hours = fields.Integer(
        string="Weekly Hours",
        required=True,
        default=1,
        help="Weekly hours (JP) of the subject for one class. It must "
        "be at least 1.",
    )
    total_class = fields.Integer(
        string="Total Class",
        required=True,
        default=1,
        help="Number of classes of the grade that take the subject. It "
        "must be at least 1.",
    )
    total_time = fields.Integer(
        string="Total Time",
        compute="_compute_total_time",
        compute_sudo=True,
        store=True,
        help="Total weekly hours of all classes: weekly hours times " "total class.",
    )

    @api.depends("weekly_hours", "total_class")
    def _compute_total_time(self):
        """Multiply the weekly hours by the number of classes."""
        for record in self:
            record.total_time = record.weekly_hours * record.total_class

    @api.model_create_multi
    def create(self, vals_list):
        """Create lines and refuse them on a curriculum not in draft.

        :param list vals_list: values of the lines to create.
        :return: the new lines.
        :rtype: recordset of ``school_curriculum_line``
        :raises ValidationError: when a line is added to a curriculum
            that is not draft.
        """
        curriculum_ids = [
            vals["curriculum_id"] for vals in vals_list if vals.get("curriculum_id")
        ]
        curriculums = self.env["school_curriculum"].browse(curriculum_ids)
        for curriculum in curriculums.filtered(lambda r: r.state != "draft"):
            curriculum._raise_not_draft()
        return super().create(vals_list)

    def write(self, vals):
        """Write lines and refuse changes on a curriculum not in draft.

        :param dict vals: values to write.
        :return: True
        :rtype: bool
        :raises ValidationError: when an editable field is written on
            a line of a curriculum that is not draft.
        """
        editable = ["curriculum_id", "subject_id", "grade_id"]
        editable += ["weekly_hours", "total_class"]
        if any(field in vals for field in editable):
            for record in self.filtered(lambda r: r.curriculum_id.state != "draft"):
                record.curriculum_id._raise_not_draft()
        return super().write(vals)

    def unlink(self):
        """Delete lines and refuse it on a curriculum not in draft.

        :return: True
        :rtype: bool
        :raises ValidationError: when a line of a curriculum that is
            not draft is deleted.
        """
        for record in self.filtered(lambda r: r.curriculum_id.state != "draft"):
            record.curriculum_id._raise_not_draft()
        return super().unlink()

    @api.constrains("weekly_hours", "total_class")
    def _check_positive(self):
        """Check that the weekly hours and the classes are positive.

        :raises ValidationError: when the weekly hours or the total
            class is less than 1.
        """
        for record in self:
            if record.weekly_hours < 1 or record.total_class < 1:
                error_message = (
                    _(
                        """
Document: School Curriculum Line
Context: Save curriculum line
Database ID: %s
Problem: Weekly hours and total class must be at least 1.
Solution: Enter a value of 1 or more
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("subject_id", "grade_id")
    def _check_grade_of_subject(self):
        """Check that the subject is applicable to the grade.

        :raises ValidationError: when the grade is not one of the
            applicable grades of the subject.
        """
        for record in self:
            if record.grade_id not in record.subject_id.grade_ids:
                error_message = (
                    _(
                        """
Document: School Curriculum Line
Context: Save curriculum line
Database ID: %s
Problem: The subject is not applicable to the grade.
Solution: Choose a grade the subject is applicable to
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("curriculum_id", "subject_id", "grade_id")
    def _check_unique_subject_grade(self):
        """Check that a subject is listed once per grade.

        :raises ValidationError: when another line of the same
            curriculum has the same subject and grade.
        """
        for record in self:
            domain = [
                ("id", "!=", record.id),
                ("curriculum_id", "=", record.curriculum_id.id),
                ("subject_id", "=", record.subject_id.id),
                ("grade_id", "=", record.grade_id.id),
            ]
            if self.search_count(domain):
                error_message = (
                    _(
                        """
Document: School Curriculum Line
Context: Save curriculum line
Database ID: %s
Problem: The subject is already listed for this grade.
Solution: Remove the duplicate line
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
