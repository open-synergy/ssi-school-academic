# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PrintReportCardLedgerLine(models.TransientModel):
    """Represents one student row of the report card ledger.

    A row exists for every enrollment of the selected class and term
    that is on progress or done. It holds the total, the average and
    the rank of the student over the scored cells of the row.
    """

    _name = "print_report_card_ledger_line"
    _description = "Print Report Card Ledger Line"
    _order = "wizard_id, sequence, id"

    wizard_id = fields.Many2one(
        string="# Ledger",
        comodel_name="print_report_card_ledger",
        required=True,
        ondelete="cascade",
        help="Ledger this row belongs to.",
    )
    sequence = fields.Integer(
        string="No",
        default=1,
        help="Number of the row on the ledger.",
    )
    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        required=True,
        ondelete="cascade",
        help="Enrollment of the student on the class and term.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        related="enrollment_id.student_id",
        readonly=True,
        help="Student of the enrollment.",
    )
    student_code = fields.Char(
        string="Student ID",
        related="enrollment_id.student_id.code",
        readonly=True,
        help="Student identification number (NIS) of the student.",
    )
    cell_ids = fields.One2many(
        string="Cells",
        comodel_name="print_report_card_ledger_cell",
        inverse_name="line_id",
        help="Score cells of this row, one for every subject column.",
    )
    has_score = fields.Boolean(
        string="Has Score",
        help="Checked when at least one cell of the row is scored. A row "
        "without score has no total, average and rank.",
    )
    total = fields.Float(
        string="Total",
        help="Sum of the scored cells of the row.",
    )
    average = fields.Float(
        string="Average",
        help="Average of the scored cells of the row.",
    )
    rank = fields.Integer(
        string="Rank",
        help="Rank of the student among the rows that have a score. Zero "
        "means no rank and is shown as a dash.",
    )
