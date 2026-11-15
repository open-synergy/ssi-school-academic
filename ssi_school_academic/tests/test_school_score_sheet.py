# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolScoreSheet(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``school_score_sheet`` model.

    The scenarios exercise generating the lines from the open
    enrollments, the confirm and approve workflow, reject, restart and
    cancel, and the constraints on the scores and on the sheet.
    """

    def test_score_sheet(self):
        """Run the score sheet scenarios."""
        self.run_yaml_scenario("test_school_score_sheet.yaml")
