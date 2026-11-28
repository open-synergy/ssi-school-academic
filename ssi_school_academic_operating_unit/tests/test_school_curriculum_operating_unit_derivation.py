# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolCurriculumOperatingUnitDerivation(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Test the derivation of the curriculum operating unit from its school.

    Covers the ``create``, ``write`` and onchange of ``school_id`` that
    set ``operating_unit_id`` from the operating unit of the school.
    """

    def test_school_curriculum_operating_unit_derivation(self):
        """Run the curriculum operating unit derivation scenarios.

        Checks the unit taken from a school with exactly one unit, an
        explicit unit that wins, the default unit kept for a school with
        no unit or several units, and the refusal of a user who does not
        hold the unit of the school.
        """
        self.run_yaml_scenario("test_school_curriculum_operating_unit_derivation.yaml")
