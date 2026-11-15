# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolScoreSheet(models.Model):
    """Represents the scores a teacher gives for one subject.

    A score sheet is a transaction document for one subject, one grade
    class and one academic term. The teacher generates the lines from
    the open enrollments of the class: one line per enrollment and per
    active score component. The teacher then fills in the scores, and
    the sheet becomes final once it is confirmed and approved. The
    scores of a finished sheet are the source of the final report card
    score. Scores may only be entered for enrollments that are open.
    """

    _name = "school_score_sheet"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
    ]
    _description = "School Score Sheet"
    _order = "date desc, id desc"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    date = fields.Date(
        string="Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Date of this score sheet. It is also the date the "
        "document number is generated from.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Academic term the scores belong to. Only enrollments of "
        "this term are offered when the lines are generated.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        related="academic_term_id.year_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Academic year of the selected Academic Term.",
    )
    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Grade class the scores are given to. Only enrollments of "
        "this class are offered when the lines are generated.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        related="grade_class_id.grade_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Grade of the selected Grade Class. It decides which "
        "subjects can be chosen.",
    )
    subject_id = fields.Many2one(
        string="Subject",
        comodel_name="school_subject",
        required=True,
        ondelete="restrict",
        readonly=True,
        domain="[('grade_ids', '=', grade_id)]",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Subject the scores are given for. Only subjects taught "
        "in the Grade of the Grade Class can be chosen.",
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Teacher who gives the scores of this sheet.",
    )
    line_ids = fields.One2many(
        string="Lines",
        comodel_name="school_score_sheet_line",
        inverse_name="sheet_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Score lines, one per enrollment and per score component.",
    )
    generate_lines_ok = fields.Boolean(
        string="Can Generate Lines",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Generate Lines " "button is visible.",
    )

    @api.constrains(
        "academic_term_id",
        "grade_class_id",
        "subject_id",
        "state",
    )
    def _check_unique_sheet(self):
        """Check that only one live sheet exists per subject.

        A score sheet that is not cancelled is the only one allowed for
        the same academic term, grade class and subject.

        :raises ValidationError: when another sheet that is not
            cancelled exists for the same term, class and subject.
        """
        for record in self:
            if record.state == "cancel":
                continue
            domain = [
                ("id", "!=", record.id),
                ("state", "!=", "cancel"),
                ("academic_term_id", "=", record.academic_term_id.id),
                ("grade_class_id", "=", record.grade_class_id.id),
                ("subject_id", "=", record.subject_id.id),
            ]
            if self.search_count(domain):
                error_message = (
                    _(
                        """
Context: Save score sheet
Database ID: %s
Problem: A score sheet already exists for this subject, class, and term.
Solution: Open the existing score sheet, or cancel it before creating a new one
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    def action_generate_lines(self):
        """Fill the lines from the open enrollments of the class.

        Replaces every line of the sheet with one line per open
        enrollment and per active score component. The button is shown
        according to the ``generate_lines_ok`` policy.

        :return: nothing
        """
        for record in self.sudo():
            record._generate_lines()

    def _generate_lines(self):
        """Replace the lines with enrollment by component lines.

        :raises UserError: when the sheet is not in draft state.
        :return: nothing
        """
        self.ensure_one()
        if self.state != "draft":
            error_message = (
                _(
                    """
Document Type: %s
Context: Generate lines
Database ID: %s
Problem: Lines can only be generated in draft state
Solution: Restart the document before generating the lines
"""
                )
                % (self._description, self.id)
            )
            raise UserError(error_message)
        self.line_ids.unlink()
        enrollments = self.env["school_enrollment"].search(
            self._get_enrollment_domain()
        )
        components = self.env["school_score_component"].search(
            self._get_component_domain(), order="sequence, id"
        )
        values = []
        for enrollment in enrollments:
            for component in components:
                values.append(self._prepare_line_values(enrollment, component))
        self.env["school_score_sheet_line"].create(values)

    def _get_enrollment_domain(self):
        """Return the domain of the enrollments that get a line.

        Extension point: only open enrollments of the same grade class
        and academic term as the sheet are taken.

        :return: domain for ``school_enrollment``
        """
        self.ensure_one()
        return [
            ("state", "=", "open"),
            ("grade_class_id", "=", self.grade_class_id.id),
            ("academic_term_id", "=", self.academic_term_id.id),
        ]

    def _get_component_domain(self):
        """Return the domain of the score components that get a line.

        Extension point: only active score components are taken.

        :return: domain for ``school_score_component``
        """
        self.ensure_one()
        return [("active", "=", True)]

    def _prepare_line_values(self, enrollment, component):
        """Build the values of one score line.

        Extension point. The score is left out on purpose, so the line
        stays not yet scored.

        :param enrollment: the ``school_enrollment`` of the line
        :param component: the ``school_score_component`` of the line
        :return: dict of ``school_score_sheet_line`` values
        """
        self.ensure_one()
        return {
            "sheet_id": self.id,
            "enrollment_id": enrollment.id,
            "component_id": component.id,
        }

    @ssi_decorator.pre_confirm_check()
    def _01_check_open_enrollment(self):
        """Check that every line belongs to an open enrollment.

        An enrollment may have left the open state after the line was
        added, so the rule of the line is checked again on confirm.

        :raises ValidationError: when a line belongs to an enrollment
            that is not open.
        """
        self.ensure_one()
        self.line_ids._check_enrollment_open()

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "manual_number_ok",
            "generate_lines_ok",
        ]
        res += policy_field
        return res
