# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolScoreSheetTeachingAssignment(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the teaching assignment defaults of the score sheet.

    The scenarios open a new score sheet as a teacher user and check
    the default teacher and term, the subject and line filled from the
    only main line of a class, and the open choice of a user without a
    main line.
    """

    def test_score_sheet_teaching_assignment(self):
        """Run the score sheet teaching assignment scenarios."""
        self.run_yaml_scenario("test_school_score_sheet_teaching_assignment.yaml")
