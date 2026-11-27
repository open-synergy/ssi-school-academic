# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolCurriculum(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the school curriculum and its lines.

    The scenarios exercise the workflow from draft to done with the
    approval that opens the curriculum, the cancel and reject paths,
    the total time and category of a line, the constraints of the lines
    and of the header, the one open curriculum per school, and the lock
    of the header and the lines outside draft.
    """

    def test_school_curriculum(self):
        """Run the school curriculum scenarios."""
        self.run_yaml_scenario("test_school_curriculum.yaml")
