# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolScoreSheetColumnLock(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the column lock of ``school_score_sheet``.

    The scenarios exercise locking and unlocking a column by policy,
    the guards on a locked column, the report card reading the locked
    columns, the confirm guard and the copy of the scores.
    """

    def test_score_sheet_column_lock(self):
        """Run the score sheet column lock scenarios."""
        self.run_yaml_scenario("test_school_score_sheet_column_lock.yaml")
