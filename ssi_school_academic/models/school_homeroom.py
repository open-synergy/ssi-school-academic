# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv import expression


class SchoolHomeroom(models.Model):
    # Shows the teaching assignment lines of the homeroom: which
    # teacher teaches which subject, with which role. It also gives
    # the homeroom a label with its class, for the dropdown of the
    # teaching assignment line.
    _inherit = "school_homeroom"

    teaching_assignment_line_ids = fields.One2many(
        string="Teaching Assignment Lines",
        comodel_name="school_teaching_assignment_line",
        inverse_name="homeroom_id",
        help="Lines of the teaching assignments that name this "
        "homeroom, for every teacher who teaches in it.",
    )

    def name_get(self):
        """Return the display names, with the class when asked for.

        A draft homeroom has no document number yet, so its usual name
        is only ``*`` and its id, which tells nothing to the user who
        picks it. With the context key ``teaching_assignment_label`` the
        name is the grade class, the academic term and the usual name.

        :return: list of ``(id, name)`` tuples
        """
        result = super().name_get()
        if not self.env.context.get("teaching_assignment_label"):
            return result
        labels = []
        for record_id, name in result:
            record = self.browse(record_id)
            label = "%s - %s (%s)" % (
                record.grade_class_id.name,
                record.academic_term_id.name,
                name,
            )
            labels.append((record_id, label))
        return labels

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        """Search by the name of the grade class when asked for.

        With the context key ``teaching_assignment_label`` the typed
        text is searched on the name of the grade class as well as on
        the usual name.

        :param name: text typed in the dropdown
        :param args: extra domain
        :param operator: search operator on the text
        :param limit: maximum number of results
        :param name_get_uid: user the names are read with
        :return: ids of the matching homerooms
        """
        if self.env.context.get("teaching_assignment_label") and name:
            domain = expression.AND(
                [
                    args or [],
                    [
                        "|",
                        ("grade_class_id.name", operator, name),
                        ("name", operator, name),
                    ],
                ]
            )
            return self._search(domain, limit=limit, access_rights_uid=name_get_uid)
        return super()._name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )
