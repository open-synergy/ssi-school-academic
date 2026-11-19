# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PrintReportCardLedgerCell(models.TransientModel):
    """Represents one score cell of the report card ledger.

    A cell sits where the row of one student meets the column of one
    subject. It is scored only when the report card of the student is
    done and its line for the subject is scored.
    """

    _name = "print_report_card_ledger_cell"
    _description = "Print Report Card Ledger Cell"
    _order = "line_id, sequence, id"

    line_id = fields.Many2one(
        string="# Row",
        comodel_name="print_report_card_ledger_line",
        required=True,
        ondelete="cascade",
        help="Row of the ledger this cell belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=1,
        help="Position of the cell in its row, the same as its column.",
    )
    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        required=True,
        ondelete="cascade",
        help="Subject of the column this cell belongs to.",
    )
    has_score = fields.Boolean(
        string="Has Score",
        help="Checked when the cell holds a score. A cell without score "
        "is shown as a dash and is not counted.",
    )
    score = fields.Float(
        string="Score",
        help="Final score of the subject on the done report card.",
    )
    is_below_minimum = fields.Boolean(
        string="Below Minimum",
        help="Checked when the score is lower than the minimum score "
        "(KKM) of the subject. A subject without minimum score is never "
        "below minimum.",
    )
