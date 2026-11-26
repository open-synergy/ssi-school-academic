# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolTeachingAssignment(models.Model):  # pylint: disable=too-few-public-methods
    # Extension class: adds the multiple operating unit mixin to
    # school_teaching_assignment, a master data. The lines of the
    # assignment have no operating unit; they follow the header.
    _name = "school_teaching_assignment"
    _inherit = [
        "school_teaching_assignment",
        "mixin.multiple_operating_unit",
    ]
