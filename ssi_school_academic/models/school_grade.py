# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolGrade(models.Model):
    # Extension of the grade: adds the curriculum phase printed on the
    # report card (for example "E" for the first year of vocational school).
    _inherit = "school_grade"

    phase = fields.Char(
        string="Phase",
        help="Curriculum phase of the grade, for example E or F. It is "
        "printed in the header of the report card. Leave empty when not "
        "applicable.",
    )
