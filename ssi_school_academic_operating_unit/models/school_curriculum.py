# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolCurriculum(models.Model):  # pylint: disable=too-few-public-methods
    # Extension class: adds the single operating unit mixin to
    # school_curriculum. The behaviour of the document itself is unchanged.
    _name = "school_curriculum"
    _inherit = [
        "school_curriculum",
        "mixin.single_operating_unit",
    ]
