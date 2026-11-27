# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchool(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the teaching hour settings added to ``school``."""

    def test_school_teaching_hours(self):
        """Run the school teaching hour settings scenario."""
        self.run_yaml_scenario("test_school.yaml")
