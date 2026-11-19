# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolReportCardMainSubject(HttpSavepointCase):
    """Tour tests for the ``school_report_card_main_subject`` instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records required by the tours.

        Pre-Condition IK: the grade and the subjects chosen by the create
        tour exist.
        """
        super().setUpClass()
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR RCMS Grade Type", "code": "/"}
        )
        cls.grade = cls.env["school_grade"].create(
            {"name": "TOUR RCMS Grade", "code": "/", "type_id": grade_type.id}
        )
        cls.subject = cls.env["school_subject"].create(
            {"name": "TOUR RCMS Subject", "code": "/", "subject_group": "vocational"}
        )

    def test_create(self):
        """Run the create tour for ``school_report_card_main_subject``.

        IK: docs/school_report_card_main_subject/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_report_card_main_subject_create",
            login="admin",
        )
