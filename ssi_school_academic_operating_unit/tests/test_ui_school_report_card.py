# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolReportCardOperatingUnit(HttpSavepointCase):
    """Tour tests for the ``school_report_card`` operating unit delta."""

    @classmethod
    def setUpClass(cls):
        """Grant admin the groups needed to see the Operating Unit field.

        The multi operating unit group is required for the Operating Unit
        field itself to be rendered on the form. The viewer group of the
        document is granted explicitly so the tour does not depend on an
        implied group chain to reach the menu.
        """
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")
        cls.env.ref("ssi_school_academic.school_report_card_viewer_group").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.user_admin.id)]}
        )

    def test_field_ou(self):
        """Run the delta tour for the report card create form.

        IK: docs/school_report_card/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_operating_unit_school_report_card_field_ou",
            login="admin",
        )
