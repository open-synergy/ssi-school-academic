# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolTeachingAssignmentDelete(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the guard on deleting a teaching assignment.

    The scenarios refuse the deletion of a line and of a document while
    a score sheet that is not cancelled exists for the same term, grade
    class and subject, whatever the role of the line. They also delete
    what has no such sheet, and release the cancelled sheets that still
    point at a deleted line.
    """

    def test_teaching_assignment_delete(self):
        """Run the teaching assignment delete scenarios."""
        self.run_yaml_scenario("test_school_teaching_assignment_delete.yaml")
