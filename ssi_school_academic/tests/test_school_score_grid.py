# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolScoreGrid(YamlTransactionCase):
    """Cover the server side of the score grid of the score sheet.

    The grid asks ``school_score_sheet`` for the layout of its
    calculated columns and for their values. Both methods return a
    value, so every test is pure Python (P1, L-01: the ``call`` action
    discards the return value of a method).
    """

    def setUp(self):
        """Create the components and one Mid-Term and one Final type.

        Every other report card type is archived first, so exactly one
        type of each term type is active. The Mid-Term type averages two
        components (70%) and weights the mid-term exam (30%); the Final
        type averages the same two (50%), weights the mid-term exam
        (20%) and the final exam (30%).
        """
        super().setUp()
        type_model = self.env["school_report_card_type"]
        type_model.search([]).write({"active": False})
        component_model = self.env["school_score_component"]
        self.uh1 = component_model.create(
            {
                "name": "UH 1",
                "code": "SGRDA",
                "category": "daily_test",
                "sequence": 10,
            }
        )
        self.task1 = component_model.create(
            {
                "name": "Tugas 1",
                "code": "SGRDB",
                "category": "assignment",
                "sequence": 20,
            }
        )
        self.pts = component_model.create(
            {
                "name": "PTS",
                "code": "SGRDC",
                "category": "mid_term_exam",
                "sequence": 30,
            }
        )
        self.pas = component_model.create(
            {
                "name": "PAS",
                "code": "SGRDD",
                "category": "final_exam",
                "sequence": 40,
            }
        )
        self.mid_type = type_model.create(
            {
                "name": "Mid-Term SGR",
                "code": "SGRTYPEA",
                "term_type": "mid_term",
                "average_weight": 70.0,
                "average_component_ids": [(6, 0, [self.uh1.id, self.task1.id])],
                "weight_ids": [(0, 0, {"component_id": self.pts.id, "weight": 30.0})],
            }
        )
        self.final_type = type_model.create(
            {
                "name": "Final SGR",
                "code": "SGRTYPEB",
                "term_type": "final",
                "average_weight": 50.0,
                "average_component_ids": [(6, 0, [self.uh1.id, self.task1.id])],
                "weight_ids": [
                    (0, 0, {"component_id": self.pts.id, "weight": 20.0}),
                    (0, 0, {"component_id": self.pas.id, "weight": 30.0}),
                ],
            }
        )
        self.sheet_model = self.env["school_score_sheet"]

    def _layout_by_key(self):
        """Return the layout of the grid keyed by column key.

        :return: ``{key: column dict}`` of ``get_score_grid_layout``.
        :rtype: dict
        """
        layout = self.sheet_model.get_score_grid_layout()
        return {column["key"]: column for column in layout}

    def test_layout_order_and_position(self):
        """Assert the layout lists the three columns after the right cell.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``get_score_grid_layout``). The average
        sits after the last averaged component, the mid and final
        scores after the last component that feeds them.
        """
        layout = self.sheet_model.get_score_grid_layout()
        self.assertEqual(
            [column["key"] for column in layout], ["average", "mid", "final"]
        )
        by_key = self._layout_by_key()
        self.assertEqual(by_key["average"]["after_component_id"], self.task1.id)
        self.assertEqual(by_key["mid"]["after_component_id"], self.pts.id)
        self.assertEqual(by_key["final"]["after_component_id"], self.pas.id)
        for column in layout:
            self.assertFalse(column["warning"])

    def test_scores_follow_the_report_card_rules(self):
        """Assert the grid values are the ones of the report card.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_score_grid``). A zero is a score
        and takes part; a student without a score of an input component
        gets None, not 0. String keys are accepted, as JSON gives them.
        """
        scores = {
            101: {self.uh1.id: 80.0, self.task1.id: 91.0, self.pts.id: 70.0},
            102: {self.uh1.id: 0.0, self.task1.id: 100.0},
            103: {self.pas.id: 70.0},
            104: {},
        }
        result = self.sheet_model.compute_score_grid(scores)
        first = {self.uh1.id: 80.0, self.task1.id: 91.0, self.pts.id: 70.0}
        self.assertEqual(
            result[101]["average"], self.final_type.compute_average_score(first)
        )
        self.assertEqual(result[101]["mid"], self.mid_type.compute_final_score(first))
        self.assertEqual(
            result[101]["final"], self.final_type.compute_final_score(first)
        )
        self.assertEqual(result[101]["average"], 86.0)
        zero = {self.uh1.id: 0.0, self.task1.id: 100.0}
        self.assertEqual(result[102]["average"], 50.0)
        self.assertEqual(result[102]["mid"], self.mid_type.compute_final_score(zero))
        self.assertIsNone(result[103]["average"])
        self.assertIsNone(result[103]["mid"])
        self.assertEqual(result[103]["final"], 70.0)
        self.assertEqual(result[104], {"average": None, "mid": None, "final": None})
        as_json = self.sheet_model.compute_score_grid(
            {"101": {str(self.uh1.id): 80.0, str(self.task1.id): 91.0}}
        )
        self.assertEqual(as_json[101]["average"], 86.0)

    def test_two_final_types_leave_the_columns_empty(self):
        """Assert two active Final types empty the average and the final.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_score_grid``). The warning is set
        and the column has no position; the mid column, whose term type
        still has exactly one active type, is still calculated.
        """
        self.env["school_report_card_type"].create(
            {
                "name": "Final SGR Second",
                "code": "SGRTYPEC",
                "term_type": "final",
                "average_weight": 100.0,
                "average_component_ids": [(6, 0, [self.uh1.id])],
            }
        )
        by_key = self._layout_by_key()
        for key in ("average", "final"):
            self.assertTrue(by_key[key]["warning"])
            self.assertFalse(by_key[key]["after_component_id"])
        self.assertFalse(by_key["mid"]["warning"])
        self.assertEqual(by_key["mid"]["after_component_id"], self.pts.id)
        result = self.sheet_model.compute_score_grid(
            {101: {self.uh1.id: 80.0, self.task1.id: 90.0}}
        )
        self.assertIsNone(result[101]["average"])
        self.assertIsNone(result[101]["final"])
        self.assertEqual(result[101]["mid"], 85.0)

    def test_no_active_type_leaves_the_column_empty(self):
        """Assert a term type without an active type warns and stays empty.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_score_grid``).
        """
        self.mid_type.write({"active": False})
        by_key = self._layout_by_key()
        self.assertTrue(by_key["mid"]["warning"])
        self.assertFalse(by_key["mid"]["after_component_id"])
        result = self.sheet_model.compute_score_grid({101: {self.uh1.id: 80.0}})
        self.assertIsNone(result[101]["mid"])
        self.assertEqual(result[101]["final"], 80.0)
