# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolScorePredicate(HttpSavepointCase):
    """Tour tests for the ``school_score_predicate`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records required by the tours.

        Pre-Condition IK: at least one Grade exists, and the Score
        Predicate edited or archived by the tours already exists with a
        line.
        """
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR Predicate Grade Type",
                "code": "/",
                "sequence": 10,
            }
        )
        cls.grade_create = cls.env["school_grade"].create(
            {
                "name": "TOUR Predicate Grade Create",
                "code": "/",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_edit = cls.env["school_grade"].create(
            {
                "name": "TOUR Predicate Grade Edit",
                "code": "/",
                "sequence": 20,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_archive = cls.env["school_grade"].create(
            {
                "name": "TOUR Predicate Grade Archive",
                "code": "/",
                "sequence": 30,
                "type_id": cls.grade_type.id,
            }
        )
        cls.env["school_score_predicate"].create(
            {
                "name": "TOUR Predicate Edit",
                "code": "/",
                "grade_ids": [(6, 0, [cls.grade_edit.id])],
                "line_ids": [(0, 0, {"name": "A", "min_score": 90.0})],
            }
        )
        cls.env["school_score_predicate"].create(
            {
                "name": "TOUR Predicate Archive",
                "code": "/",
                "grade_ids": [(6, 0, [cls.grade_archive.id])],
            }
        )

    def test_create(self):
        """Run the create tour for ``school_score_predicate``.

        IK: docs/school_score_predicate/01-create.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_score_predicate_create", login="admin"
        )

    def test_edit(self):
        """Run the edit tour for ``school_score_predicate``.

        IK: docs/school_score_predicate/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_score_predicate_edit", login="admin"
        )

    def test_archive(self):
        """Run the archive tour for ``school_score_predicate``.

        IK: docs/school_score_predicate/03-archive.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_score_predicate_archive", login="admin"
        )
