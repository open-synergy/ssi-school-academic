# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolScoreComponent(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the ``school_score_component`` model.

    The scenarios exercise creating components of the different
    categories, changing the sequence of a component, and searching
    the components by category.
    """

    def test_score_component(self):
        """Run the score component scenarios."""
        self.run_yaml_scenario("test_school_score_component.yaml")
