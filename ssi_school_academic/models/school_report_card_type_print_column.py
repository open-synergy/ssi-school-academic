# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

MAX_PRINT_COLUMNS = 4


class SchoolReportCardTypePrintColumn(models.Model):
    """
    Detail line of ``school_report_card_type``.
    One line is one score component column printed on the mid-term report
    card, with its own print title and its position among the columns.
    """

    _name = "school_report_card_type_print_column"
    _description = "School Report Card Type Print Column"
    _order = "type_id, sequence, id"

    type_id = fields.Many2one(
        string="# Report Card Type",
        comodel_name="school_report_card_type",
        required=True,
        ondelete="cascade",
        help="Report card type this printed column belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Position of the column on the printed report card.",
    )
    component_id = fields.Many2one(
        string="Component",
        comodel_name="school_score_component",
        required=True,
        ondelete="restrict",
        help="Score component whose score is printed in this column.",
    )
    print_title = fields.Char(
        string="Print Title",
        help=(
            "Title of the column on the printed report card. "
            "Leave empty to print the name of the component."
        ),
    )

    @api.constrains("type_id")
    def _check_max_columns(self):
        """Reject a report card type with more than four printed columns.

        :raises ValidationError: when a type has more lines than
            ``MAX_PRINT_COLUMNS``.
        """
        for card_type in self.sudo().mapped("type_id"):
            if len(card_type.print_column_ids) > MAX_PRINT_COLUMNS:
                error_message = (
                    _(
                        """
Context: Validate report card type
Database ID: %s
Problem: A report card type can print at most %s columns.
Solution: Remove the extra printed columns
"""
                    )
                    % (card_type.id, MAX_PRINT_COLUMNS)
                )
                raise ValidationError(error_message)

    @api.constrains("type_id", "component_id")
    def _check_unique_component(self):
        """Reject a component printed twice in the same report card type.

        :raises ValidationError: when two lines of one type share the
            same component.
        """
        for record in self.sudo():
            duplicates = record.type_id.print_column_ids.filtered(
                lambda line, rec=record: line.component_id == rec.component_id
            )
            if len(duplicates) > 1:
                error_message = (
                    _(
                        """
Context: Validate report card type
Database ID: %s
Problem: The component %s is printed more than once.
Solution: Keep only one printed column for each component
"""
                    )
                    % (record.type_id.id, record.component_id.display_name)
                )
                raise ValidationError(error_message)
