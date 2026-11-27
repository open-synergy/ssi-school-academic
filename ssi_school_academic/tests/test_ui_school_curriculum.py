# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 only SavepointCase prepares
# ``cls.env`` in ``setUpClass``, which is where every work instruction
# Pre-Condition below is built.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolCurriculum(HttpSavepointCase):
    """Tour tests for the ``school_curriculum`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the master data and one curriculum per tour.

        ``base.user_admin`` belongs to the validator and the "All" data
        ownership groups of ``school_curriculum``, so it can run every
        tour below and sees every fixture. Each curriculum gets an
        explicit ``user_id`` so that the internal user record rule
        cannot hide it from the tour session, and its own school so that
        the one-open-curriculum rule never links two tours.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Pre-Condition 01-create.md: the school, academic year, subject
        # and grade the tour picks from the dropdowns already exist.
        cls._create_structure("Create")

        # Pre-Condition 10-cancel.md: a reason exists and is global, so
        # the wizard lists it whatever the demo data holds.
        cls.cancel_reason = (
            cls.env["base.cancel_reason"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "Tour CU Cancel Reason",
                    "code": "TOURCUCR",
                    "global_use": True,
                }
            )
        )

        # Pre-Condition 04-confirm.md: Draft.
        cls.curriculum_confirm = cls._create_curriculum("Confirm")

        # Pre-Condition 05-approve.md and 06-reject.md: Waiting for
        # Approval, with ``admin`` among the active approvers.
        cls.curriculum_approve = cls._create_curriculum("Approve")
        cls._run_transition(cls.curriculum_approve, "action_confirm")
        cls.curriculum_reject = cls._create_curriculum("Reject")
        cls._run_transition(cls.curriculum_reject, "action_confirm")

        # Pre-Condition 09-finish.md: On Progress, reached by approving
        # a confirmed curriculum (the approval opens it automatically).
        cls.curriculum_finish = cls._create_curriculum("Finish")
        cls._run_transition(cls.curriculum_finish, "action_confirm")
        cls._run_transition(cls.curriculum_finish, "action_approve_approval")

        # Pre-Condition 10-cancel.md: Draft, one of the states the
        # cancel policy allows.
        cls.curriculum_cancel = cls._create_curriculum("Cancel")

        # Pre-Condition 12-restart.md: Rejected.
        cls.curriculum_restart = cls._create_curriculum("Restart")
        cls._run_transition(cls.curriculum_restart, "action_confirm")
        cls._run_transition(cls.curriculum_restart, "action_reject_approval")

    @classmethod
    def _create_structure(cls, label):
        """Create the school, year, grade and subject of a scenario.

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
        subject = env["school_subject"].create(
            {
                "name": "TOUR %s Subject" % label,
                "code": "/",
                "grade_ids": [(6, 0, [grade.id])],
            }
        )
        return {"school": school, "year": year, "grade": grade, "subject": subject}

    @classmethod
    def _create_curriculum(cls, label):
        """Create one Draft curriculum dedicated to a single tour.

        :param label: short scenario name, e.g. ``"Confirm"``
        :return: the new ``school_curriculum`` record, in Draft, whose
            title is the key the tour uses to find its row
        """
        structure = cls._create_structure(label)
        return (
            cls.env["school_curriculum"]
            .with_user(cls.admin)
            .create(
                {
                    "title": "Tour CU %s Curriculum" % label,
                    "school_id": structure["school"].id,
                    "academic_year_id": structure["year"].id,
                    "effective_start": "2026-07-01",
                    "effective_end": "2027-06-30",
                    "user_id": cls.admin.id,
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "subject_id": structure["subject"].id,
                                "grade_id": structure["grade"].id,
                                "weekly_hours": 4,
                                "total_class": 3,
                            },
                        ),
                    ],
                }
            )
        )

    @classmethod
    def _run_transition(cls, curriculum, method):
        """Advance a fixture curriculum through one workflow method.

        The policy fields guarding each button are computed from
        ``policy.template`` against the state written by the previous
        transition, so the cache is dropped before every call.

        :param curriculum: the ``school_curriculum`` record to advance
        :param method: name of the workflow method, e.g.
            ``"action_confirm"``
        """
        curriculum.invalidate_cache()
        getattr(curriculum.with_user(cls.admin), method)()
        curriculum.invalidate_cache()

    def test_create(self):
        """Run the create tour for ``school_curriculum``.

        IK: docs/school_curriculum/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_curriculum_create",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_curriculum``.

        IK: docs/school_curriculum/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_curriculum_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_curriculum``.

        IK: docs/school_curriculum/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_curriculum_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_curriculum``.

        IK: docs/school_curriculum/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_curriculum_reject",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``school_curriculum``.

        IK: docs/school_curriculum/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_curriculum_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_curriculum``.

        IK: docs/school_curriculum/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_curriculum_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_curriculum``.

        IK: docs/school_curriculum/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_curriculum_restart",
            login="admin",
        )
