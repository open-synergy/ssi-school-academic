# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolReportCardType(YamlTransactionCase):
    """Cover the ``school_report_card_type`` and its weight lines.

    The scenarios exercise creating and editing a report card type, and
    its four constraints: weights totalling 100%, a component weighted
    once, averaged components when an average weight is set, and a
    rounding threshold between 0 and 1. The ``compute_final_score``
    return value is covered by pure Python methods.
    """

    def setUp(self):
        """Create the components and the report card types.

        Builds a mid-term type (70% average of two components, 30%
        mid-term exam) and a final type (50% average, 20% mid-term
        exam, 30% final exam), both with the default threshold.
        """
        super().setUp()
        component_model = self.env["school_score_component"]
        self.uh1 = component_model.create(
            {"name": "UH 1", "code": "RCTP1A", "category": "daily_test"}
        )
        self.task1 = component_model.create(
            {"name": "Tugas 1", "code": "RCTP1B", "category": "assignment"}
        )
        self.pts = component_model.create(
            {"name": "PTS", "code": "RCTP1C", "category": "mid_term_exam"}
        )
        self.pas = component_model.create(
            {"name": "PAS", "code": "RCTP1D", "category": "final_exam"}
        )
        type_model = self.env["school_report_card_type"]
        self.mid_type = type_model.create(
            {
                "name": "Mid-Term P1",
                "code": "RCTYPEP1",
                "term_type": "mid_term",
                "average_weight": 70.0,
                "average_component_ids": [(6, 0, [self.uh1.id, self.task1.id])],
                "weight_ids": [(0, 0, {"component_id": self.pts.id, "weight": 30.0})],
            }
        )
        self.final_type = type_model.create(
            {
                "name": "Final P1",
                "code": "RCTYPEP2",
                "term_type": "final",
                "average_weight": 50.0,
                "average_component_ids": [(6, 0, [self.uh1.id, self.task1.id])],
                "weight_ids": [
                    (0, 0, {"component_id": self.pts.id, "weight": 20.0}),
                    (0, 0, {"component_id": self.pas.id, "weight": 30.0}),
                ],
            }
        )

    def test_report_card_type(self):
        """Run the report card type scenarios."""
        self.run_yaml_scenario("test_school_report_card_type.yaml")

    def test_final_score_below_threshold(self):
        """Assert a raw score of 87.45 rounds down to 87.0.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_final_score``).
        """
        scores = {self.uh1.id: 87.0, self.task1.id: 87.0, self.pts.id: 88.5}
        self.assertEqual(self.mid_type.compute_final_score(scores), 87.0)

    def test_final_score_at_threshold(self):
        """Assert a raw score of 87.56 rounds up to 88.0.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_final_score``).
        """
        scores = {self.uh1.id: 87.8, self.task1.id: 87.8, self.pts.id: 87.0}
        self.assertEqual(self.mid_type.compute_final_score(scores), 88.0)

    def test_final_score_just_below_threshold(self):
        """Assert a raw score of 87.55 rounds down to 87.0.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_final_score``).
        """
        scores = {self.uh1.id: 88.0, self.task1.id: 88.0, self.pts.id: 86.5}
        self.assertEqual(self.mid_type.compute_final_score(scores), 87.0)

    def test_final_score_missing_component(self):
        """Assert a missing mid-term exam score does not pull to 0.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_final_score``).
        """
        scores = {self.uh1.id: 98.0}
        self.assertEqual(self.mid_type.compute_final_score(scores), 98.0)

    def test_final_score_no_scores(self):
        """Assert an empty score dict gives 0.0.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_final_score``).
        """
        self.assertEqual(self.mid_type.compute_final_score({}), 0.0)

    def test_final_score_final_type(self):
        """Assert the final type computes 79.0 from 80, 90 and 70.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_final_score``).
        """
        scores = {
            self.uh1.id: 80.0,
            self.task1.id: 80.0,
            self.pts.id: 90.0,
            self.pas.id: 70.0,
        }
        self.assertEqual(self.final_type.compute_final_score(scores), 79.0)

    def test_final_score_zero_counts_in_average(self):
        """Assert a filled score of 0 enters the average: 53.0.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_final_score``).
        """
        average_type = self.env["school_report_card_type"].create(
            {
                "name": "Average Only P1",
                "code": "RCTYPEP3",
                "term_type": "final",
                "average_weight": 100.0,
                "average_component_ids": [
                    (6, 0, [self.uh1.id, self.task1.id, self.pts.id])
                ],
            }
        )
        scores = {self.uh1.id: 80.0, self.task1.id: 80.0, self.pts.id: 0.0}
        self.assertEqual(average_type.compute_final_score(scores), 53.0)

    def test_final_score_average_rounds_half_up(self):
        """Assert averages of 87.5 and 86.5 round up to 88 and 87.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_final_score``). Python's own
        ``round`` sends 86.5 to 86 (nearest even), which is why the
        average is rounded with ``float_round``.
        """
        scores = {self.uh1.id: 87.0, self.task1.id: 88.0}
        self.assertEqual(self.mid_type.compute_final_score(scores), 88.0)
        scores = {self.uh1.id: 86.0, self.task1.id: 87.0}
        self.assertEqual(self.mid_type.compute_final_score(scores), 87.0)

    def test_final_score_average_rounds_down_below_half(self):
        """Assert an average of 87.49 rounds down to 87 before the weight.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        the return value of ``compute_final_score``).
        """
        scores = {self.uh1.id: 87.0, self.task1.id: 87.98}
        self.assertEqual(self.mid_type.compute_final_score(scores), 87.0)
