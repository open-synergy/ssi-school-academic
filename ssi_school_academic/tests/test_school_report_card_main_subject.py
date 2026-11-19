# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Deviation from the odoo-yaml-test standard (P1, L-01).

``_get_main_subjects`` returns a recordset, which YAML cannot read back
because ``action: call`` drops the return value of a method (L-01).

CI runs on Python 3.6 -- no walrus operator.
"""
from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolReportCardMainSubject(YamlTransactionCase):
    """Cover the ``school_report_card_main_subject`` model.

    The YAML scenarios exercise the create, edit and archive flow and
    the constraints. The Python scenario exercises the subject picker
    used by the score ledger.
    """

    def setUp(self):
        """Create two grades, three subjects and four grade classes.

        :return: nothing
        """
        super().setUp()
        env = self.env
        count = env["school"].search_count([])
        grade_type = env["school_grade_type"].create(
            {"name": "RCMSP Grade Type", "code": "RCMSPGT%d" % count}
        )
        self.school = env["school"].create(
            {
                "name": "RCMSP School",
                "code": "RCMSPSC%d" % count,
                "grade_type_id": grade_type.id,
            }
        )
        self.grade = env["school_grade"].create(
            {
                "name": "RCMSP Grade",
                "code": "RCMSPGR%d" % count,
                "type_id": grade_type.id,
            }
        )
        self.other_grade = env["school_grade"].create(
            {
                "name": "RCMSP Other Grade",
                "code": "RCMSPOG%d" % count,
                "type_id": grade_type.id,
                "sequence": 20,
            }
        )
        self.subjects = env["school_subject"]
        for index in range(3):
            self.subjects |= env["school_subject"].create(
                {
                    "name": "RCMSP Subject %d" % index,
                    "code": "RCMSPSB%d_%d" % (count, index),
                    "subject_group": "vocational",
                }
            )
        self.class_p = self._create_class("P", self.grade, "RCMSP Program P", count)
        self.class_q = self._create_class("Q", self.grade, "RCMSP Program Q", count)
        self.class_none = self._create_class("N", self.grade, False, count)
        self.class_other = self._create_class(
            "O", self.other_grade, "RCMSP Program P", count
        )

    def _create_class(self, suffix, grade, program, count):
        """Create a grade class of the test school.

        :param suffix: short text used in the name and the code.
        :param grade: ``school_grade`` record of the class.
        :param program: expertise program, ``False`` for none.
        :param count: number making the code unique.
        :return: the new grade class.
        :rtype: recordset of ``school_grade_class``
        """
        return self.env["school_grade_class"].create(
            {
                "name": "RCMSP Class %s" % suffix,
                "code": "RCMSPCL%s%d" % (suffix, count),
                "school_id": self.school.id,
                "grade_id": grade.id,
                "expertise_program": program,
            }
        )

    def _create_main(self, grade, program, subjects, code):
        """Create a main subject record.

        :param grade: ``school_grade`` record.
        :param program: expertise program, ``False`` for none.
        :param subjects: ``school_subject`` records.
        :param code: unique code of the record.
        :return: the new record.
        :rtype: recordset of ``school_report_card_main_subject``
        """
        return self.env["school_report_card_main_subject"].create(
            {
                "name": "RCMSP Main %s" % code,
                "code": code,
                "grade_id": grade.id,
                "expertise_program": program,
                "subject_ids": [(6, 0, subjects.ids)],
            }
        )

    def test_main_subject(self):
        """Run the main subject YAML scenarios."""
        self.run_yaml_scenario("test_school_report_card_main_subject.yaml")

    def test_get_main_subjects(self):
        """Pick the main subjects: program, fallback, then empty.

        Deviation P1, L-01: the picker returns a recordset that YAML
        cannot read back.
        """
        model = self.env["school_report_card_main_subject"]
        main_p = self._create_main(
            self.grade, "RCMSP Program P", self.subjects[0] | self.subjects[1], "RP"
        )
        fallback = self._create_main(self.grade, False, self.subjects[2], "RF")
        self.assertEqual(model._get_main_subjects(self.class_p), main_p.subject_ids)
        self.assertEqual(model._get_main_subjects(self.class_q), fallback.subject_ids)
        self.assertEqual(
            model._get_main_subjects(self.class_none), fallback.subject_ids
        )
        self.assertFalse(model._get_main_subjects(self.class_other))
        fallback.active = False
        self.assertFalse(model._get_main_subjects(self.class_q))
        self.assertEqual(model._get_main_subjects(self.class_p), main_p.subject_ids)
