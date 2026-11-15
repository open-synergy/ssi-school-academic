# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolAcademicOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Test the operating unit glue of the school academic documents.

    Covers the ``operating_unit_id`` field added to
    ``school_score_sheet`` and ``school_report_card``, and the record
    rule that limits each document to the operating units of the user.
    """

    def test_school_academic_operating_unit(self):
        """Run the operating unit scenarios.

        Creates a score sheet and a report card with an explicit
        operating unit, then checks what a user of each operating unit
        can find and read.
        """
        self.run_yaml_scenario("test_data_school_academic_operating_unit.yaml")
