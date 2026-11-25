# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import AccessError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolScoreSheetComponentAccess(YamlTransactionCase):
    """Cover the display name of a component for a limited user.

    The manager of the learning outcomes has no access to the score
    sheets. The learning objective form must still open for that user
    when the objective is used on a sheet, without opening the sheet.
    Every test runs as that user and checks a returned value or an
    access error, so all of them are pure Python (P1, L-01: the
    ``call`` action discards the return value of a method).
    """

    def setUp(self):
        """Create a sheet of another user and the limited user.

        The sheet belongs to the administrator and has one daily test
        component that measures one learning objective. The limited
        user is an internal user of the learning outcome group only.
        """
        super().setUp()
        env = self.env
        count = env["school_grade_type"].search_count([])
        grade_type = env["school_grade_type"].create(
            {"name": "SSSA Grade Type", "code": "SSSAGT%d" % count}
        )
        school = env["school"].create(
            {
                "name": "SSSA School",
                "code": "SSSASC%d" % env["school"].search_count([]),
                "grade_type_id": grade_type.id,
            }
        )
        year = env["school_academic_year"].create(
            {
                "name": "SSSA Year",
                "code": "SSSAAY%d" % env["school_academic_year"].search_count([]),
                "date_start": date(2026, 7, 1),
                "date_end": date(2027, 6, 30),
            }
        )
        term = env["school_academic_term"].create(
            {
                "name": "SSSA Term",
                "code": "SSSATM%d" % env["school_academic_term"].search_count([]),
                "date_start": date(2026, 7, 1),
                "date_end": date(2026, 12, 31),
                "year_id": year.id,
            }
        )
        grade = env["school_grade"].create(
            {
                "name": "SSSA Grade",
                "code": "SSSAGR%d" % env["school_grade"].search_count([]),
                "type_id": grade_type.id,
            }
        )
        grade_class = env["school_grade_class"].create(
            {
                "name": "SSSA Class",
                "code": "SSSACL%d" % env["school_grade_class"].search_count([]),
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        subject = env["school_subject"].create(
            {
                "name": "SSSA Subject",
                "code": "SSSASJ%d" % env["school_subject"].search_count([]),
                "grade_ids": [(6, 0, [grade.id])],
            }
        )
        partner = env["res.partner"].create({"name": "SSSA Teacher Home"})
        employee = env["hr.employee"].create(
            {
                "name": "SSSA Teacher Employee",
                "company_id": env.ref("base.main_company").id,
                "address_home_id": partner.id,
            }
        )
        teacher = env["school_teacher"].create(
            {
                "name": "SSSA Teacher",
                "code": "SSSATC%d" % env["school_teacher"].search_count([]),
                "employee_id": employee.id,
            }
        )
        self.component = env["school_score_component"].create(
            {
                "name": "SSSA UH 1",
                "code": "SSSAC%d" % env["school_score_component"].search_count([]),
                "category": "daily_test",
                "sequence": 10,
            }
        )
        outcome = env["school_subject_outcome"].create(
            {
                "name": "SSSA Outcome",
                "code": "SSSACP%d" % env["school_subject_outcome"].search_count([]),
                "subject_id": subject.id,
                "grade_id": grade.id,
                "academic_term_id": term.id,
            }
        )
        self.objective = env["school_subject_outcome_objective"].create(
            {
                "outcome_id": outcome.id,
                "code": "SSSATP1",
                "description": "Explains the basic concepts.",
            }
        )
        self.sheet = env["school_score_sheet"].create(
            {
                "academic_term_id": term.id,
                "grade_class_id": grade_class.id,
                "subject_id": subject.id,
                "teacher_id": teacher.id,
                "date": date(2026, 8, 10),
                "user_id": env.ref("base.user_admin").id,
            }
        )
        self.sheet_component = env["school_score_sheet_component"].create(
            {
                "sheet_id": self.sheet.id,
                "component_id": self.component.id,
                "objective_ids": [(6, 0, [self.objective.id])],
            }
        )
        self.limited_user = env["res.users"].create(
            {
                "name": "SSSA Outcome Manager",
                "login": "sssa_outcome_manager",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            env.ref("base.group_user").id,
                            env.ref(
                                "ssi_school_academic.school_subject_outcome_group"
                            ).id,
                        ],
                    )
                ],
            }
        )

    def _assert_readable_name(self):
        """Check the name and the objective form read as limited user.

        The name is the component name followed by the number of the
        sheet, which is ``/`` while the sheet has no number.
        """
        user = self.limited_user
        component = self.sheet_component.with_user(user)
        self.assertEqual(
            component.name_get(),
            [(self.sheet_component.id, "SSSA UH 1 (/)")],
        )
        data = self.objective.with_user(user).read(["score_sheet_component_ids"])
        self.assertEqual(
            data[0]["score_sheet_component_ids"], [self.sheet_component.id]
        )

    def test_name_get_draft_sheet(self):
        """Read the component name of a draft sheet as limited user.

        Pure Python (P1, L-01): the returned value of ``name_get`` is
        asserted, and ``action: call`` discards it.
        """
        self.assertEqual(self.sheet.state, "draft")
        self._assert_readable_name()

    def test_name_get_done_sheet(self):
        """Read the component name of a done sheet as limited user.

        Pure Python (P1, L-01): the returned value of ``name_get`` is
        asserted, and ``action: call`` discards it.
        """
        self.sheet.write({"state": "done"})
        self._assert_readable_name()

    def test_sheet_stays_closed(self):
        """Check the limited user still cannot read the sheet itself.

        Pure Python (P1, L-01): the access error comes from a read
        done as another user, with the result of the read not kept by
        the ``call`` action.
        """
        with self.assertRaises(AccessError):
            self.sheet.with_user(self.limited_user).read(["name"])
