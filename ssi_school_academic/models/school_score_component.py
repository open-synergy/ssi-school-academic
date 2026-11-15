# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolScoreComponent(models.Model):
    """
    Represents one slot of a score component of the report card.
    Each record is a single slot, e.g. "UH 1" or "PTS". A report card
    that uses three daily tests is configured by creating three
    components of the daily test category.
    """

    _name = "school_score_component"
    _inherit = ["mixin.master_data"]
    _description = "School Score Component"
    _order = "sequence, id"

    category = fields.Selection(
        string="Category",
        selection=[
            ("daily_test", "Daily Test"),
            ("assignment", "Assignment"),
            ("mid_term_exam", "Mid-Term Exam"),
            ("final_exam", "Final Exam"),
        ],
        required=True,
        help=(
            "Kind of assessment the component belongs to: "
            "Daily Test = daily test slot, "
            "Assignment = assignment slot, "
            "Mid-Term Exam = mid-term exam, "
            "Final Exam = final exam."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help=(
            "Order of the component. It sets the column order on the "
            "score input and on the printed report card."
        ),
    )
