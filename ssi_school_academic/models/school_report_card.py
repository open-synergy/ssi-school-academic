# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolReportCard(models.Model):
    """Represents the report card of one student for one term.

    A report card is a transaction document for one open enrollment and
    one report card type, for example Mid-Term or Final. The homeroom
    teacher generates one line per subject of the grade, computes the
    final scores from the score sheets that are done, fills in the
    manual parts (co-curricular, extracurricular, absences and notes)
    and finishes the document through approval. A finished report card
    is only read and printed again, even after the enrollment is done.
    """

    _name = "school_report_card"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
    ]
    _description = "School Report Card"
    _order = "print_date desc, id desc"

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

    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        required=True,
        ondelete="restrict",
        domain="[('state', '=', 'open')]",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Open enrollment of the student the report card is for. "
        "The report card of an enrollment that is done is still read "
        "and printed.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        related="enrollment_id.student_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Student of the selected Enrollment.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        related="enrollment_id.academic_year_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Academic year of the selected Enrollment.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        related="enrollment_id.academic_term_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Academic term of the selected Enrollment. The scores come "
        "from the score sheets of this term.",
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        related="enrollment_id.grade_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Grade of the selected Enrollment. It decides which "
        "subjects get a line.",
    )
    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        related="enrollment_id.grade_class_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Grade class of the selected Enrollment.",
    )
    homeroom_id = fields.Many2one(
        string="Homeroom",
        comodel_name="school_homeroom",
        related="enrollment_id.homeroom_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help="Homeroom of the selected Enrollment.",
    )
    type_id = fields.Many2one(
        string="Report Card Type",
        comodel_name="school_report_card_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Kind of report card, for example Mid-Term or Final. It "
        "decides how the final score of every subject is computed.",
    )
    sick_days = fields.Integer(
        string="Sick Days",
        default=0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Number of days the student was absent because of sickness.",
    )
    permission_days = fields.Integer(
        string="Permission Days",
        default=0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Number of days the student was absent with permission.",
    )
    absent_days = fields.Integer(
        string="Absent Days",
        default=0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Number of days the student was absent without a reason.",
    )
    homeroom_note = fields.Text(
        string="Homeroom Teacher Note",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Note of the homeroom teacher printed on the report card.",
    )
    parent_response = fields.Text(
        string="Parent Response",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Response of the parent or guardian printed on the report " "card.",
    )
    print_city = fields.Char(
        string="Print City",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="City printed next to the signature date.",
    )
    print_date = fields.Date(
        string="Print Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Date printed next to the signature. It is also the date "
        "the document number is generated from.",
    )
    line_ids = fields.One2many(
        string="Subject Lines",
        comodel_name="school_report_card_line",
        inverse_name="report_card_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Final score of the student, one line per subject.",
    )
    co_curricular_ids = fields.One2many(
        string="Co-Curriculars",
        comodel_name="school_report_card_co_curricular",
        inverse_name="report_card_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Co-curricular themes written by hand.",
    )
    extracurricular_ids = fields.One2many(
        string="Extracurriculars",
        comodel_name="school_report_card_extracurricular",
        inverse_name="report_card_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Extracurricular activities written by hand.",
    )
    generate_lines_ok = fields.Boolean(
        string="Can Generate Lines",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Generate Lines button " "is visible.",
    )
    compute_scores_ok = fields.Boolean(
        string="Can Compute Scores",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Compute Scores button " "is visible.",
    )

    @api.constrains("enrollment_id")
    def _constrains_enrollment_open(self):
        """Check that a report card is made for an open enrollment.

        Runs when the enrollment is set or changed, so the report card
        of an enrollment that later becomes done stays openable.

        :raises ValidationError: when the enrollment is not open.
        """
        self._check_enrollment_open()

    @api.constrains("enrollment_id", "type_id", "state")
    def _check_unique_report_card(self):
        """Check that only one live report card exists per type.

        A report card that is not cancelled is the only one allowed for
        the same enrollment and report card type.

        :raises ValidationError: when another report card that is not
            cancelled exists for the same enrollment and type.
        """
        for record in self:
            if record.state == "cancel":
                continue
            domain = [
                ("id", "!=", record.id),
                ("state", "!=", "cancel"),
                ("enrollment_id", "=", record.enrollment_id.id),
                ("type_id", "=", record.type_id.id),
            ]
            if self.search_count(domain):
                error_message = (
                    _(
                        """
Context: Save report card
Database ID: %s
Problem: A report card already exists for this enrollment and report card type.
Solution: Open the existing report card, or cancel it before creating a new one
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("sick_days", "permission_days", "absent_days")
    def _check_absence_days(self):
        """Check that no absence day count is negative.

        :raises ValidationError: when a count of days is below 0.
        """
        for record in self:
            if min(record.sick_days, record.permission_days, record.absent_days) < 0:
                error_message = (
                    _(
                        """
Context: Save report card
Database ID: %s
Problem: Absence days cannot be negative.
Solution: Enter 0 or a positive number of days
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    def _check_enrollment_open(self):
        """Raise when a report card belongs to an enrollment not open.

        Shared by the constraint on the enrollment and by the check on
        confirm, so both apply the same rule.

        :raises ValidationError: when the enrollment is not open.
        """
        for record in self:
            if record.enrollment_id.state != "open":
                error_message = (
                    _(
                        """
Context: Check report card
Database ID: %s
Problem: Report cards may only be created for open enrollments.
Solution: Select an enrollment that is open
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    def action_generate_lines(self):
        """Fill the lines with one line per subject and compute them.

        Replaces every line of the report card with one line per active
        subject taught in the grade, then fills the final scores. The
        button is shown according to the ``generate_lines_ok`` policy.

        :return: nothing
        """
        for record in self.sudo():
            record._generate_lines()

    def action_compute_scores(self):
        """Fill the final score of every line from the score sheets.

        The button is shown according to the ``compute_scores_ok``
        policy.

        :return: nothing
        """
        for record in self.sudo():
            record._compute_scores()

    def _check_draft_state(self, context):
        """Raise when the report card is not in draft state.

        :param str context: name of the action, used in the message.
        :raises UserError: when the report card is not in draft state.
        """
        self.ensure_one()
        if self.state != "draft":
            error_message = (
                _(
                    """
Document Type: %s
Context: %s
Database ID: %s
Problem: This action is only allowed in draft state
Solution: Restart the document before running this action
"""
                )
                % (self._description, context, self.id)
            )
            raise UserError(error_message)

    def _generate_lines(self):
        """Replace the lines by one line per subject, then compute.

        :raises UserError: when the report card is not in draft state.
        :return: nothing
        """
        self.ensure_one()
        self._check_draft_state("Generate lines")
        self.line_ids.unlink()
        subjects = self.env["school_subject"].search(self._get_subject_domain())
        self.env["school_report_card_line"].create(
            [self._prepare_line_values(subject) for subject in subjects]
        )
        self._compute_scores()

    def _compute_scores(self):
        """Fill the final score of every line.

        :raises UserError: when the report card is not in draft state.
        :return: nothing
        """
        self.ensure_one()
        self._check_draft_state("Compute scores")
        for line in self.line_ids:
            line.final_score = self.type_id.compute_final_score(
                line._get_component_scores()
            )

    def _get_subject_domain(self):
        """Return the domain of the subjects that get a line.

        Extension point: only active subjects taught in the grade of
        the report card are taken.

        :return: domain for ``school_subject``
        """
        self.ensure_one()
        return [("grade_ids", "in", self.grade_id.ids)]

    def _prepare_line_values(self, subject):
        """Build the values of one subject line.

        Extension point. The final score is left out on purpose; the
        compute scores action fills it.

        :param subject: the ``school_subject`` of the line
        :return: dict of ``school_report_card_line`` values
        """
        self.ensure_one()
        return {
            "report_card_id": self.id,
            "subject_id": subject.id,
        }

    @ssi_decorator.pre_confirm_check()
    def _01_check_open_enrollment(self):
        """Check that the enrollment is still open on confirm.

        An enrollment may have left the open state after the report
        card was created, so the rule is checked again on confirm.

        :raises ValidationError: when the enrollment is not open.
        """
        self.ensure_one()
        self._check_enrollment_open()

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
            "compute_scores_ok",
        ]
        res += policy_field
        return res
