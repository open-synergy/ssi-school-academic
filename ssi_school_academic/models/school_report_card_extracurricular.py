# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolReportCardExtracurricular(models.Model):
    """Represents one extracurricular activity printed on a report card.

    A line holds the name of the activity and a short description, both
    written by hand by the homeroom teacher.
    """

    _name = "school_report_card_extracurricular"
    _description = "School Report Card Extracurricular"
    _order = "report_card_id, id"

    report_card_id = fields.Many2one(
        string="# Report Card",
        comodel_name="school_report_card",
        required=True,
        ondelete="cascade",
        help="Report card this extracurricular line belongs to.",
    )
    name = fields.Char(
        string="Activity",
        required=True,
        help="Name of the extracurricular activity.",
    )
    description = fields.Char(
        string="Description",
        help="Short description of the student's result in the activity.",
    )
