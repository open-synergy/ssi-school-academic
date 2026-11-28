# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolTeachingAssignmentSync(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the sync of the draft score sheet with the main teacher.

    The scenarios change the teacher of a document, add a main line,
    change the role of a line and add a second main line. The draft
    score sheet of the same term, class and subject follows the main
    teacher, while the sheets that are not draft are not touched.
    The responsible user of the sheet follows the user account of the
    teacher, and a teacher without an account keeps the previous one.
    """

    def test_teaching_assignment_sync(self):
        """Run the teaching assignment sync scenarios."""
        self.run_yaml_scenario("test_school_teaching_assignment_sync.yaml")
