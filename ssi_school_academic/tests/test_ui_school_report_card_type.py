# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolReportCardType(HttpSavepointCase):
    """Tour tests for the ``school_report_card_type`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records required by the tours.

        Pre-Condition IK: the Score Components exist, and the Report
        Card Types edited or archived by the tours already exist with a
        valid configuration.
        """
        super().setUpClass()
        component_model = cls.env["school_score_component"]
        cls.component_uh = component_model.create(
            {"name": "TOUR RCT UH 1", "code": "/", "category": "daily_test"}
        )
        cls.component_task = component_model.create(
            {"name": "TOUR RCT Task 1", "code": "/", "category": "assignment"}
        )
        cls.component_pts = component_model.create(
            {"name": "TOUR RCT PTS", "code": "/", "category": "mid_term_exam"}
        )
        type_model = cls.env["school_report_card_type"]
        for name in ("TOUR Report Card Type Edit", "TOUR Report Card Type Archive"):
            type_model.create(
                {
                    "name": name,
                    "code": "/",
                    "term_type": "mid_term",
                    "average_weight": 70.0,
                    "average_component_ids": [
                        (6, 0, [cls.component_uh.id, cls.component_task.id])
                    ],
                    "weight_ids": [
                        (
                            0,
                            0,
                            {
                                "component_id": cls.component_pts.id,
                                "weight": 30.0,
                            },
                        )
                    ],
                }
            )

    def test_create(self):
        """Run the create tour for ``school_report_card_type``.

        IK: docs/school_report_card_type/01-create.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_report_card_type_create", login="admin"
        )

    def test_edit(self):
        """Run the edit tour for ``school_report_card_type``.

        IK: docs/school_report_card_type/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_report_card_type_edit", login="admin"
        )

    def test_archive(self):
        """Run the archive tour for ``school_report_card_type``.

        IK: docs/school_report_card_type/03-archive.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_report_card_type_archive",
            login="admin",
        )
