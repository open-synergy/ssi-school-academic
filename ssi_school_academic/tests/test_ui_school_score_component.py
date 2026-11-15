# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolScoreComponent(HttpSavepointCase):
    """Tour tests for the ``school_score_component`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records required by the tours.

        Pre-Condition IK: the Score Components edited or archived by the
        tours already exist.
        """
        super().setUpClass()
        cls.component_edit = cls.env["school_score_component"].create(
            {
                "name": "TOUR Score Component Edit",
                "code": "/",
                "category": "daily_test",
            }
        )
        cls.component_archive = cls.env["school_score_component"].create(
            {
                "name": "TOUR Score Component Archive",
                "code": "/",
                "category": "assignment",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_score_component``.

        IK: docs/school_score_component/01-create.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_score_component_create", login="admin"
        )

    def test_edit(self):
        """Run the edit tour for ``school_score_component``.

        IK: docs/school_score_component/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_score_component_edit", login="admin"
        )

    def test_archive(self):
        """Run the archive tour for ``school_score_component``.

        IK: docs/school_score_component/03-archive.md
        """
        self.start_tour(
            "/web",
            "ssi_school_academic_school_score_component_archive",
            login="admin",
        )
