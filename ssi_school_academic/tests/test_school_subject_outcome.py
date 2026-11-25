# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolSubjectOutcome(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the learning outcome (CP) and objective (TP) features.

    The scenarios exercise the learning outcome master data and its
    one active record per scope, the learning objectives chosen on the
    score sheet components, and the learning objective text of the
    report card lines that is filled and refilled from them.
    """

    def test_subject_outcome(self):
        """Run the learning outcome and objective scenarios."""
        self.run_yaml_scenario("test_school_subject_outcome.yaml")

    def test_subject_outcome_generate_lines(self):
        """Run the scenario of generating the lines of a score sheet.

        The scenario counts the components of the sheet, and the setup
        of the other scenarios adds components with every replay, so
        it runs in a test method of its own (T-01, remedy 5).
        """
        self.run_yaml_scenario("test_school_subject_outcome_generate_lines.yaml")
