# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class CopyTeachingAssignmentFromPreviousTerm(models.TransientModel):
    # Extension class: the assignment made in the target term keeps the
    # operating units of the source assignment.
    _name = "copy_teaching_assignment_from_previous_term"
    _inherit = ["copy_teaching_assignment_from_previous_term"]

    def _prepare_assignment_values(self, source, target_term):
        """Add the operating units of the source to the new assignment.

        :param source: the source ``school_teaching_assignment``
        :param target_term: the target ``school_academic_term``
        :return: dict of ``school_teaching_assignment`` values
        """
        result = super()._prepare_assignment_values(source, target_term)
        result["operating_unit_ids"] = [(6, 0, source.operating_unit_ids.ids)]
        return result
