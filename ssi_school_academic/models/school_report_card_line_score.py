# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolReportCardLineScore(models.Model):
    """Represents the copied score of one component of a report line.

    When the scores of a report card are computed, the score of the
    student for each score component is copied here. The print reads
    this copy instead of the score sheets, so a printed report card
    does not change when a score sheet is unlocked, changed or
    cancelled later.
    """

    _name = "school_report_card_line_score"
    _description = "School Report Card Line Score"
    _order = "line_id, component_id"

    line_id = fields.Many2one(
        string="Report Card Line",
        comodel_name="school_report_card_line",
        required=True,
        ondelete="cascade",
        help="Report card line the copied score belongs to.",
    )
    component_id = fields.Many2one(
        string="Score Component",
        comodel_name="school_score_component",
        required=True,
        ondelete="restrict",
        help="Score component the copied score is given for.",
    )
    score = fields.Float(
        string="Score",
        help="Score of the student for the component, as it was when "
        "the scores of the report card were computed.",
    )
