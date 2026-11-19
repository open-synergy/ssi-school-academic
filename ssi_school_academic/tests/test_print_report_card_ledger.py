# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Deviation from the odoo-yaml-test standard (P1, L-01).

The ledger buttons return an ``ir.actions.report`` dict and the HTML
report is rendered and read back as text, which YAML cannot express
because ``action: call`` drops the return value of a method (L-01).

CI runs on Python 3.6 -- no walrus operator.
"""
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged

HTML_REPORT = "ssi_school_academic.report_print_report_card_ledger_html"
PDF_REPORT = "ssi_school_academic.report_print_report_card_ledger_pdf"


@tagged("post_install", "-at_install")
class TestPrintReportCardLedger(YamlTransactionCase):
    """Cover the ``print_report_card_ledger`` wizard.

    The YAML scenarios exercise the rows, the cells, the columns and the
    rank of the ledger. The Python scenario exercises the report
    actions and the text of the HTML report.
    """

    def test_ledger(self):
        """Run the ledger YAML scenarios."""
        self.run_yaml_scenario("test_print_report_card_ledger.yaml")

    def setUp(self):
        """Create a class with two open enrollments and one done card.

        The first student has a done report card with a score below the
        minimum score of its subject, the second student has no report
        card.

        :return: nothing
        """
        super().setUp()
        env = self.env
        count = env["school"].search_count([])
        grade_type = env["school_grade_type"].create(
            {"name": "PLDG Grade Type", "code": "PLDGGT%d" % count}
        )
        school = env["school"].create(
            {
                "name": "PLDG School",
                "code": "PLDGSC%d" % count,
                "grade_type_id": grade_type.id,
            }
        )
        year = env["school_academic_year"].create(
            {
                "name": "PLDG Academic Year",
                "code": "PLDGAY%d" % count,
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        self.term = env["school_academic_term"].create(
            {
                "name": "PLDG Term",
                "code": "PLDGTM%d" % count,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        grade = env["school_grade"].create(
            {
                "name": "PLDG Grade",
                "code": "PLDGGR%d" % count,
                "type_id": grade_type.id,
            }
        )
        self.grade_class = env["school_grade_class"].create(
            {
                "name": "PLDG Class",
                "code": "PLDGCL%d" % count,
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        self.subject = env["school_subject"].create(
            {
                "name": "PLDG Subject",
                "code": "PLDGSJ%d" % count,
                "grade_ids": [(6, 0, [grade.id])],
                "minimum_score_ids": [
                    (0, 0, {"grade_id": grade.id, "minimum_score": 75.0})
                ],
            }
        )
        component = env["school_score_component"].create(
            {
                "name": "PLDG UH",
                "code": "PLDGC%d" % count,
                "category": "daily_test",
                "sequence": 10,
            }
        )
        self.card_type = env["school_report_card_type"].create(
            {
                "name": "PLDG Final",
                "code": "PLDGRT%d" % count,
                "term_type": "final",
                "average_weight": 100.0,
                "average_component_ids": [(6, 0, [component.id])],
            }
        )
        admin = env.ref("base.user_admin")
        enrollments = []
        for index in (1, 2):
            contact = env["res.partner"].create({"name": "PLDG Contact %d" % index})
            student = env["school_student"].create(
                {
                    "name": "PLDG Student %d" % index,
                    "code": "PLDGST%d_%d" % (count, index),
                    "contact_id": contact.id,
                    "school_id": school.id,
                }
            )
            enrollment = env["school_enrollment"].create(
                {
                    "academic_year_id": year.id,
                    "academic_term_id": self.term.id,
                    "school_id": school.id,
                    "grade_id": grade.id,
                    "grade_class_id": self.grade_class.id,
                    "student_id": student.id,
                    "currency_id": env.company.currency_id.id,
                }
            )
            enrollment.with_user(admin).action_confirm()
            enrollment.invalidate_cache()
            enrollment.with_user(admin).action_approve_approval()
            enrollments.append(enrollment)
        card = env["school_report_card"].create(
            {
                "enrollment_id": enrollments[0].id,
                "type_id": self.card_type.id,
                "print_city": "Jakarta",
                "print_date": "2026-12-20",
                "user_id": admin.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "subject_id": self.subject.id,
                            "final_score": 70.0,
                            "is_scored": True,
                        },
                    )
                ],
            }
        )
        card.with_user(admin).action_confirm()
        card.invalidate_cache()
        card.with_user(admin).action_approve_approval()

    def _create_wizard(self):
        """Create a ledger wizard for the class of the fixture.

        :return: the new wizard.
        :rtype: recordset of ``print_report_card_ledger``
        """
        return self.env["print_report_card_ledger"].create(
            {
                "grade_class_id": self.grade_class.id,
                "academic_term_id": self.term.id,
                "type_id": self.card_type.id,
            }
        )

    def test_show_html_report(self):
        """Show the ledger and read back its HTML (P1, L-01).

        The Show button returns the HTML report action, and the HTML
        carries the title, the students, a dash for the student
        without a done report card and the red background of the score
        below the minimum score.
        """
        wizard = self._create_wizard()
        action = wizard.action_show()
        self.assertEqual(action["type"], "ir.actions.report")
        self.assertEqual(action["report_name"], HTML_REPORT)
        report = self.env["ir.actions.report"]._get_report_from_name(HTML_REPORT)
        html = report._render_qweb_html(wizard.ids)[0].decode("utf-8")
        self.assertIn("Report Card Ledger", html)
        self.assertIn("PLDG Student 1", html)
        self.assertIn("PLDG Student 2", html)
        self.assertIn("PLDG Subject", html)
        self.assertIn("background-color: #f8b4b4;", html)
        self.assertIn("70.00", html)
        self.assertEqual(len(wizard.line_ids), 2)
        self.assertEqual(wizard.line_ids[0].rank, 1)
        self.assertEqual(wizard.line_ids[1].rank, 0)

    def test_print_pdf_action(self):
        """Print the ledger and read the PDF report action (P1, L-01).

        The Print button returns the PDF report action of the same
        ledger; the PDF itself is not rendered.
        """
        wizard = self._create_wizard()
        action = wizard.action_print()
        self.assertEqual(action["type"], "ir.actions.report")
        self.assertEqual(action["report_name"], PDF_REPORT)
        self.assertEqual(action["report_type"], "qweb-pdf")
        self.assertEqual(len(wizard.line_ids), 2)
