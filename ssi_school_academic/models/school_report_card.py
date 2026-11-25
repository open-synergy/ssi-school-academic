# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import format_date

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

    # Redeclare the state selection so that the translation entries of
    # the state values belong to this module. The values and labels are
    # identical with the mixins, only the module is recorded.
    state = fields.Selection(
        selection_add=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("reject", "Rejected"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        ondelete={
            "confirm": "set default",
            "reject": "set default",
            "done": "set default",
            "cancel": "set default",
        },
    )

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
    refill_learning_objective_ok = fields.Boolean(
        string="Can Refill Learning Objective",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help="Policy that determines whether the Refill Learning "
        "Objective button is visible.",
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

    def action_refill_learning_objective(self):
        """Overwrite the learning objective of every line.

        Builds the text again from the score sheets that are done and
        replaces what is on the lines, the text typed by hand included.
        The button is shown according to the
        ``refill_learning_objective_ok`` policy.

        :return: nothing
        """
        for record in self.sudo():
            record._refill_learning_objective()

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

        A line without any entered score is left not scored, with an
        empty final score, instead of getting a computed zero. The
        learning objective text is filled for the lines that have none;
        a text that is already there is never overwritten.

        :raises UserError: when the report card is not in draft state.
        :return: nothing
        """
        self.ensure_one()
        self._check_draft_state("Compute scores")
        for line in self.line_ids:
            component_scores = line._get_component_scores()
            if component_scores:
                line.write(
                    {
                        "is_scored": True,
                        "final_score": self.type_id.compute_final_score(
                            component_scores
                        ),
                    }
                )
            else:
                line.write({"is_scored": False, "final_score": False})
        self.line_ids._refill_learning_objective(False)

    def _refill_learning_objective(self):
        """Overwrite the learning objective of every line.

        :raises UserError: when the report card is not in draft state.
        :return: nothing
        """
        self.ensure_one()
        self._check_draft_state("Refill learning objective")
        self.line_ids._refill_learning_objective(True)

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

    def get_report_card_print_data(self):
        """Return the data the report card print template needs.

        Called by the py3o template of the report card. The first
        statement checks the Viewer group, because the read access of
        the model is granted to every user and the report route does
        not check the groups of the report. The returned dict holds the
        translated static ``labels``, the ``header`` values, the
        ``component_count`` and ``component_headers`` of the printed
        score columns (none for a final report card), the subject
        ``groups`` with their rows, and the blocks that are
        ``False`` when empty (``co_curricular``, ``extracurricular``,
        ``homeroom_note`` and ``parent_response``).

        :raises AccessError: when the user is not in the Viewer group
            of the report card.
        :return: dict ready to print
        :rtype: dict
        """
        self.ensure_one()
        group = "ssi_school_academic.school_report_card_viewer_group"
        if not self.env.user.has_group(group):
            error_message = (
                _(
                    """
Document Type: %s
Context: Print report card
Database ID: %s
Problem: You are not allowed to print this report card
Solution: Ask the administrator to add you to the report card Viewer group
"""
                )
                % (self._description, self.id)
            )
            raise AccessError(error_message)
        record = self.sudo()
        card_type = record.type_id
        show_components = card_type.term_type == "mid_term"
        columns = card_type.print_column_ids
        if not show_components:
            columns = columns.browse()
        components = columns.mapped("component_id")
        enrollment = record.enrollment_id
        student = record.student_id
        teacher = record.homeroom_id.teacher_id
        grade_class = record.grade_class_id
        labels = record._get_print_labels()
        if show_components:
            period = labels["mid_term_semester"]
        else:
            period = labels["semester"]
        return {
            "labels": labels,
            "period": period,
            "show_components": show_components,
            "component_count": len(columns),
            "component_headers": [
                column.print_title or column.component_id.name or ""
                for column in columns
            ],
            "header": {
                "student_name": student.name or "",
                "nis": student.code or "",
                "nisn": student.contact_id.nisn or "",
                "school": enrollment.school_id.name or "",
                "school_address": record._get_print_school_address(),
                "program": grade_class.expertise_program or "",
                "concentration": grade_class.expertise_concentration or "",
                "class_name": grade_class.name or "",
                "phase": record.grade_id.phase or "",
                "academic_year": record.academic_year_id.name or "",
                "term": record.academic_term_id.name or "",
            },
            "footer": " | ".join(
                [grade_class.name or "", student.name or "", student.code or ""]
            ),
            "groups": record._get_print_groups(components, show_components),
            "co_curricular": [
                {"theme": item.theme or "", "description": item.description or ""}
                for item in record.co_curricular_ids
            ]
            or False,
            "extracurricular": [
                {
                    "no": str(index),
                    "name": item.name or "",
                    "description": item.description or "",
                }
                for index, item in enumerate(record.extracurricular_ids, start=1)
            ]
            or False,
            "absence": {
                "sick": str(record.sick_days),
                "permission": str(record.permission_days),
                "absent": str(record.absent_days),
            },
            "homeroom_note": record.homeroom_note or False,
            "parent_response": record.parent_response or False,
            "print_city": record.print_city or "",
            "print_date": format_date(self.env, record.print_date),
            "homeroom_name": teacher.name or "",
            "homeroom_nuptk": teacher.nuptk or "",
        }

    def _get_print_school_address(self):
        """Return the address of the school of the enrollment.

        :return: address of the school contact on one line, empty when
            the school has no contact
        :rtype: str
        """
        self.ensure_one()
        partner = self.enrollment_id.school_id.partner_id
        if not partner:
            return ""
        address = partner._display_address(without_company=True)
        return ", ".join(part for part in address.split("\n") if part.strip())

    @api.model
    def _format_print_score(self, score):
        """Format a score without a useless decimal part.

        :param float score: the score to print
        :return: text such as ``87`` or ``85.5``
        :rtype: str
        """
        return "%g" % score

    def _get_print_groups(self, components, show_components):
        """Build the subject groups and rows of the printed table.

        Rows are grouped by subject group, General first and then
        Vocational, and ordered by the subject name. A group without a
        row is left out. A component the subject has no score for is
        printed as ``-``. A row that is not scored prints ``-`` as its
        final score and as its learning objective when that is empty.

        :param components: score components of the printed columns, in
            column order; empty when no component column is printed
        :param bool show_components: whether the component columns
            are printed
        :return: list of ``{"title": str, "rows": [dict]}``
        :rtype: list
        """
        self.ensure_one()
        labels = self._get_print_labels()
        titles = [
            ("general", labels["general"]),
            ("vocational", labels["vocational"]),
        ]
        result = []
        for group_key, title in titles:
            lines = self.line_ids.filtered(
                lambda line, key=group_key: line.subject_group == key
            ).sorted(lambda line: line.subject_id.name or "")
            rows = []
            for index, line in enumerate(lines, start=1):
                scores = [""] * len(components)
                if show_components:
                    component_scores = line._get_component_scores()
                    for position, component in enumerate(components):
                        if component.id in component_scores:
                            scores[position] = self._format_print_score(
                                component_scores[component.id]
                            )
                        else:
                            scores[position] = "-"
                if line.is_scored:
                    final = self._format_print_score(line.final_score)
                    objective = line.learning_objective or ""
                else:
                    final = "-"
                    objective = line.learning_objective or "-"
                rows.append(
                    {
                        "no": str(index),
                        "subject": line.subject_id.name or "",
                        "scores": scores,
                        "final": final,
                        "objective": objective,
                    }
                )
            if rows:
                result.append({"title": title, "rows": rows})
        return result

    @api.model
    def _get_print_labels(self):
        """Return every static text of the printed report card.

        The texts are English and translated here, so they reach the
        ``.pot`` file instead of being typed into the template.

        :return: label per key
        :rtype: dict
        """
        return {
            "title": _("Learning Result Report"),
            "mid_term_semester": _("Mid-Term Semester"),
            "semester": _("Semester"),
            "name": _("Name"),
            "nis": _("Student ID (NIS)"),
            "nisn": _("National Student ID (NISN)"),
            "school": _("School Name"),
            "address": _("Address"),
            "program": _("Expertise Program"),
            "concentration": _("Expertise Concentration"),
            "class": _("Class"),
            "phase": _("Phase"),
            "academic_year": _("Academic Year"),
            "general": _("General Subjects"),
            "vocational": _("Vocational Subjects"),
            "no": _("No."),
            "subject": _("Subject"),
            "final": _("Final Score"),
            "achievement": _("Competency Achievement"),
            "co_curricular": _("Co-Curricular"),
            "extracurricular": _("Extracurricular"),
            "activity": _("Activity"),
            "description": _("Description"),
            "absence": _("Absences"),
            "sick": _("Sick"),
            "permission": _("Permission"),
            "absent": _("Without Reason"),
            "homeroom_note": _("Homeroom Teacher Note"),
            "parent_response": _("Parent Response"),
            "parent": _("Parent / Guardian"),
            "homeroom": _("Homeroom Teacher"),
            "nuptk": _("NUPTK"),
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
            "refill_learning_objective_ok",
        ]
        res += policy_field
        return res
