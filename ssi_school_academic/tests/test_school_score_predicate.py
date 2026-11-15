# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolScorePredicate(YamlTransactionCase):
    """Cover the ``school_score_predicate`` and its lines.

    The scenarios exercise creating, editing and archiving a predicate
    table, and its three constraints: one active table per grade,
    unique minimum scores in a table, and minimum scores between 0 and
    100. The return values of ``get_predicate_line`` and
    ``_get_predicate_for_grade`` are covered by pure Python methods.
    """

    def setUp(self):
        """Create the grades and the predicate tables.

        Builds two grades, a table for the first grade with the lines
        A (90), B (80), C (70) and D (0), and a table for the second
        grade with the lines A (90) and C (70) only, so no line starts
        at 0.
        """
        super().setUp()
        grade_type = self.env["school_grade_type"].create(
            {"name": "Predicate Py Grade Type", "code": "/", "sequence": 10}
        )
        grade_model = self.env["school_grade"]
        self.grade_a = grade_model.create(
            {
                "name": "Predicate Py Grade A",
                "code": "/",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        self.grade_b = grade_model.create(
            {
                "name": "Predicate Py Grade B",
                "code": "/",
                "sequence": 20,
                "type_id": grade_type.id,
            }
        )
        self.grade_c = grade_model.create(
            {
                "name": "Predicate Py Grade C",
                "code": "/",
                "sequence": 30,
                "type_id": grade_type.id,
            }
        )
        predicate_model = self.env["school_score_predicate"]
        self.full_table = predicate_model.create(
            {
                "name": "Predicate Py Full",
                "code": "/",
                "grade_ids": [(6, 0, [self.grade_a.id])],
                "line_ids": [
                    (0, 0, {"name": "A", "min_score": 90.0}),
                    (0, 0, {"name": "B", "min_score": 80.0}),
                    (0, 0, {"name": "C", "min_score": 70.0}),
                    (0, 0, {"name": "D", "min_score": 0.0}),
                ],
            }
        )
        self.partial_table = predicate_model.create(
            {
                "name": "Predicate Py Partial",
                "code": "/",
                "grade_ids": [(6, 0, [self.grade_b.id])],
                "line_ids": [
                    (0, 0, {"name": "A", "min_score": 90.0}),
                    (0, 0, {"name": "C", "min_score": 70.0}),
                ],
            }
        )

    def test_score_predicate(self):
        """Run the score predicate scenarios."""
        self.run_yaml_scenario("test_school_score_predicate.yaml")

    def test_predicate_line_top(self):
        """Assert a score of 90 earns predicate A.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``get_predicate_line``).
        """
        self.assertEqual(self.full_table.get_predicate_line(90.0).name, "A")

    def test_predicate_line_just_below_boundary(self):
        """Assert a score of 89.99 earns predicate B.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``get_predicate_line``).
        """
        self.assertEqual(self.full_table.get_predicate_line(89.99).name, "B")

    def test_predicate_line_middle(self):
        """Assert a score of 70 earns predicate C.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``get_predicate_line``).
        """
        self.assertEqual(self.full_table.get_predicate_line(70.0).name, "C")

    def test_predicate_line_lowest(self):
        """Assert a score of 5 earns predicate D.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``get_predicate_line``).
        """
        self.assertEqual(self.full_table.get_predicate_line(5.0).name, "D")

    def test_predicate_line_no_match(self):
        """Assert a score of 5 gives no line without a minimum of 0.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``get_predicate_line``).
        """
        self.assertFalse(self.partial_table.get_predicate_line(5.0))

    def test_predicate_for_grade_found(self):
        """Assert the active table of a grade is returned.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``_get_predicate_for_grade``).
        """
        result = self.env["school_score_predicate"]._get_predicate_for_grade(
            self.grade_a
        )
        self.assertEqual(result, self.full_table)

    def test_predicate_for_grade_archived(self):
        """Assert an archived table is not returned for its grade.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``_get_predicate_for_grade``).
        """
        self.full_table.write({"active": False})
        result = self.env["school_score_predicate"]._get_predicate_for_grade(
            self.grade_a
        )
        self.assertFalse(result)

    def test_predicate_for_grade_missing(self):
        """Assert a grade outside every table gives an empty result.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``_get_predicate_for_grade``).
        """
        result = self.env["school_score_predicate"]._get_predicate_for_grade(
            self.grade_c
        )
        self.assertFalse(result)
