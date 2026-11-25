# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolReportCard(HttpSavepointCase):
    """Tour tests for the ``school_report_card`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the master data and report cards required by the tours.

        One open enrollment is shared by every scenario. The unique key
        of a live report card is its enrollment and report card type,
        so every scenario owns a dedicated Report Card Type (suffixed
        CREATE, GENERATE, COMPUTE, REFILL, CONFIRM, APPROVE, REJECT,
        CANCEL).
        No suffix is a prefix of another, so the list always shows one
        uniquely-named row per scenario.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR SRC Grade Type", "code": "/"}
        )
        school = cls.env["school"].create(
            {"name": "TOUR SRC School", "code": "/", "grade_type_id": grade_type.id}
        )
        year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR SRC Year",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        cls.term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR SRC Term",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": year.id,
                "enrollment_state": "open",
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {"name": "TOUR SRC Grade", "code": "/", "type_id": grade_type.id}
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR SRC Class",
                "code": "/",
                "school_id": school.id,
                "grade_id": cls.grade.id,
            }
        )
        cls.subject = cls.env["school_subject"].create(
            {
                "name": "TOUR SRC Subject",
                "code": "/",
                "grade_ids": [(6, 0, [cls.grade.id])],
            }
        )
        cls.env["school_score_predicate"].create(
            {
                "name": "TOUR SRC Predicate",
                "code": "/",
                "grade_ids": [(6, 0, [cls.grade.id])],
                "line_ids": [
                    (0, 0, {"name": "TOUR SRC Top", "min_score": 80.0}),
                    (0, 0, {"name": "TOUR SRC Base", "min_score": 0.0}),
                ],
            }
        )
        partner = cls.env["res.partner"].create({"name": "TOUR SRC Teacher Address"})
        employee = cls.env["hr.employee"].create(
            {
                "name": "TOUR SRC Teacher Employee",
                "company_id": cls.env.ref("base.main_company").id,
                "address_home_id": partner.id,
            }
        )
        cls.teacher = cls.env["school_teacher"].create(
            {"name": "TOUR SRC Teacher", "code": "/", "employee_id": employee.id}
        )
        cls.component = cls.env["school_score_component"].create(
            {
                "name": "TOUR SRC Daily Test 1",
                "code": "/",
                "category": "daily_test",
                "sequence": 10,
            }
        )
        cls.enrollment = cls._create_open_enrollment(school, year)
        # ``global_use`` makes the reason selectable on every document;
        # without it the wizard radio does not offer the reason.
        cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR SRC Cancel Reason",
                "code": "TOURSRCCR",
                "global_use": True,
            }
        )

        # ── Create tour: only the Report Card Type exists ──
        cls._create_type("CREATE")

        # ── Generate Lines tour: a Draft report card without lines ──
        cls._create_card("GENERATE")

        # ── Compute Scores tour: lines generated before the score
        # sheet is done, so the Predicate changes when scores arrive ──
        compute = cls._create_card("COMPUTE")
        compute.with_user(cls.admin).action_generate_lines()
        compute.invalidate_cache()
        cls._create_done_sheet()

        # ── Refill tour: lines generated after the sheet is done, then a
        # text typed by hand over the filled learning objective ──
        refill = cls._create_card("REFILL")
        refill.with_user(cls.admin).action_generate_lines()
        refill.invalidate_cache()
        refill.line_ids.write({"learning_objective": "TOUR SRC manual text"})

        # ── Confirm tour: a Draft report card ──
        cls._create_card("CONFIRM")

        # ── Approve tour: a report card Waiting for Approval ──
        cls._confirm(cls._create_card("APPROVE"))

        # ── Reject tour: a report card Waiting for Approval ──
        cls._confirm(cls._create_card("REJECT"))

        # ── Cancel tour: a Draft report card ──
        cls._create_card("CANCEL")

    @classmethod
    def _create_open_enrollment(cls, school, year):
        """Create a student and open its enrollment through its workflow.

        :param school: the ``school`` record of the student
        :param year: the ``school_academic_year`` of the enrollment
        :return: the opened ``school_enrollment`` record
        """
        contact = cls.env["res.partner"].create({"name": "TOUR SRC Contact"})
        student = cls.env["school_student"].create(
            {
                "name": "TOUR SRC Student",
                "code": "/",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = cls.env["school_enrollment"].create(
            {
                # Manually assigned so the tour can pick this record
                # from the Enrollment m2o dropdown by typing
                # predictable text; the number is kept when it opens.
                "name": "TOUR-SRC-ENR-001",
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
    def _create_type(cls, suffix):
        """Create the dedicated Report Card Type of a scenario.

        :param suffix: scenario name appended to the type name
        :return: the new ``school_report_card_type`` record
        """
        return cls.env["school_report_card_type"].create(
            {
                "name": "TOUR SRC Type %s" % suffix,
                "code": "/",
                "term_type": "mid_term",
                "average_weight": 100.0,
                "average_component_ids": [(6, 0, [cls.component.id])],
            }
        )

    @classmethod
    def _create_card(cls, suffix):
        """Create a Draft report card for the type of a scenario.

        :param suffix: scenario name appended to the type name
        :return: the new ``school_report_card`` record
        """
        report_type = cls._create_type(suffix)
        return cls.env["school_report_card"].create(
            {
                "enrollment_id": cls.enrollment.id,
                "type_id": report_type.id,
                "print_date": "2026-12-20",
                "user_id": cls.admin.id,
            }
        )

    @classmethod
    def _create_done_sheet(cls):
        """Create a score sheet that is done, with one score of 90.

        :return: nothing
        """
        outcome = cls.env["school_subject_outcome"].create(
            {
                "name": "TOUR SRC Outcome",
                "code": "/",
                "subject_id": cls.subject.id,
                "grade_id": cls.grade.id,
                "academic_term_id": cls.term.id,
            }
        )
        objective = cls.env["school_subject_outcome_objective"].create(
            {
                "outcome_id": outcome.id,
                "code": "TOUR SRC TP",
                "description": "TOUR SRC objective description",
            }
        )
        sheet = cls.env["school_score_sheet"].create(
            {
                "academic_term_id": cls.term.id,
                "grade_class_id": cls.grade_class.id,
                "subject_id": cls.subject.id,
                "teacher_id": cls.teacher.id,
                "date": "2026-08-10",
                "user_id": cls.admin.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "enrollment_id": cls.enrollment.id,
                            "component_id": cls.component.id,
                            "score": 90.0,
                        },
                    )
                ],
                "component_ids": [
                    (
                        0,
                        0,
                        {
                            "component_id": cls.component.id,
                            "objective_ids": [(6, 0, [objective.id])],
                        },
                    )
                ],
            }
        )
        sheet = sheet.with_user(cls.admin)
        sheet.action_confirm()
        sheet.invalidate_cache()
        sheet.action_approve_approval()
        sheet.invalidate_cache()

    @classmethod
    def _confirm(cls, card):
        """Move a report card to Waiting for Approval through its action.

        :param card: the ``school_report_card`` record to confirm
        :return: nothing
        """
        card = card.with_user(cls.admin)
        card.action_confirm()
        card.invalidate_cache()

    def test_create(self):
        """Run the create tour for ``school_report_card``.

        IK: docs/school_report_card/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_report_card_create",
            login="admin",
        )

    def test_generate_lines(self):
        """Run the generate lines tour for ``school_report_card``.

        IK: docs/school_report_card/02-generate-lines.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_report_card_generate_lines",
            login="admin",
        )

    def test_compute_scores(self):
        """Run the compute scores tour for ``school_report_card``.

        IK: docs/school_report_card/03-compute-scores.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_report_card_compute_scores",
            login="admin",
        )

    def test_refill_learning_objective(self):
        """Run the refill learning objective tour for the report card.

        IK: docs/school_report_card/09-refill-learning-objective.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_report_card_refill_learning_objective",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_report_card``.

        IK: docs/school_report_card/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_report_card_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_report_card``.

        IK: docs/school_report_card/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_report_card_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_report_card``.

        IK: docs/school_report_card/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_report_card_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_report_card``.

        IK: docs/school_report_card/07-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_report_card_cancel",
            login="admin",
        )
