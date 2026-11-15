# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolScoreSheet(HttpSavepointCase):
    """Tour tests for the ``school_score_sheet`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the master data and score sheets required by the tours.

        Every scenario owns a dedicated Subject (suffixed CREATE,
        GENERATE, CONFIRM, APPROVE, REJECT, CANCEL, RESTART). The
        unique key of a sheet is its term, class and subject, so each
        scenario can move its own sheet without affecting another one,
        and no suffix is a prefix of another, so the list always shows
        one uniquely-named row per scenario.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR SSS Grade Type", "code": "/"}
        )
        school = cls.env["school"].create(
            {"name": "TOUR SSS School", "code": "/", "grade_type_id": grade_type.id}
        )
        year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR SSS Year",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        cls.term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR SSS Term",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {"name": "TOUR SSS Grade", "code": "/", "type_id": grade_type.id}
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR SSS Class",
                "code": "/",
                "school_id": school.id,
                "grade_id": cls.grade.id,
            }
        )
        partner = cls.env["res.partner"].create({"name": "TOUR SSS Teacher Address"})
        employee = cls.env["hr.employee"].create(
            {
                "name": "TOUR SSS Teacher Employee",
                "company_id": cls.env.ref("base.main_company").id,
                "address_home_id": partner.id,
            }
        )
        cls.teacher = cls.env["school_teacher"].create(
            {"name": "TOUR SSS Teacher", "code": "/", "employee_id": employee.id}
        )
        cls.component = cls.env["school_score_component"].create(
            {
                "name": "TOUR SSS Daily Test 1",
                "code": "/",
                "category": "daily_test",
                "sequence": 10,
            }
        )
        cls.enrollments = cls.env["school_enrollment"]
        for index in (1, 2):
            cls.enrollments |= cls._create_open_enrollment(
                school, year, index, "TOUR SSS Student %s" % index
            )
        # ``global_use`` makes the reason selectable on every document;
        # without it the wizard radio does not offer the reason.
        cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR SSS Cancel Reason",
                "code": "TOURSSSCR",
                "global_use": True,
            }
        )

        # ── Create tour: only the Subject exists, no sheet yet ──
        cls._create_subject("CREATE")

        # ── Generate Lines tour: a Draft sheet without lines ──
        cls._create_sheet("GENERATE")

        # ── Confirm tour: a Draft sheet with lines ──
        confirm = cls._create_sheet("CONFIRM")
        cls._add_lines(confirm)

        # ── Approve tour: a sheet Waiting for Approval ──
        approve = cls._create_sheet("APPROVE")
        cls._add_lines(approve)
        cls._confirm(approve)

        # ── Reject tour: a sheet Waiting for Approval ──
        reject = cls._create_sheet("REJECT")
        cls._add_lines(reject)
        cls._confirm(reject)

        # ── Cancel tour: a Draft sheet with lines ──
        cancel = cls._create_sheet("CANCEL")
        cls._add_lines(cancel)

        # ── Restart Approval tour: a sheet Waiting for Approval ──
        restart = cls._create_sheet("RESTART")
        cls._add_lines(restart)
        cls._confirm(restart)

    @classmethod
    def _create_open_enrollment(cls, school, year, index, student_name):
        """Create a student and open its enrollment through its workflow.

        :param school: the ``school`` record of the student
        :param year: the ``school_academic_year`` of the enrollment
        :param index: number used to name the contact and the student
        :param student_name: name of the new student
        :return: the opened ``school_enrollment`` record
        """
        contact = cls.env["res.partner"].create({"name": "TOUR SSS Contact %s" % index})
        student = cls.env["school_student"].create(
            {
                "name": student_name,
                "code": "/",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = cls.env["school_enrollment"].create(
            {
                "academic_year_id": year.id,
                "academic_term_id": cls.term.id,
                "school_id": school.id,
                "grade_id": cls.grade.id,
                "grade_class_id": cls.grade_class.id,
                "student_id": student.id,
                "currency_id": cls.env.company.currency_id.id,
            }
        )
        enrollment = enrollment.with_user(cls.admin).with_context(
            bypass_policy_check=True
        )
        enrollment.action_confirm()
        enrollment.invalidate_cache()
        enrollment.action_approve_approval()
        enrollment.invalidate_cache()
        return enrollment

    @classmethod
    def _create_subject(cls, suffix):
        """Create the dedicated Subject of a scenario.

        :param suffix: scenario name appended to the Subject name
        :return: the new ``school_subject`` record
        """
        return cls.env["school_subject"].create(
            {
                "name": "TOUR SSS Subject %s" % suffix,
                "code": "/",
                "grade_ids": [(6, 0, [cls.grade.id])],
            }
        )

    @classmethod
    def _create_sheet(cls, suffix):
        """Create a Draft sheet for the dedicated Subject of a scenario.

        :param suffix: scenario name appended to the Subject name
        :return: the new ``school_score_sheet`` record
        """
        subject = cls._create_subject(suffix)
        return cls.env["school_score_sheet"].create(
            {
                "academic_term_id": cls.term.id,
                "grade_class_id": cls.grade_class.id,
                "subject_id": subject.id,
                "teacher_id": cls.teacher.id,
                "date": "2026-08-10",
                "user_id": cls.admin.id,
            }
        )

    @classmethod
    def _add_lines(cls, sheet):
        """Fill a sheet with one line per open enrollment.

        :param sheet: the ``school_score_sheet`` record to fill
        :return: nothing
        """
        sheet.with_user(cls.admin).action_generate_lines()
        sheet.invalidate_cache()

    @classmethod
    def _confirm(cls, sheet):
        """Move a sheet to Waiting for Approval through its action.

        :param sheet: the ``school_score_sheet`` record to confirm
        :return: nothing
        """
        sheet = sheet.with_user(cls.admin)
        sheet.action_confirm()
        sheet.invalidate_cache()

    def test_create(self):
        """Run the create tour for ``school_score_sheet``.

        IK: docs/school_score_sheet/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_score_sheet_create",
            login="admin",
        )

    def test_generate_lines(self):
        """Run the generate lines tour for ``school_score_sheet``.

        IK: docs/school_score_sheet/02-generate-lines.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_score_sheet_generate_lines",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_score_sheet``.

        IK: docs/school_score_sheet/03-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_score_sheet_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_score_sheet``.

        IK: docs/school_score_sheet/04-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_score_sheet_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_score_sheet``.

        IK: docs/school_score_sheet/05-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_score_sheet_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_score_sheet``.

        IK: docs/school_score_sheet/06-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_score_sheet_cancel",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour for ``school_score_sheet``.

        IK: docs/school_score_sheet/07-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_score_sheet_restart_approval",
            login="admin",
        )
