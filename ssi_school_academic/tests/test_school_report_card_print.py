# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Deviation from the odoo-yaml-test standard (P1, L-01).

The print helper returns a dict and the report is rendered to an ODT
package whose XML is read back, which YAML cannot express because
``action: call`` drops the return value of a method (L-01). Acting as
another user is also Python only.

CI runs on Python 3.6 -- no walrus operator.
"""
import os
from io import BytesIO
from unittest import mock
from zipfile import ZipFile

from lxml import etree
from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import AccessError
from odoo.tests import tagged

LINE_MODEL = (
    "odoo.addons.ssi_school_academic.models.school_report_card_line."
    "SchoolReportCardLine._get_component_scores"
)


@tagged("post_install", "-at_install")
class TestSchoolReportCardPrint(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover the py3o print of ``school_report_card``.

    The report is rendered to an ODT without the PDF conversion, then
    the text of ``content.xml`` and ``styles.xml`` is checked.
    """

    def setUp(self):
        """Create an open enrollment, two report card types and subjects.

        :return: nothing
        """
        super().setUp()
        env = self.env
        count = env["school"].search_count([])
        grade_type = env["school_grade_type"].create(
            {"name": "PRT Grade Type", "code": "PRTGT%d" % count}
        )
        self.school = env["school"].create(
            {
                "name": "PRT School",
                "code": "PRTSC%d" % count,
                "grade_type_id": grade_type.id,
            }
        )
        year = env["school_academic_year"].create(
            {
                "name": "PRT Academic Year",
                "code": "PRTAY%d" % count,
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        term = env["school_academic_term"].create(
            {
                "name": "PRT Term",
                "code": "PRTTM%d" % count,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        self.grade = env["school_grade"].create(
            {
                "name": "PRT Grade",
                "code": "PRTGR%d" % count,
                "type_id": grade_type.id,
                "phase": "E",
            }
        )
        grade_class = env["school_grade_class"].create(
            {
                "name": "PRT Class",
                "code": "PRTCL%d" % count,
                "school_id": self.school.id,
                "grade_id": self.grade.id,
                "expertise_program": "PRT Program",
                "expertise_concentration": "PRT Concentration",
            }
        )
        self.subject = self._create_subject("PRT Subject A", "general", count)
        self.subject_2 = self._create_subject("PRT Subject B", "vocational", count)
        self.comp_1 = self._create_component("PRT UH 1", 10, count)
        self.comp_2 = self._create_component("PRT UH 2", 20, count)
        pts = self._create_component("PRT PTS", 30, count)
        self.comp_3 = self._create_component("PRT UH 3", 40, count)
        self.comp_4 = self._create_component("PRT UH 4", 50, count)
        self.count = count
        self.pts = pts
        self.mid_type = env["school_report_card_type"].create(
            {
                "name": "PRT Mid-Term",
                "code": "PRTMT%d" % count,
                "term_type": "mid_term",
                "average_weight": 70.0,
                "average_component_ids": [(6, 0, [self.comp_1.id, self.comp_2.id])],
                "weight_ids": [(0, 0, {"component_id": pts.id, "weight": 30.0})],
                "print_column_ids": [
                    (0, 0, {"component_id": self.comp_1.id, "sequence": 10}),
                    (0, 0, {"component_id": self.comp_2.id, "sequence": 20}),
                ],
            }
        )
        self.final_type = env["school_report_card_type"].create(
            {
                "name": "PRT Final",
                "code": "PRTFT%d" % count,
                "term_type": "final",
                "average_weight": 100.0,
                "average_component_ids": [(6, 0, [self.comp_1.id, self.comp_2.id])],
            }
        )
        contact = env["res.partner"].create({"name": "PRT Student Contact"})
        contact.nisn = "PRTNISN001"
        student = env["school_student"].create(
            {
                "name": "PRT Student",
                "code": "PRTST%d" % count,
                "contact_id": contact.id,
                "school_id": self.school.id,
            }
        )
        self.enrollment = env["school_enrollment"].create(
            {
                "academic_year_id": year.id,
                "academic_term_id": term.id,
                "school_id": self.school.id,
                "grade_id": self.grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
                "currency_id": env.company.currency_id.id,
            }
        )
        admin = env.ref("base.user_admin")
        self.enrollment.with_user(admin).action_confirm()
        self.enrollment.invalidate_cache()
        self.enrollment.with_user(admin).action_approve_approval()

    def _create_subject(self, name, group, count):
        """Create a subject taught in the grade.

        :param str name: name of the subject
        :param str group: ``general`` or ``vocational``
        :param int count: number used to make the code unique
        :return: the new subject
        """
        return self.env["school_subject"].create(
            {
                "name": name,
                "code": "PRT%s%d" % (name[-1], count),
                "subject_group": group,
                "grade_ids": [(6, 0, [self.grade.id])],
            }
        )

    def _create_component(self, name, sequence, count):
        """Create a score component.

        :param str name: name of the component
        :param int sequence: order of the component
        :param int count: number used to make the code unique
        :return: the new component
        """
        return self.env["school_score_component"].create(
            {
                "name": name,
                "code": "PRTC%d%d" % (sequence, count),
                "category": "daily_test",
                "sequence": sequence,
            }
        )

    def _create_card(self, card_type, **values):
        """Create a report card with one line per subject.

        :param card_type: report card type of the new report card
        :param values: extra values of the report card
        :return: the new report card
        """
        vals = {
            "enrollment_id": self.enrollment.id,
            "type_id": card_type.id,
            "print_city": "Jakarta",
            "print_date": "2026-12-20",
        }
        vals.update(values)
        card = self.env["school_report_card"].create(vals)
        line_model = self.env["school_report_card_line"]
        first = line_model.create(
            {
                "report_card_id": card.id,
                "subject_id": self.subject.id,
                "learning_objective": "PRT understands the concepts.",
            }
        )
        first.write({"is_scored": True, "final_score": 87.0})
        second = line_model.create(
            {"report_card_id": card.id, "subject_id": self.subject_2.id}
        )
        second.write({"is_scored": True, "final_score": 90.0})
        return card

    def _render_package(self, card):
        """Render the report of a report card to ODT without conversion.

        :param card: report card to print
        :return: the ODT package of the rendered report
        :rtype: bytes
        """
        report = self.env.ref("ssi_school_academic.report_school_report_card")
        engine = (
            self.env["py3o.report"]
            .with_context(report_py3o_skip_conversion=True)
            .create({"ir_actions_report_id": report.id})
        )
        path = engine._create_single_report(card, {})
        try:
            with open(path, "rb") as odt_file:
                return odt_file.read()
        finally:
            os.unlink(path)

    def _render(self, card):
        """Render the report of a report card to ODT without conversion.

        :param card: report card to print
        :return: the text of ``content.xml`` and ``styles.xml``
        :rtype: str
        """
        data = self._render_package(card)
        texts = []
        with ZipFile(BytesIO(data)) as package:
            for name in ("content.xml", "styles.xml"):
                root = etree.fromstring(package.read(name))
                texts.append(" ".join(root.itertext()))
        return "\n".join(texts)

    def _render_tables(self, card):
        """Return the score tables of the rendered report card.

        :param card: report card to print
        :return: ``{table name: number of columns}`` of the score tables
        :rtype: dict
        """
        data = self._render_package(card)
        with ZipFile(BytesIO(data)) as package:
            root = etree.fromstring(package.read("content.xml"))
        namespaces = {"table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0"}
        result = {}
        for table in root.iterfind(".//table:table", namespaces):
            name = table.get("{%s}name" % namespaces["table"])
            if name in ("FinalTable",) or name.startswith("MidTable"):
                result[name] = len(table.findall("table:table-column", namespaces))
        return result

    def _create_mid_type(self, columns):
        """Create a mid-term report card type with printed columns.

        :param list columns: ``(component, print title)`` per column, in
            the order they are printed
        :return: the new report card type
        """
        self.count += 1
        lines = [
            (
                0,
                0,
                {"component_id": comp.id, "sequence": 10 * pos, "print_title": title},
            )
            for pos, (comp, title) in enumerate(columns, start=1)
        ]
        return self.env["school_report_card_type"].create(
            {
                "name": "PRT Mid-Term %d" % self.count,
                "code": "PRTMX%d" % self.count,
                "term_type": "mid_term",
                "average_weight": 0.0,
                "weight_ids": [(0, 0, {"component_id": self.pts.id, "weight": 100.0})],
                "print_column_ids": lines,
            }
        )

    def test_report_record(self):
        """Check the report record (P1, L-01).

        The report is a py3o PDF report whose template file exists and
        which only the Viewer group may print.
        """
        report = self.env.ref("ssi_school_academic.report_school_report_card")
        self.assertEqual(report.report_type, "py3o")
        self.assertEqual(report.py3o_filetype, "pdf")
        self.assertEqual(report.model, "school_report_card")
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            report.py3o_template_fallback,
        )
        self.assertTrue(os.path.isfile(path))
        viewer = self.env.ref("ssi_school_academic.school_report_card_viewer_group")
        self.assertEqual(report.groups_id, viewer)

    def test_print_mid_term(self):
        """Check the mid-term print shows the component columns (P1, L-01).

        The header, the component names, the final score and the
        learning objective are in the rendered ODT.
        """
        card = self._create_card(self.mid_type)
        scores = {self.comp_1.id: 90.0}
        with mock.patch(LINE_MODEL, new=lambda line: scores):
            text = self._render(card)
        for expected in (
            "PRT Student",
            "PRTNISN001",
            "PRT Program",
            "PRT Concentration",
            "PRT UH 1",
            "PRT UH 2",
            "87",
            "PRT understands the concepts.",
            "Mid-Term Semester",
        ):
            self.assertIn(expected, text)
        with mock.patch(LINE_MODEL, new=lambda line: scores):
            data = card.get_report_card_print_data()
        self.assertEqual(data["header"]["phase"], "E")
        self.assertTrue(data["footer"].startswith("PRT Class | PRT Student | PRTST"))
        general = data["groups"][0]
        self.assertEqual(general["rows"][0]["scores"][:2], ["90", "-"])

    def test_print_final(self):
        """Check the final print has no component column (P1, L-01).

        The component names are not in the rendered ODT.
        """
        card = self._create_card(self.final_type)
        text = self._render(card)
        self.assertNotIn("PRT UH 1", text)
        self.assertIn("PRT Student", text)
        self.assertIn("87", text)
        data = card.get_report_card_print_data()
        self.assertFalse(data["show_components"])
        self.assertEqual(data["period"], "Semester")

    def test_print_unscored_line(self):
        """Check a line without any score prints a dash (P1, L-01).

        The row of the unscored subject has ``-`` as its final score
        and as its learning objective, and not ``0``, while the scored
        rows keep their score.
        """
        card = self._create_card(self.final_type)
        subject = self._create_subject("PRT Subject 3", "general", 3)
        self.env["school_report_card_line"].create(
            {"report_card_id": card.id, "subject_id": subject.id}
        )
        text = self._render(card)
        self.assertRegex(text, r"PRT Subject 3\s+-\s+-")
        self.assertIn("87", text)
        rows = card.get_report_card_print_data()["groups"][0]["rows"]
        unscored = [row for row in rows if row["subject"] == "PRT Subject 3"]
        self.assertEqual(len(unscored), 1)
        self.assertEqual(unscored[0]["final"], "-")
        self.assertEqual(unscored[0]["objective"], "-")

    def test_label_no(self):
        """Check the number column label is not the core ``No`` (P1, L-01).

        The source text of the label is ``No.`` so the translation of
        the core ``No`` (``Tidak`` in Indonesian) is never applied. In
        English the label is the source text. The placeholder key is
        unchanged.
        """
        card = self._create_card(self.final_type)
        data = card.with_context(lang="en_US").get_report_card_print_data()
        self.assertEqual(data["labels"]["no"], "No.")

    def test_empty_blocks_hidden(self):
        """Check the empty blocks are not printed (P1, L-01).

        Without co-curricular, extracurricular, note and parent
        response the labels of those blocks are not rendered, while
        the absence block is always printed.
        """
        card = self._create_card(self.final_type)
        text = self._render(card)
        for label in (
            "Co-Curricular",
            "Extracurricular",
            "Homeroom Teacher Note",
            "Parent Response",
        ):
            self.assertNotIn(label, text)
        self.assertIn("Absences", text)
        data = card.get_report_card_print_data()
        for key in (
            "co_curricular",
            "extracurricular",
            "homeroom_note",
            "parent_response",
        ):
            self.assertIs(data[key], False)

    def test_filled_blocks_printed(self):
        """Check the filled blocks are printed (P1, L-01).

        Two co-curricular themes are both printed, with the
        extracurricular, the note and the parent response.
        """
        card = self._create_card(
            self.final_type,
            homeroom_note="PRT keep it up",
            parent_response="PRT thank you",
            co_curricular_ids=[
                (0, 0, {"theme": "PRT Theme One", "description": "PRT first"}),
                (0, 0, {"theme": "PRT Theme Two", "description": "PRT second"}),
            ],
            extracurricular_ids=[(0, 0, {"name": "PRT Scout", "description": "Good"})],
        )
        text = self._render(card)
        for expected in (
            "Co-Curricular",
            "PRT Theme One",
            "PRT Theme Two",
            "PRT Scout",
            "PRT keep it up",
            "PRT thank you",
        ):
            self.assertIn(expected, text)

    def test_print_access_denied(self):
        """Check a user outside the Viewer group cannot print (P1, L-01).

        The helper raises ``AccessError`` for an internal user without
        the Viewer group of the report card.
        """
        card = self._create_card(self.final_type)
        user = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": "PRT Plain User",
                    "login": "prt_plain_user_%d" % card.id,
                    "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
                }
            )
        )
        with self.assertRaises(AccessError):
            card.with_user(user).get_report_card_print_data()

    def test_print_titles(self):
        """Check the print titles replace the component names (P1, L-01).

        Three columns titled SUM1 to SUM3 give three headers, three
        scores per row and a seven column table. The component names
        are not printed, and an empty title falls back to the name.
        """
        card_type = self._create_mid_type(
            [
                (self.comp_1, "SUM1"),
                (self.comp_2, "SUM2"),
                (self.comp_3, "SUM3"),
            ]
        )
        card = self._create_card(card_type)
        scores = {self.comp_1.id: 90.0, self.comp_2.id: 0.0}
        with mock.patch(LINE_MODEL, new=lambda line: scores):
            data = card.get_report_card_print_data()
            text = self._render(card)
        self.assertEqual(data["component_count"], 3)
        self.assertEqual(data["component_headers"], ["SUM1", "SUM2", "SUM3"])
        row = data["groups"][0]["rows"][0]
        self.assertEqual(len(row["scores"]), 3)
        self.assertEqual(row["scores"], ["90", "0", "-"])
        self.assertEqual(row["final"], "87")
        for expected in ("SUM1", "SUM2", "SUM3"):
            self.assertIn(expected, text)
        self.assertNotIn("PRT UH 1", text)
        self.assertEqual(self._render_tables(card), {"MidTable3": 7})

    def test_print_title_empty_uses_component_name(self):
        """Check an empty print title prints the component name (P1, L-01).

        The column order follows the sequence of the printed columns,
        not the sequence of the components.
        """
        card_type = self._create_mid_type([(self.comp_2, False), (self.comp_1, "SUM1")])
        card = self._create_card(card_type)
        with mock.patch(LINE_MODEL, new=lambda line: {}):
            data = card.get_report_card_print_data()
        self.assertEqual(data["component_headers"], ["PRT UH 2", "SUM1"])

    def test_print_column_count_tables(self):
        """Check one table variant per column count (P1, L-01).

        One to four columns print a table of four fixed columns plus
        one per component, zero columns print the final score table,
        and a final report card never prints component columns.
        """
        comps = [self.comp_1, self.comp_2, self.comp_3, self.comp_4]
        for count in range(0, 5):
            card_type = self._create_mid_type([(comp, False) for comp in comps[:count]])
            card = self._create_card(card_type)
            with mock.patch(LINE_MODEL, new=lambda line: {}):
                data = card.get_report_card_print_data()
                tables = self._render_tables(card)
            self.assertEqual(data["component_count"], count)
            self.assertEqual(len(data["component_headers"]), count)
            if count:
                self.assertEqual(
                    tables, {"MidTable%s" % ("" if count == 4 else count): 4 + count}
                )
            else:
                self.assertEqual(tables, {"FinalTable": 4})
        final_card = self._create_card(self.final_type)
        self.assertEqual(self._render_tables(final_card), {"FinalTable": 4})
        self.assertEqual(final_card.get_report_card_print_data()["component_count"], 0)

    def test_print_zero_score_and_unscored_component(self):
        """Check a zero score prints ``0`` and a missing one ``-`` (P1, L-01).

        The final score is the one of the report card line, also when a
        weighted component is not printed.
        """
        card = self._create_card(self.mid_type)
        scores = {self.comp_1.id: 0.0}
        with mock.patch(LINE_MODEL, new=lambda line: scores):
            data = card.get_report_card_print_data()
        row = data["groups"][0]["rows"][0]
        self.assertEqual(row["scores"], ["0", "-"])
        self.assertEqual(row["final"], "87")
