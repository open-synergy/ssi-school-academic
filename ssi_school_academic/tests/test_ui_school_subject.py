# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolSubject(HttpSavepointCase):
    """Tour tests for the ``school_subject`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records required by the tours.

        Pre-Condition IK: at least one Grade exists, and the Subject
        edited or archived by the tours already exists with a minimum
        score line.
        """
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR Subject Grade Type",
                "code": "/",
                "sequence": 10,
            }
        )
        cls.grade_create = cls.env["school_grade"].create(
            {
                "name": "TOUR Subject Grade Create",
                "code": "/",
                "sequence": 10,
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_edit = cls.env["school_grade"].create(
            {
                "name": "TOUR Subject Grade Edit",
                "code": "/",
                "sequence": 20,
                "type_id": cls.grade_type.id,
            }
        )
        cls.subject_edit = cls.env["school_subject"].create(
            {
                "name": "TOUR Subject Edit",
                "code": "/",
                "grade_ids": [(6, 0, [cls.grade_edit.id])],
            }
        )
        cls.env["school_subject_minimum_score"].create(
            {
                "subject_id": cls.subject_edit.id,
                "grade_id": cls.grade_edit.id,
                "minimum_score": 70.0,
            }
        )
        cls.env["school_subject"].create(
            {
                "name": "TOUR Subject Archive",
                "code": "/",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_subject``.

        IK: docs/school_subject/01-create.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_subject_create", login="admin"
        )

    def test_edit(self):
        """Run the edit tour for ``school_subject``.

        IK: docs/school_subject/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_subject_edit", login="admin"
        )

    def test_archive(self):
        """Run the archive tour for ``school_subject``.

        IK: docs/school_subject/03-archive.md
        """
        self.start_tour(
            "/web", "ssi_school_academic_school_subject_archive", login="admin"
        )
