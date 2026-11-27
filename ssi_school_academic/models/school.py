# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class School(models.Model):
    # Extension of the school: adds the weekly teaching hours a teacher is
    # required to carry and the factor applied to co-teaching hours. Both
    # values are read by the manpower planning workload recap.
    _inherit = "school"

    teacher_mandatory_weekly_hours = fields.Integer(
        string="Teacher Mandatory Weekly Hours",
        default=0,
        help="Teaching hours per week every teacher of this school must "
        "carry. It is used by the teaching hour workload recap of Manpower "
        "Planning. Zero means not set, so the recap does not judge a "
        "shortage or an excess of hours.",
    )
    co_teaching_hour_factor = fields.Float(
        string="Co-Teaching Hour Factor",
        default=0.5,
        help="Share of the subject hours counted for a co-teacher, from 0 "
        "to 1. For example 0.5 counts half of the subject hours. It is "
        "used by the teaching hour workload recap of Manpower Planning.",
    )

    @api.constrains("teacher_mandatory_weekly_hours", "co_teaching_hour_factor")
    def _check_teaching_hour_settings(self):
        """Reject a negative mandatory hour or an out of range factor.

        :raises ValidationError: when the mandatory weekly hours are
            negative, or when the co-teaching factor is outside 0 to 1.
        """
        for school in self.sudo():
            if school.teacher_mandatory_weekly_hours < 0:
                error_message = (
                    _(
                        """
Context: Validate school teaching hour settings
Database ID: %s
Problem: Teacher mandatory weekly hours must not be negative.
Solution: Enter zero or a positive number of hours
"""
                    )
                    % (school.id,)
                )
                raise ValidationError(error_message)
            if not 0 <= school.co_teaching_hour_factor <= 1:
                error_message = (
                    _(
                        """
Context: Validate school teaching hour settings
Database ID: %s
Problem: Co-teaching hour factor must be between 0 and 1.
Solution: Enter a factor from 0 to 1
"""
                    )
                    % (school.id,)
                )
                raise ValidationError(error_message)
