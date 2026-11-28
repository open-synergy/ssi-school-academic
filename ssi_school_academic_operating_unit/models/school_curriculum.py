# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

from .school_curriculum_operating_unit_helper import (
    derive_operating_unit_from_school_vals,
    get_operating_unit_id_from_school,
)


class SchoolCurriculum(models.Model):
    # Extension class: adds the single operating unit mixin to
    # school_curriculum and derives its operating unit from the school
    # instead of the default operating unit of the creating user.
    _name = "school_curriculum"
    _inherit = [
        "school_curriculum",
        "mixin.single_operating_unit",
    ]

    @api.model
    def create(self, vals):
        """Derive ``operating_unit_id`` from ``school_id`` on create.

        The derivation runs before ``super()`` so it precedes the
        user default of ``mixin.single_operating_unit``. An explicit
        ``operating_unit_id`` in ``vals`` is kept.

        :param dict vals: values for the new record.
        :return: the created curriculum.
        :rtype: recordset
        """
        derive_operating_unit_from_school_vals(self.env, vals)
        return super().create(vals)

    def write(self, vals):
        """Re-derive ``operating_unit_id`` when ``school_id`` changes.

        A write holding only ``operating_unit_id`` passes unchanged,
        so a user of the multiple operating unit group can still
        change it.

        :param dict vals: values to write.
        :return: True
        :rtype: bool
        """
        derive_operating_unit_from_school_vals(self.env, vals)
        return super().write(vals)

    @api.onchange("school_id")
    def onchange_operating_unit_id(self):
        """Set ``operating_unit_id`` from the selected school.

        Mirrors the ``create``/``write`` derivation so the form shows
        the operating unit before it is saved. Nothing is set when the
        school does not have exactly one operating unit.
        """
        operating_unit_id = get_operating_unit_id_from_school(
            self.env, self.school_id.id
        )
        if operating_unit_id:
            self.operating_unit_id = operating_unit_id
