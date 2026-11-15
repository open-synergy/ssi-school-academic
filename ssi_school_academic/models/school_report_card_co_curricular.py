# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolReportCardCoCurricular(models.Model):
    """Represents one co-curricular theme printed on a report card.

    A line holds a theme and its description, both written by hand by
    the homeroom teacher.
    """

    _name = "school_report_card_co_curricular"
    _description = "School Report Card Co-Curricular"
    _order = "report_card_id, id"

    report_card_id = fields.Many2one(
        string="# Report Card",
        comodel_name="school_report_card",
        required=True,
        ondelete="cascade",
        help="Report card this co-curricular line belongs to.",
    )
    theme = fields.Char(
        string="Theme",
        required=True,
        help="Theme of the co-curricular activity.",
    )
    description = fields.Text(
        string="Description",
        help="Description of what the student did in the theme.",
    )
