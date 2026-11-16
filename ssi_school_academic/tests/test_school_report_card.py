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

    def test_state_selection(self):
        """Check the state selection is unchanged (P1, L-01).

        The selection of the state field is redeclared in this module
        only to record the module of its values. The values, labels and
        order are the ones of the transaction mixins. The selection is
        a field attribute, which YAML cannot read (L-01).
        """
        expected = [
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("reject", "Rejected"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ]
        model = self.env["school_report_card"]
        self.assertEqual(model._fields["state"].selection, expected)
