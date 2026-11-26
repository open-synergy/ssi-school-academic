# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class GenerateScoreSheetFromTeachingAssignment(models.TransientModel):
    # Extension class: the score sheet made by the wizard carries the
    # operating unit of the teaching assignment.
    _name = "generate_score_sheet_from_teaching_assignment"
    _inherit = ["generate_score_sheet_from_teaching_assignment"]

    def _prepare_score_sheet_values(self, line):
        """Add the operating unit of the assignment to the sheet values.

        The wizard creates the sheet as the superuser, so the sheet
        would otherwise get the default operating unit of the user who
        runs the wizard. When the assignment of the line has exactly one
        operating unit the sheet gets that unit. When it has none, or
        more than one, the operating unit is not set and the sheet keeps
        the default of the user: the first unit is never picked.

        :param line: the ``school_teaching_assignment_line`` record
        :return: dict of ``school_score_sheet`` values
        """
        result = super()._prepare_score_sheet_values(line)
        units = line.assignment_id.operating_unit_ids
        if len(units) == 1:
            result["operating_unit_id"] = units.id
        return result
