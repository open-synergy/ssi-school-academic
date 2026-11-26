# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolTeachingAssignment(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the teaching assignment models and their two wizards.

    The scenarios exercise the weekly hours of a header, the
    constraints on the header and on its lines, the lines listed on the
    homeroom and on the teacher, the generation of the score sheets
    from the main lines, and the copy of the assignments to another
    academic term.
    """

    def test_teaching_assignment(self):
        """Run the teaching assignment scenarios."""
        self.run_yaml_scenario("test_school_teaching_assignment.yaml")
