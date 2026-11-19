# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiPrintReportCardLedger(HttpSavepointCase):
    """Tour tests for the ``print_report_card_ledger`` instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the class, the term and the type the tour picks.

        Pre-Condition IK: the grade class, the academic term and the
        report card type chosen in the dialog exist. The user of the
        tour is the admin, who is in the report card groups.
        """
        super().setUpClass()
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR LDG Grade Type", "code": "/"}
        )
        school = cls.env["school"].create(
            {"name": "TOUR LDG School", "code": "/", "grade_type_id": grade_type.id}
        )
        year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR LDG Year",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        cls.term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR LDG Term",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        grade = cls.env["school_grade"].create(
            {"name": "TOUR LDG Grade", "code": "/", "type_id": grade_type.id}
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR LDG Class",
                "code": "/",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        component = cls.env["school_score_component"].create(
            {
                "name": "TOUR LDG UH",
                "code": "/",
                "category": "daily_test",
                "sequence": 10,
            }
        )
        cls.card_type = cls.env["school_report_card_type"].create(
            {
                "name": "TOUR LDG Type",
                "code": "/",
                "term_type": "final",
                "average_weight": 100.0,
                "average_component_ids": [(6, 0, [component.id])],
            }
        )

    def test_print(self):
        """Run the print tour for ``print_report_card_ledger``.

        The Print button is not clicked: it downloads a PDF file, which
        has no DOM signal of completion.

        IK: docs/print_report_card_ledger/01-print.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_print_report_card_ledger_print",
            login="admin",
        )
