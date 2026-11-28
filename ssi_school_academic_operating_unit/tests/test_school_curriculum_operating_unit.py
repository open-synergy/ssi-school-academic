# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolCurriculumOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Test the operating unit glue of the school curriculum.

    Covers the ``operating_unit_id`` field added to ``school_curriculum``
    and the record rule that limits the curriculums to the operating
    units of the user, next to the company rule of the base module.
    """

    def test_school_curriculum_operating_unit(self):
        """Run the curriculum operating unit scenarios.

        Checks what a user of one operating unit finds, writes and is
        refused, and that a user of the company group still finds the
        curriculums of every operating unit of the company.
        """
        self.run_yaml_scenario("test_school_curriculum_operating_unit.yaml")
