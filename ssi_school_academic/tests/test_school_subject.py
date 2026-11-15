# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolSubject(YamlTransactionCase):  # pylint: disable=too-few-public-methods
    """Cover the ``school_subject`` and ``school_subject_minimum_score`` models.

    The scenarios exercise creating, editing and archiving a subject
    with its minimum score lines, and the three constraints on a
    minimum score line: one line per grade, a score from 0 to 100, and
    a grade among the applicable grades of the subject.
    """

    def test_subject(self):
        """Run the subject and minimum score scenarios."""
        self.run_yaml_scenario("test_school_subject.yaml")
