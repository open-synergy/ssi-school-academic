# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolReportCardTypeWeight(models.Model):
    """
    Detail line of ``school_report_card_type``.
    One line stores the weight of one score component that is not part
    of the average, e.g. the mid-term exam in a mid-term report card.
    """

    _name = "school_report_card_type_weight"
    _description = "School Report Card Type Weight"
    _order = "type_id, id"

    type_id = fields.Many2one(
        string="# Report Card Type",
        comodel_name="school_report_card_type",
        required=True,
        ondelete="cascade",
        help="Report card type this weight belongs to.",
    )
    component_id = fields.Many2one(
        string="Component",
        comodel_name="school_score_component",
        required=True,
        ondelete="restrict",
        help="Score component this weight applies to.",
    )
    weight = fields.Float(
        string="Weight (%)",
        required=True,
        help="Weight, in percent, of the component in the final score.",
    )
