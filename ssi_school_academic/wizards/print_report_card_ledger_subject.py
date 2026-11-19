# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PrintReportCardLedgerSubject(models.TransientModel):
    """Represents one subject column of the report card ledger.

    A column exists for every subject found on the non-cancelled report
    cards of the selected type that belong to the students of the
    ledger. It holds the average of the scored cells of that column.
    """

    _name = "print_report_card_ledger_subject"
    _description = "Print Report Card Ledger Subject"
    _order = "wizard_id, sequence, id"

    wizard_id = fields.Many2one(
        string="# Ledger",
        comodel_name="print_report_card_ledger",
        required=True,
        ondelete="cascade",
        help="Ledger this column belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=1,
        help="Position of the column on the ledger.",
    )
    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        required=True,
        ondelete="cascade",
        help="Subject shown in this column.",
    )
    has_average = fields.Boolean(
        string="Has Average",
        help="Checked when at least one cell of this column is scored.",
    )
    average = fields.Float(
        string="Average",
        help="Average of the scored cells of this column. It is shown as "
        "a dash when no cell of the column is scored.",
    )
