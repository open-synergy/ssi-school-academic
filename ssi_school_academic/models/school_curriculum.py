# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolCurriculum(models.Model):
    """Represents the curriculum of one school for one academic year.

    A curriculum is a transaction document that lists, per subject and
    per grade, the weekly hours (JP) and the number of classes the
    school runs. It is made in draft, confirmed, approved and thereby
    opened, and finished when it is no longer in force. A school has
    at most one curriculum that is not cancelled per academic year,
    and at most one curriculum that is open at the same time. The
    header and the lines can only be changed while the curriculum is in
    draft.
    """

    _name = "school_curriculum"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Curriculum"
    _order = "school_id, effective_start desc, id desc"

    # Multiple approval attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_button = False
    _automatically_insert_open_policy_fields = False
    _automatically_insert_multiple_approval_page = True

    # Attributes related to add element on form view automatically
    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    # Fields that can only be written while the curriculum is draft.
    _draft_only_fields = [
        "title",
        "school_id",
        "academic_year_id",
        "effective_start",
        "effective_end",
        "line_ids",
    ]

    # Redeclare the state selection so that the translation entries of
    # the state values belong to this module. The values and labels are
    # identical with the mixins, only the module is recorded.
    state = fields.Selection(
        selection_add=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("reject", "Rejected"),
            ("open", "On Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        ondelete={
            "confirm": "set default",
            "reject": "set default",
            "open": "set default",
            "done": "set default",
            "cancel": "set default",
        },
    )

    title = fields.Char(
        string="Title",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Name of the curriculum, for example the curriculum year or "
        "the name of the national curriculum.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="School the curriculum is run in.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Academic year the curriculum is made for. A school can "
        "have only one curriculum that is not cancelled per academic "
        "year.",
    )
    effective_start = fields.Date(
        string="Effective Start",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="First date the curriculum is in force. It is also the "
        "date the document number is generated from.",
    )
    effective_end = fields.Date(
        string="Effective End",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Last date the curriculum is in force. It cannot be "
        "earlier than the effective start.",
    )
    line_ids = fields.One2many(
        string="Lines",
        comodel_name="school_curriculum_line",
        inverse_name="curriculum_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=True,
        help="Weekly hours and number of classes per subject and " "grade.",
    )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super(SchoolCurriculum, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def write(self, vals):
        """Write the curriculum and refuse changes outside draft.

        :param dict vals: values to write.
        :return: True
        :rtype: bool
        :raises ValidationError: when a field that is only editable in
            draft is written on a curriculum that is not draft.
        """
        if any(field in vals for field in self._draft_only_fields):
            for record in self.filtered(lambda r: r.state != "draft"):
                record._raise_not_draft()
        return super().write(vals)

    def _raise_not_draft(self):
        """Raise the error of a change outside draft.

        :raises ValidationError: always.
        """
        self.ensure_one()
        error_message = (
            _(
                """
Document: School Curriculum
Context: Change curriculum
Database ID: %s
Problem: The curriculum can only be changed in draft state.
Solution: Restart the document before changing it
"""
            )
            % (self.id,)
        )
        raise ValidationError(error_message)

    @api.constrains("effective_start", "effective_end")
    def _check_effective_dates(self):
        """Check that the effective period is not reversed.

        :raises ValidationError: when the effective start is later
            than the effective end.
        """
        for record in self:
            if record.effective_start > record.effective_end:
                error_message = (
                    _(
                        """
Document: School Curriculum
Context: Save curriculum
Database ID: %s
Problem: Effective start cannot be later than effective end.
Solution: Correct the effective dates
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("school_id", "academic_year_id", "state")
    def _check_unique_school_year(self):
        """Check that a school has one curriculum per academic year.

        Cancelled curriculums are not counted. The search ignores the
        record rules, so a curriculum of another user is counted too.

        :raises ValidationError: when another curriculum that is not
            cancelled exists for the same school and academic year.
        """
        for record in self.filtered(lambda r: r.state != "cancel"):
            domain = [
                ("id", "!=", record.id),
                ("school_id", "=", record.school_id.id),
                ("academic_year_id", "=", record.academic_year_id.id),
                ("state", "!=", "cancel"),
            ]
            if self.sudo().search_count(domain):
                error_message = (
                    _(
                        """
Document: School Curriculum
Context: Save curriculum
Database ID: %s
Problem: The school already has a curriculum for this academic year.
Solution: Cancel the other curriculum or choose another academic year
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("school_id", "state")
    def _check_single_open(self):
        """Check that a school has one open curriculum at a time.

        The search ignores the record rules, so an open curriculum of
        another user is counted too.

        :raises ValidationError: when another curriculum of the same
            school is already open.
        """
        for record in self.filtered(lambda r: r.state == "open"):
            domain = [
                ("id", "!=", record.id),
                ("school_id", "=", record.school_id.id),
                ("state", "=", "open"),
            ]
            if self.sudo().search_count(domain):
                error_message = (
                    _(
                        """
Document: School Curriculum
Context: Open curriculum
Database ID: %s
Problem: The school already has a curriculum that is on progress.
Solution: Finish or cancel the open curriculum first
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
