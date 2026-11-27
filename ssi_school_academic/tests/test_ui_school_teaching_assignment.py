# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolTeachingAssignment(HttpSavepointCase):
    """Tour tests for the ``school_teaching_assignment`` work instructions."""

    @classmethod
    def _create_structure(cls, label):
        """Create the school, grade, class and subject of a scenario.

        :param label: short text used in the names of the records
        :return: dict of the created records
        """
        env = cls.env
        grade_type = env["school_grade_type"].create(
            {"name": "TOUR %s Grade Type" % label, "code": "/"}
        )
        school = env["school"].create(
            {
                "name": "TOUR %s School" % label,
                "code": "/",
                "grade_type_id": grade_type.id,
            }
        )
        year = env["school_academic_year"].create(
            {
                "name": "TOUR %s Year" % label,
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        grade = env["school_grade"].create(
            {"name": "TOUR %s Grade" % label, "code": "/", "type_id": grade_type.id}
        )
        grade_class = env["school_grade_class"].create(
            {
                "name": "TOUR %s Class" % label,
                "code": "/",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        subject = env["school_subject"].create(
            {
                "name": "TOUR %s Subject" % label,
                "code": "/",
                "grade_ids": [(6, 0, [grade.id])],
            }
        )
        return {
            "school": school,
            "year": year,
            "grade": grade,
            "grade_class": grade_class,
            "subject": subject,
        }

    @classmethod
    def _create_term(cls, year, name, date_start, date_end):
        """Create an academic term of a year.

        :param year: the ``school_academic_year`` of the term
        :param name: name of the term
        :param date_start: first day of the term, as text
        :param date_end: last day of the term, as text
        :return: the new ``school_academic_term``
        """
        return cls.env["school_academic_term"].create(
            {
                "name": name,
                "code": "/",
                "date_start": date_start,
                "date_end": date_end,
                "year_id": year.id,
            }
        )

    @classmethod
    def _create_homeroom(cls, structure, term):
        """Create a homeroom of the class of a scenario in a term.

        :param structure: dict returned by ``_create_structure``
        :param term: the ``school_academic_term`` of the homeroom
        :return: the new ``school_homeroom``
        """
        return cls.env["school_homeroom"].create(
            {
                "academic_year_id": structure["year"].id,
                "academic_term_id": term.id,
                "school_id": structure["school"].id,
                "grade_id": structure["grade"].id,
                "grade_class_id": structure["grade_class"].id,
            }
        )

    @classmethod
    def _create_teacher(cls, label, with_user=True):
        """Create a teacher, with an employee and optionally a user.

        :param label: short text used in the names of the records
        :param with_user: link the employee to a new user
        :return: the new ``school_teacher``
        """
        env = cls.env
        partner = env["res.partner"].create({"name": "TOUR %s Home" % label})
        values = {
            "name": "TOUR %s Employee" % label,
            "company_id": env.ref("base.main_company").id,
            "address_home_id": partner.id,
        }
        if with_user:
            user = env["res.users"].create(
                {"name": "TOUR %s User" % label, "login": "tour_%s_user" % label}
            )
            values["user_id"] = user.id
        employee = env["hr.employee"].create(values)
        return env["school_teacher"].create(
            {
                "name": "TOUR %s Teacher" % label,
                "code": "/",
                "employee_id": employee.id,
            }
        )

    @classmethod
    def setUpClass(cls):
        """Create the master data the four tours work with.

        Pre-Condition IK: the teacher, the term, the homerooms and the
        subjects already exist. The create tour gets a teacher, a term,
        a homeroom and a subject to pick. The generate tour gets an
        assignment with one main line of a teacher who has a user. The
        copy tour gets two terms, an assignment in the first one, and
        the homeroom of the same class in both terms. The delete tour
        gets an assignment with one line and no score sheet.
        """
        super().setUpClass()
        create = cls._create_structure("TA")
        term = cls._create_term(
            create["year"], "TOUR TA Term", "2026-07-01", "2026-12-31"
        )
        cls._create_homeroom(create, term)
        cls._create_teacher("TA", with_user=False)

        generate = cls._create_structure("TG")
        term_generate = cls._create_term(
            generate["year"], "TOUR TG Term", "2026-07-01", "2026-12-31"
        )
        homeroom_generate = cls._create_homeroom(generate, term_generate)
        teacher_generate = cls._create_teacher("TG")
        header = cls.env["school_teaching_assignment"].create(
            {
                "name": "TOUR TG Assignment",
                "code": "/",
                "teacher_id": teacher_generate.id,
                "academic_term_id": term_generate.id,
            }
        )
        cls.env["school_teaching_assignment_line"].create(
            {
                "assignment_id": header.id,
                "homeroom_id": homeroom_generate.id,
                "subject_id": generate["subject"].id,
                "role": "main",
                "weekly_hours": 2,
            }
        )

        copy = cls._create_structure("TC")
        term_a = cls._create_term(
            copy["year"], "TOUR TC Term A", "2026-07-01", "2026-12-31"
        )
        term_b = cls._create_term(
            copy["year"], "TOUR TC Term B", "2027-01-01", "2027-06-30"
        )
        homeroom_a = cls._create_homeroom(copy, term_a)
        cls._create_homeroom(copy, term_b)
        teacher_copy = cls._create_teacher("TC", with_user=False)
        header_copy = cls.env["school_teaching_assignment"].create(
            {
                "name": "TOUR TC Assignment",
                "code": "/",
                "teacher_id": teacher_copy.id,
                "academic_term_id": term_a.id,
            }
        )
        cls.env["school_teaching_assignment_line"].create(
            {
                "assignment_id": header_copy.id,
                "homeroom_id": homeroom_a.id,
                "subject_id": copy["subject"].id,
                "role": "main",
                "weekly_hours": 2,
            }
        )

        delete = cls._create_structure("TD")
        term_delete = cls._create_term(
            delete["year"], "TOUR TD Term", "2026-07-01", "2026-12-31"
        )
        homeroom_delete = cls._create_homeroom(delete, term_delete)
        teacher_delete = cls._create_teacher("TD", with_user=False)
        header_delete = cls.env["school_teaching_assignment"].create(
            {
                "name": "TOUR TD Assignment",
                "code": "/",
                "teacher_id": teacher_delete.id,
                "academic_term_id": term_delete.id,
            }
        )
        cls.env["school_teaching_assignment_line"].create(
            {
                "assignment_id": header_delete.id,
                "homeroom_id": homeroom_delete.id,
                "subject_id": delete["subject"].id,
                "role": "main",
                "weekly_hours": 2,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_teaching_assignment``.

        IK: docs/school_teaching_assignment/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_teaching_assignment_create",
            login="admin",
        )

    def test_generate_score_sheets(self):
        """Run the generate score sheets tour for the assignment.

        IK: docs/school_teaching_assignment/03-generate-score-sheets.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_teaching_assignment_generate_score_sheets",
            login="admin",
        )

    def test_copy_from_previous_term(self):
        """Run the copy from the previous term tour for the assignments.

        IK: docs/school_teaching_assignment/04-copy-from-previous-term.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_teaching_assignment_copy_from_previous_term",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_teaching_assignment``.

        IK: docs/school_teaching_assignment/05-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_teaching_assignment_delete",
            login="admin",
        )
