# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0, HttpCase does not set up
# cls.env in setUpClass, so fixtures written there would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolSubjectOutcome(HttpSavepointCase):
    """Tour tests for the ``school_subject_outcome`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the master data the create tour picks from.

        Pre-Condition IK: the Subject, the Grade and the Academic Term
        of the outcome already exist.
        """
        super().setUpClass()
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR SSO Grade Type", "code": "/"}
        )
        year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR SSO Year",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        cls.env["school_academic_term"].create(
            {
                "name": "TOUR SSO Term",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": year.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {"name": "TOUR SSO Grade", "code": "/", "type_id": grade_type.id}
        )
        cls.env["school_subject"].create(
            {
                "name": "TOUR SSO Subject",
                "code": "/",
                "grade_ids": [(6, 0, [grade.id])],
            }
        )

    def test_create(self):
        """Run the create tour for ``school_subject_outcome``.

        IK: docs/school_subject_outcome/01-create.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_subject_outcome_create", login="admin"
        )
