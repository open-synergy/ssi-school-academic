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
    The scores are entered in a student by component grid, which asks
    this model for its calculated columns and for the minimum score.
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
    minimum_score = fields.Float(
        string="Minimum Score",
        compute="_compute_minimum_score",
        store=False,
        compute_sudo=True,
        help="Minimum score (KKM) of the subject on the grade of the "
        "class. It is 0 when the subject has no minimum score for that "
        "grade. The score grid shows a score below it in red.",
    )

    @api.depends(
        "subject_id",
        "grade_id",
        "subject_id.minimum_score_ids.grade_id",
        "subject_id.minimum_score_ids.minimum_score",
    )
    def _compute_minimum_score(self):
        """Compute the minimum score of the subject on the grade.

        Looks for the minimum score line of the subject that belongs to
        the grade of the sheet; 0 when there is none.
        """
        for record in self:
            result = 0.0
            for line in record.subject_id.minimum_score_ids:
                if line.grade_id == record.grade_id:
                    result = line.minimum_score
            record.minimum_score = result

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

    @api.model
    def _get_score_grid_types(self):
        """Return the active report card types per term type.

        :return: ``{term_type: recordset}`` for ``mid_term`` and
            ``final``; a recordset holds every active type of that term
            type, so it is not exactly one record when the
            configuration is wrong.
        :rtype: dict
        """
        type_model = self.env["school_report_card_type"].sudo()
        result = {}
        for term_type in ("mid_term", "final"):
            result[term_type] = type_model.search([("term_type", "=", term_type)])
        return result

    @api.model
    def _get_score_grid_column_defs(self):
        """Return the definition of the three calculated grid columns.

        Extension point. The Average and the Final Score column use the
        active Final report card type, the Mid Score column the active
        Mid-Term one (the source of the Average is the Final type).

        :return: list of dicts, in the order ``average``, ``mid``,
            ``final``, with the keys ``key``, ``label``, ``types``
            (the active types of the column) and ``with_weights``
            (whether the weighted components are inputs too).
        :rtype: list
        """
        types = self._get_score_grid_types()
        return [
            {
                "key": "average",
                "label": _("Average"),
                "types": types["final"],
                "with_weights": False,
            },
            {
                "key": "mid",
                "label": _("Mid Score"),
                "types": types["mid_term"],
                "with_weights": True,
            },
            {
                "key": "final",
                "label": _("Final Score"),
                "types": types["final"],
                "with_weights": True,
            },
        ]

    @api.model
    def _get_score_grid_input_components(self, report_type, with_weights):
        """Return the components that feed a calculated grid column.

        :param report_type: the one ``school_report_card_type`` of the
            column
        :param bool with_weights: also take the weighted components,
            not only the averaged ones
        :return: the input components
        :rtype: recordset of ``school_score_component``
        """
        components = report_type.average_component_ids
        if with_weights:
            components |= report_type.weight_ids.mapped("component_id")
        return components

    @api.model
    def get_score_grid_layout(self):
        """Describe the calculated columns of the score grid.

        Each column sits right after its input component with the
        highest sequence. When the term type of the column has not
        exactly one active report card type, the column carries a
        warning, has no position (``after_component_id`` False, so the
        grid puts it at the far right) and stays empty.

        :return: list of dicts ``key``, ``label``,
            ``after_component_id`` and ``warning``, in the order
            ``average``, ``mid``, ``final``.
        :rtype: list
        """
        result = []
        for column in self._get_score_grid_column_defs():
            report_types = column["types"]
            warning = False
            after_component_id = False
            if len(report_types) != 1:
                warning = _(
                    "Exactly one active report card type of the term "
                    "type is needed for this column, but %s found."
                ) % (len(report_types),)
            else:
                components = self._get_score_grid_input_components(
                    report_types, column["with_weights"]
                )
                if components:
                    last = max(components, key=lambda c: (c.sequence, c.id))
                    after_component_id = last.id
            result.append(
                {
                    "key": column["key"],
                    "label": column["label"],
                    "after_component_id": after_component_id,
                    "warning": warning,
                }
            )
        return result

    @api.model
    def compute_score_grid(self, scores):
        """Compute the calculated columns of the score grid.

        The rules are the ones of the report card: the average is
        ``compute_average_score`` and the mid and final scores are
        ``compute_final_score`` of the active report card type. A
        column is None when its term type has not exactly one active
        report card type, or when the student has no score of an input
        component of the column; it is never 0 in that case.

        :param dict scores: ``{student_id: {component_id: score}}``
            with only the cells that were scored. Keys may be strings,
            as they come from JSON.
        :return: ``{student_id: {"average", "mid", "final"}}``
        :rtype: dict
        """
        columns = self._get_score_grid_column_defs()
        result = {}
        for student_key, component_scores in (scores or {}).items():
            parsed = {
                int(component_key): float(score)
                for component_key, score in (component_scores or {}).items()
            }
            row = {}
            for column in columns:
                row[column["key"]] = self._compute_score_grid_cell(column, parsed)
            result[int(student_key)] = row
        return result

    @api.model
    def _compute_score_grid_cell(self, column, scores):
        """Compute one calculated cell of the score grid.

        :param dict column: the column definition, see
            ``_get_score_grid_column_defs``
        :param dict scores: ``{component_id: score}`` of one student
        :return: the value, or None when the cell must stay empty.
        :rtype: float or None
        """
        report_types = column["types"]
        if len(report_types) != 1:
            return None
        components = self._get_score_grid_input_components(
            report_types, column["with_weights"]
        )
        entered = {
            component_id: score
            for component_id, score in scores.items()
            if component_id in components.ids
        }
        if not entered:
            return None
        if column["key"] == "average":
            return report_types.compute_average_score(entered)
        return report_types.compute_final_score(entered)

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
