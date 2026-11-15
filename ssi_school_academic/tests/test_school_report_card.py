# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolReportCard(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``school_report_card`` model and its detail lines.

    The scenarios exercise generating the lines per subject, computing
    the final score, minimum score and predicate from the score sheets
    that are done, the manual parts, the confirm and approve workflow,
    and the constraints on the enrollment, the absence days and the
    subjects.
    """

    def test_report_card(self):
        """Run the report card scenarios."""
        self.run_yaml_scenario("test_school_report_card.yaml")
