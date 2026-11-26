# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolTeachingAssignmentOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Test the operating unit glue of the teaching assignment.

    Covers the record rule that limits the teaching assignments to the
    operating units of the user, and the propagation of the operating
    unit by the generate score sheet wizard and the copy wizard.
    """

    def test_school_teaching_assignment_operating_unit(self):
        """Run the teaching assignment operating unit scenarios.

        Checks what a user of one unit finds, the unit of the sheets the
        generate wizard creates for one unit and for several units, and
        the units of an assignment copied to another term.
        """
        self.run_yaml_scenario("test_school_teaching_assignment_operating_unit.yaml")
