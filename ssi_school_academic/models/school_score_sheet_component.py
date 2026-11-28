# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolScoreSheetComponent(models.Model):
    """Represents one score column of a score sheet.

    A record links a score sheet to one score component, of any
    category, that has lines on the sheet. It holds the lock of the
    column, and for a daily test or an assignment also the learning
    objectives (TP) the column measures. A teacher locks a column when
    its scores are final; a locked column cannot be changed until it is
    unlocked, and the report card reads it without waiting for the
    sheet to be done. The objectives must belong to the learning
    outcome of the subject, the grade and the academic term of the
    sheet.
    """

    _name = "school_score_sheet_component"
    _description = "School Score Sheet Component"
    _order = "sheet_id, component_id"

    sheet_id = fields.Many2one(
        string="Score Sheet",
        comodel_name="school_score_sheet",
        required=True,
        ondelete="cascade",
        help="Score sheet this component belongs to.",
    )
    component_id = fields.Many2one(
        string="Score Component",
        comodel_name="school_score_component",
        required=True,
        ondelete="restrict",
        help="Score component of the sheet, for example Daily Test 1.",
    )
    is_locked = fields.Boolean(
        string="Locked",
        default=False,
        readonly=True,
        help="Set when the teacher locked the column. The scores of a "
        "locked column cannot be changed, and the report card reads "
        "them. It is changed only by the Lock Column and Unlock Column "
        "buttons, which follow the policy of the score sheet.",
    )
    objective_ids = fields.Many2many(
        string="Learning Objectives",
        comodel_name="school_subject_outcome_objective",
        relation="school_score_sheet_component_objective_rel",
        column1="sheet_component_id",
        column2="objective_id",
        help="Learning objectives (TP) this component measures. Only "
        "objectives of the subject, the grade and the academic term of "
        "the score sheet can be chosen.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Create columns, refusing a lock that bypasses the buttons.

        :param list vals_list: values of the columns to create.
        :return: the new columns.
        :rtype: recordset of ``school_score_sheet_component``
        :raises UserError: when a value sets ``is_locked`` outside the
            lock context.
        """
        for vals in vals_list:
            if vals.get("is_locked"):
                self._check_lock_context()
        return super().create(vals_list)

    def write(self, vals):
        """Write columns, refusing a lock that bypasses the buttons.

        :param dict vals: values to write.
        :return: True
        :rtype: bool
        :raises UserError: when the values set ``is_locked`` outside
            the lock context.
        """
        if "is_locked" in vals:
            self._check_lock_context()
        return super().write(vals)

    @api.model
    def _check_lock_context(self):
        """Raise unless the call comes from the lock buttons.

        The lock is written only with the ``score_column_lock`` context,
        which only ``_set_column_lock`` sets, so a direct RPC write
        cannot unlock a column.

        :raises UserError: when the context key is missing.
        """
        if self.env.context.get("score_column_lock"):
            return
        error_message = _(
            """
Context: Lock score column
Database ID: -
Problem: The lock of a column can only be changed with the buttons.
Solution: Use the Lock Column or Unlock Column button of the score sheet
"""
        )
        raise UserError(error_message)

    def action_lock_column(self):
        """Lock the columns, so their scores cannot change.

        The button is shown according to the ``lock_column_ok`` policy
        of the score sheet, and the policy is checked again here.

        :return: nothing
        """
        self._set_column_lock(True)

    def action_unlock_column(self):
        """Unlock the columns, so their scores can change again.

        The button is shown according to the ``unlock_column_ok``
        policy of the score sheet, and the policy is checked again here.

        :return: nothing
        """
        self._set_column_lock(False)

    def _set_column_lock(self, locked):
        """Check the policy of each sheet, then write the lock.

        :param bool locked: True to lock, False to unlock.
        :raises UserError: when a sheet is not in draft state, or its
            policy does not allow the action to the user.
        :return: nothing
        """
        policy_field = "lock_column_ok" if locked else "unlock_column_ok"
        for record in self:
            record._check_column_lock_allowed(policy_field)
        self.with_context(score_column_lock=True).write({"is_locked": locked})

    def _check_column_lock_allowed(self, policy_field):
        """Raise when the column may not be locked or unlocked now.

        :param str policy_field: ``lock_column_ok`` or
            ``unlock_column_ok``, the policy of the score sheet.
        :raises UserError: when the sheet is not in draft state, or the
            policy is not met and the policy check is not bypassed.
        """
        self.ensure_one()
        sheet = self.sheet_id
        if sheet.state != "draft":
            error_message = (
                _(
                    """
Document Type: %s
Context: Lock score column
Database ID: %s
Problem: A column can only be locked or unlocked in draft state
Solution: Restart the document before changing the lock of the column
"""
                )
                % (sheet._description, sheet.id)
            )
            raise UserError(error_message)
        if self.env.context.get("bypass_policy_check", False):
            return
        if not sheet[policy_field]:
            error_message = (
                _(
                    """
Document Type: %s
Context: Lock score column
Database ID: %s
Problem: Document is not allowed to change the lock of a column
Solution: Check the %s policy prerequisite
"""
                )
                % (sheet._description, sheet.id, policy_field)
            )
            raise UserError(error_message)

    def name_get(self):
        """Return the display name of each record.

        The name is the score component followed by the number of the
        score sheet, for example ``UH 1 (SSS/2026/000018)``. A draft
        sheet has no number yet and shows ``/``.

        The names are read with ``sudo()``: the display name is shown
        wherever the component is a tag, for example on the learning
        objective form, and the user may not read the score sheet
        itself because of its record rule. Only the name string leaves
        this method; no elevated recordset is returned.

        :return: list of ``(id, display name)`` pairs.
        :rtype: list
        """
        result = []
        for record in self.sudo():
            name = "%s (%s)" % (
                record.component_id.name or "",
                record.sheet_id.name or "",
            )
            result.append((record.id, name))
        return result

    @api.constrains("sheet_id", "component_id")
    def _check_unique_component(self):
        """Check that a sheet has one record per component.

        :raises ValidationError: when another record of the same sheet
            has the same score component.
        """
        for record in self:
            domain = [
                ("id", "!=", record.id),
                ("sheet_id", "=", record.sheet_id.id),
                ("component_id", "=", record.component_id.id),
            ]
            if self.search_count(domain):
                error_message = (
                    _(
                        """
Context: Save score sheet component
Database ID: %s
Problem: Component %s may only appear once per score sheet.
Solution: Remove the duplicate component
"""
                    )
                    % (record.id, record.display_name)
                )
                raise ValidationError(error_message)

    @api.constrains("objective_ids", "sheet_id")
    def _constrains_objective_scope(self):
        """Check the objectives against the scope of the sheet.

        :raises ValidationError: when an objective does not belong to
            the subject, grade and academic term of the sheet.
        """
        self._check_objective_scope()

    def _check_objective_scope(self):
        """Raise when an objective is outside the scope of the sheet.

        Shared by the constraint of this model and by the constraint of
        the score sheet, which runs it when the subject, the grade class
        or the academic term of the sheet changes.

        :raises ValidationError: when an objective belongs to another
            subject, grade or academic term than the sheet.
        """
        for record in self:
            sheet = record.sheet_id
            for objective in record.objective_ids:
                if (
                    objective.subject_id != sheet.subject_id
                    or objective.grade_id != sheet.grade_class_id.grade_id
                    or objective.academic_term_id != sheet.academic_term_id
                ):
                    error_message = (
                        _(
                            """
Context: Save score sheet component
Database ID: %s
Problem: Objective %s is outside the subject, grade, and term of sheet component %s.
Solution: Choose only objectives of the same subject, grade, and term as the sheet
"""
                        )
                        % (record.id, objective.display_name, record.display_name)
                    )
                    raise ValidationError(error_message)
