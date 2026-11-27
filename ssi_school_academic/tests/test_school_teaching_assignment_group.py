# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolTeachingAssignmentGroup(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the implied groups of the Teaching Assignment group.

    The scenarios check that the group implies the Homeroom Viewer
    group, but not the Homeroom User group, and that a user granted
    only this group inherits the same groups.
    """

    def test_teaching_assignment_group(self):
        """Run the Teaching Assignment group scenarios."""
        self.run_yaml_scenario("test_school_teaching_assignment_group.yaml")
