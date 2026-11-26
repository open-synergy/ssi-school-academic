# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import AccessError, UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolTeachingAssignmentAccess(YamlTransactionCase):
    """Cover who may read the teaching assignments and the score sheets.

    A main teacher reads the score sheets that belong to the teacher
    user and the own teaching assignment only. An assistant teacher
    reads, and never changes, the score sheet of the term, class and
    subject the teacher assists in. Every test runs as a limited user
    and checks a returned value or an access error, so all of them are
    pure Python (P1, L-01: the ``call`` action discards the return
    value of a method).
    """

    def _create_teacher(self, label, with_groups=True):
        """Create a teacher with an employee and an internal user.

        :param label: short text used in the names and the login
        :param with_groups: give the user the score sheet user group
        :return: tuple of the ``school_teacher`` and the ``res.users``
        """
        env = self.env
        groups = [env.ref("base.group_user").id]
        if with_groups:
            groups.append(
                env.ref("ssi_school_academic.school_score_sheet_user_group").id
            )
        user = env["res.users"].create(
            {
                "name": "SSTAA User %s" % label,
                "login": "sstaa_%s_%d" % (label, env["res.users"].search_count([])),
                "groups_id": [(6, 0, groups)],
            }
        )
        partner = env["res.partner"].create({"name": "SSTAA Home %s" % label})
        employee = env["hr.employee"].create(
            {
                "name": "SSTAA Employee %s" % label,
                "company_id": env.ref("base.main_company").id,
                "address_home_id": partner.id,
                "user_id": user.id,
            }
        )
        teacher = env["school_teacher"].create(
            {
                "name": "SSTAA Teacher %s" % label,
                "code": "SSTAATC%d" % env["school_teacher"].search_count([]),
                "employee_id": employee.id,
            }
        )
        return teacher, user

    def _create_line(self, teacher, homeroom, subject, role):
        """Create a teaching assignment line in the fixture term.

        The assignment of the teacher is created when it is missing.

        :param teacher: the ``school_teacher`` of the line
        :param homeroom: the ``school_homeroom`` of the line
        :param subject: the ``school_subject`` of the line
        :param role: ``main`` or ``assistant``
        :return: the new ``school_teaching_assignment_line``
        """
        env = self.env
        header = env["school_teaching_assignment"].search(
            [
                ("teacher_id", "=", teacher.id),
                ("academic_term_id", "=", self.term.id),
            ]
        )
        if not header:
            header = env["school_teaching_assignment"].create(
                {
                    "name": "SSTAA %s" % teacher.name,
                    "code": "/",
                    "teacher_id": teacher.id,
                    "academic_term_id": self.term.id,
                }
            )
        return env["school_teaching_assignment_line"].create(
            {
                "assignment_id": header.id,
                "homeroom_id": homeroom.id,
                "subject_id": subject.id,
                "role": role,
                "weekly_hours": 2,
            }
        )

    def _create_sheet(self, grade_class, subject, teacher, user):
        """Create a draft score sheet owned by a user.

        :param grade_class: the ``school_grade_class`` of the sheet
        :param subject: the ``school_subject`` of the sheet
        :param teacher: the ``school_teacher`` of the sheet
        :param user: the ``res.users`` that owns the sheet
        :return: the new ``school_score_sheet``
        """
        return self.env["school_score_sheet"].create(
            {
                "academic_term_id": self.term.id,
                "grade_class_id": grade_class.id,
                "subject_id": subject.id,
                "teacher_id": teacher.id,
                "date": date(2026, 8, 10),
                "user_id": user.id,
            }
        )

    def setUp(self):
        """Create the term, the classes, three teachers and their lines.

        The main teacher teaches subject A in class X, the assistant
        teacher assists in the same subject and class, and the third
        teacher has no line. The main teacher also teaches subject B in
        class Y. One sheet exists for each main line.
        """
        super().setUp()
        env = self.env
        grade_type = env["school_grade_type"].create(
            {
                "name": "SSTAA Grade Type",
                "code": "SSTAAGT%d" % env["school_grade_type"].search_count([]),
            }
        )
        school = env["school"].create(
            {
                "name": "SSTAA School",
                "code": "SSTAASC%d" % env["school"].search_count([]),
                "grade_type_id": grade_type.id,
            }
        )
        year = env["school_academic_year"].create(
            {
                "name": "SSTAA Year",
                "code": "SSTAAAY%d" % env["school_academic_year"].search_count([]),
                "date_start": date(2026, 7, 1),
                "date_end": date(2027, 6, 30),
            }
        )
        self.term = env["school_academic_term"].create(
            {
                "name": "SSTAA Term",
                "code": "SSTAATM%d" % env["school_academic_term"].search_count([]),
                "date_start": date(2026, 7, 1),
                "date_end": date(2026, 12, 31),
                "year_id": year.id,
                "state": "open",
            }
        )
        grade = env["school_grade"].create(
            {
                "name": "SSTAA Grade",
                "code": "SSTAAGR%d" % env["school_grade"].search_count([]),
                "type_id": grade_type.id,
            }
        )
        self.class_x = env["school_grade_class"].create(
            {
                "name": "SSTAA Class X",
                "code": "SSTAACX%d" % env["school_grade_class"].search_count([]),
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        self.class_y = env["school_grade_class"].create(
            {
                "name": "SSTAA Class Y",
                "code": "SSTAACY%d" % env["school_grade_class"].search_count([]),
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        self.subject_a = env["school_subject"].create(
            {
                "name": "SSTAA Subject A",
                "code": "SSTAASA%d" % env["school_subject"].search_count([]),
                "grade_ids": [(6, 0, [grade.id])],
            }
        )
        self.subject_b = env["school_subject"].create(
            {
                "name": "SSTAA Subject B",
                "code": "SSTAASB%d" % env["school_subject"].search_count([]),
                "grade_ids": [(6, 0, [grade.id])],
            }
        )
        homerooms = {}
        for key, grade_class in (("x", self.class_x), ("y", self.class_y)):
            homerooms[key] = env["school_homeroom"].create(
                {
                    "academic_year_id": year.id,
                    "academic_term_id": self.term.id,
                    "school_id": school.id,
                    "grade_id": grade.id,
                    "grade_class_id": grade_class.id,
                }
            )
        self.teacher_main, self.user_main = self._create_teacher("main")
        self.teacher_asst, self.user_asst = self._create_teacher("asst")
        self.teacher_none, self.user_none = self._create_teacher("none")
        self.line_main_x = self._create_line(
            self.teacher_main, homerooms["x"], self.subject_a, "main"
        )
        self.line_main_y = self._create_line(
            self.teacher_main, homerooms["y"], self.subject_b, "main"
        )
        self.line_asst = self._create_line(
            self.teacher_asst, homerooms["x"], self.subject_a, "assistant"
        )
        self.sheet_x = self._create_sheet(
            self.class_x, self.subject_a, self.teacher_main, self.user_main
        )
        self.sheet_y = self._create_sheet(
            self.class_y, self.subject_b, self.teacher_main, self.user_main
        )

    def test_default_teacher_and_term(self):
        """Check the defaults of a new sheet for a teacher user.

        Pure Python (P1, L-01): the values returned by ``default_get``
        are asserted. A user who is not a teacher gets no teacher.
        """
        env = self.env
        fields_list = ["teacher_id", "academic_term_id"]
        sheet_model = env["school_score_sheet"]
        values = sheet_model.with_user(self.user_main).default_get(fields_list)
        self.assertEqual(values["teacher_id"], self.teacher_main.id)
        first_open = env["school_academic_term"].search(
            [("state", "=", "open")], limit=1
        )
        self.assertEqual(values["academic_term_id"], first_open.id)
        plain_user = env["res.users"].create(
            {"name": "SSTAA Plain", "login": "sstaa_plain"}
        )
        values = sheet_model.with_user(plain_user).default_get(fields_list)
        self.assertFalse(values.get("teacher_id"))

    def test_allowed_lines_narrow_for_a_teacher(self):
        """Check the allowed lines, classes and subjects of a teacher.

        Pure Python (P1, L-01): the recordsets returned by the compute
        are asserted. The classes are the classes of the main lines,
        and the subjects are the ones of the chosen class.
        """
        sheet_model = self.env["school_score_sheet"].with_user(self.user_main)
        sheet = sheet_model.new({"academic_term_id": self.term.id})
        self.assertEqual(
            sheet.allowed_teaching_assignment_line_ids,
            self.line_main_x | self.line_main_y,
        )
        self.assertEqual(sheet.allowed_grade_class_ids, self.class_x | self.class_y)
        self.assertEqual(sheet.allowed_subject_ids, self.subject_a | self.subject_b)
        sheet = sheet_model.new(
            {
                "academic_term_id": self.term.id,
                "grade_class_id": self.class_y.id,
            }
        )
        self.assertEqual(sheet.allowed_subject_ids, self.subject_b)

    def test_allowed_lines_open_for_a_user_without_lines(self):
        """Check that a user without a main line is not restricted.

        Pure Python (P1, L-01): the recordsets returned by the compute
        are asserted. The allowed lines are empty, and every grade
        class and subject stays available.
        """
        env = self.env
        sheet = (
            env["school_score_sheet"]
            .with_user(self.user_none)
            .new({"academic_term_id": self.term.id})
        )
        self.assertFalse(sheet.allowed_teaching_assignment_line_ids)
        self.assertEqual(
            sheet.allowed_grade_class_ids,
            env["school_grade_class"].search([]),
        )
        self.assertEqual(
            sheet.allowed_subject_ids,
            env["school_subject"].search([]),
        )

    def test_onchange_fills_line_and_subject(self):
        """Check the onchange methods that fill the line and the subject.

        Pure Python (P1, L-01): the onchange methods are called on a
        new record and the values they assign are asserted. The only
        main line of the chosen class fills the line and the subject,
        and the chosen line fills the term, class and teacher.
        """
        sheet_model = self.env["school_score_sheet"].with_user(self.user_main)
        sheet = sheet_model.new(
            {
                "academic_term_id": self.term.id,
                "grade_class_id": self.class_x.id,
            }
        )
        sheet.onchange_teaching_assignment_line_id()
        self.assertEqual(sheet.teaching_assignment_line_id, self.line_main_x)
        sheet.onchange_subject_id()
        self.assertEqual(sheet.subject_id, self.subject_a)
        sheet = sheet_model.new({"teaching_assignment_line_id": self.line_main_y.id})
        sheet.onchange_academic_term_id()
        sheet.onchange_grade_class_id()
        sheet.onchange_teacher_id()
        sheet.onchange_subject_id()
        self.assertEqual(sheet.academic_term_id, self.term)
        self.assertEqual(sheet.grade_class_id, self.class_y)
        self.assertEqual(sheet.teacher_id, self.teacher_main)
        self.assertEqual(sheet.subject_id, self.subject_b)

    def test_onchange_class_without_line_clears_the_line(self):
        """Check the line is cleared when the class does not match it.

        Pure Python (P1, L-01): the onchange method is called on a new
        record and the value it assigns is asserted. The user is not a
        teacher, so no line fits any class.
        """
        sheet = (
            self.env["school_score_sheet"]
            .with_user(self.user_none)
            .new(
                {
                    "academic_term_id": self.term.id,
                    "grade_class_id": self.class_x.id,
                    "teaching_assignment_line_id": self.line_main_y.id,
                }
            )
        )
        sheet.onchange_teaching_assignment_line_id()
        self.assertFalse(sheet.teaching_assignment_line_id)

    def test_main_teacher_reads_own_sheets_only(self):
        """Check a teacher finds the own sheets and no other sheet.

        Pure Python (P1, L-01): the result of ``search`` is asserted.
        """
        sheet_model = self.env["school_score_sheet"]
        domain = [("id", "in", [self.sheet_x.id, self.sheet_y.id])]
        found = sheet_model.with_user(self.user_main).search(domain)
        self.assertEqual(found, self.sheet_x | self.sheet_y)
        found = sheet_model.with_user(self.user_none).search(domain)
        self.assertFalse(found)

    def test_assistant_reads_but_never_changes(self):
        """Check an assistant teacher reads the sheet and cannot write.

        Pure Python (P1, L-01): the result of ``search`` is asserted,
        and the access errors come from calls done as another user.
        The assistant reads the sheet of class X only.
        """
        sheet_model = self.env["school_score_sheet"]
        domain = [("id", "in", [self.sheet_x.id, self.sheet_y.id])]
        found = sheet_model.with_user(self.user_asst).search(domain)
        self.assertEqual(found, self.sheet_x)
        sheet = self.sheet_x.with_user(self.user_asst)
        self.assertEqual(
            sheet.read(["teacher_id"])[0]["teacher_id"][0], self.teacher_main.id
        )
        with self.assertRaises(AccessError):
            sheet.write({"date": date(2026, 8, 12)})
        with self.assertRaises(AccessError):
            sheet.unlink()
        with self.assertRaises(AccessError):
            self.sheet_y.with_user(self.user_asst).read(["date"])

    def test_assistant_users_compute_and_search(self):
        """Check the assistant users of a sheet and the search on them.

        Pure Python (P1, L-01): the computed recordset and the result
        of ``search`` are asserted. The negative operators return the
        other sheets, and an operator that is not supported raises.
        """
        sheet_model = self.env["school_score_sheet"]
        self.assertEqual(self.sheet_x.assistant_user_ids, self.user_asst)
        self.assertFalse(self.sheet_y.assistant_user_ids)
        scope = [("id", "in", [self.sheet_x.id, self.sheet_y.id])]
        found = sheet_model.search(
            scope + [("assistant_user_ids", "in", [self.user_asst.id])]
        )
        self.assertEqual(found, self.sheet_x)
        found = sheet_model.search(
            scope + [("assistant_user_ids", "=", self.user_asst.id)]
        )
        self.assertEqual(found, self.sheet_x)
        found = sheet_model.search(
            scope + [("assistant_user_ids", "not in", [self.user_asst.id])]
        )
        self.assertEqual(found, self.sheet_y)
        found = sheet_model.search(
            scope + [("assistant_user_ids", "!=", self.user_asst.id)]
        )
        self.assertEqual(found, self.sheet_y)
        with self.assertRaises(UserError):
            sheet_model.search([("assistant_user_ids", "like", "x")])

    def test_teacher_reads_own_assignment_only(self):
        """Check a teacher finds the own lines and assignment only.

        Pure Python (P1, L-01): the result of ``search`` is asserted,
        and the access error comes from a read done as another user.
        """
        env = self.env
        line_model = env["school_teaching_assignment_line"]
        found = line_model.with_user(self.user_main).search([])
        self.assertEqual(found, self.line_main_x | self.line_main_y)
        found = line_model.with_user(self.user_none).search([])
        self.assertFalse(found)
        header = self.line_asst.assignment_id
        with self.assertRaises(AccessError):
            header.with_user(self.user_main).read(["name"])
        with self.assertRaises(AccessError):
            self.line_asst.with_user(self.user_main).write({"weekly_hours": 9})

    def test_line_display_name_for_limited_user(self):
        """Check the display name of a line reads for a user without access.

        Pure Python (P1, L-01): the value returned by ``name_get`` is
        asserted. The name joins the teacher, class and subject.
        """
        env = self.env
        limited = env["res.users"].create(
            {"name": "SSTAA Limited", "login": "sstaa_limited"}
        )
        result = self.line_main_x.with_user(limited).name_get()
        self.assertEqual(
            result,
            [
                (
                    self.line_main_x.id,
                    "SSTAA Teacher main / SSTAA Class X / SSTAA Subject A",
                )
            ],
        )

    def test_generate_wizard_needs_read_access(self):
        """Check the generate wizard refuses an assignment the user hides.

        Pure Python (P9, L-21): the wizard runs as the superuser for
        the work and checks the rights of the real user first, so the
        check itself is what is tested.
        """
        env = self.env
        group = env.ref("ssi_school_academic.school_teaching_assignment_group")
        manager = env["res.users"].create(
            {
                "name": "SSTAA Manager",
                "login": "sstaa_manager",
                "groups_id": [(6, 0, [env.ref("base.group_user").id, group.id])],
            }
        )
        wizard = (
            env["generate_score_sheet_from_teaching_assignment"]
            .with_user(manager)
            .create({"assignment_ids": [(6, 0, [self.line_asst.assignment_id.id])]})
        )
        result = wizard.action_generate()
        self.assertEqual(result["res_model"], wizard._name)
        self.assertIn("Score sheets created: 0", wizard.result_note)
        teacher_wizard = env["generate_score_sheet_from_teaching_assignment"].create(
            {"assignment_ids": [(6, 0, [self.line_asst.assignment_id.id])]}
        )
        with self.assertRaises(AccessError):
            teacher_wizard.with_user(self.user_main).action_generate()

    def test_homeroom_label_and_search(self):
        """Check the homeroom label and search used by the line dropdown.

        Pure Python (P1, L-01): the values returned by ``name_get`` and
        ``name_search`` are asserted. Without the context key the usual
        name is kept.
        """
        homeroom = self.line_main_x.homeroom_id
        plain = homeroom.name_get()
        labelled = homeroom.with_context(teaching_assignment_label=True).name_get()
        self.assertNotEqual(plain, labelled)
        self.assertIn("SSTAA Class X - SSTAA Term", labelled[0][1])
        model = self.env["school_homeroom"].with_context(teaching_assignment_label=True)
        found = model.name_search("SSTAA Class X")
        self.assertEqual([item[0] for item in found], [homeroom.id])
        plain_found = self.env["school_homeroom"].name_search("SSTAA Class X")
        self.assertFalse(plain_found)
