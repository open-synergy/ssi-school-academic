# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolTeacher(models.Model):
    # Lists the teaching assignments of the teacher. There is no view
    # for it, the field only exposes the relation to other models.
    _inherit = "school_teacher"

    teaching_assignment_ids = fields.One2many(
        string="Teaching Assignments",
        comodel_name="school_teaching_assignment",
        inverse_name="teacher_id",
        help="Teaching assignments of this teacher, one per academic " "term.",
    )
