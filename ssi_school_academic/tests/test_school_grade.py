# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolGrade(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the ``phase`` field added to ``school_grade``."""

    def test_grade_phase(self):
        """Run the grade phase scenario."""
        self.run_yaml_scenario("test_school_grade.yaml")
