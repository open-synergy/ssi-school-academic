# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import math

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_round


class SchoolReportCardType(models.Model):
    """
    Represents a kind of report card, e.g. Mid-Term or Final.
    It stores how the final score is calculated: which components are
    averaged, the weight of the average and of every other component,
    the columns printed on the report card (component, title and order),
    and the decimal threshold
    used to round the final score.
    """

    _name = "school_report_card_type"
    _inherit = ["mixin.master_data"]
    _description = "School Report Card Type"

    term_type = fields.Selection(
        string="Term Type",
        selection=[
            ("mid_term", "Mid-Term"),
            ("final", "Final"),
        ],
        required=True,
        help=(
            "Kind of term the report card covers: "
            "Mid-Term = mid-term report card, "
            "Final = end-of-term report card."
        ),
    )
    average_component_ids = fields.Many2many(
        string="Averaged Components",
        comodel_name="school_score_component",
        relation="school_report_card_type_average_component_rel",
        column1="type_id",
        column2="component_id",
        help=(
            "Score components whose scores are averaged into one part "
            "of the final score. A component without a score is left "
            "out of the average."
        ),
    )
    average_weight = fields.Float(
        string="Average Weight (%)",
        help=(
            "Weight, in percent, of the average of the averaged "
            "components in the final score."
        ),
    )
    weight_ids = fields.One2many(
        string="Component Weights",
        comodel_name="school_report_card_type_weight",
        inverse_name="type_id",
        help=(
            "Weight of every score component that is not averaged. "
            "The average weight plus these weights must total 100%."
        ),
    )
    print_column_ids = fields.One2many(
        string="Printed Columns",
        comodel_name="school_report_card_type_print_column",
        inverse_name="type_id",
        help=(
            "Score component columns printed on the mid-term report card, "
            "at most four, in the order of their sequence. Leave empty to "
            "print only the final score."
        ),
    )
    display_component_ids = fields.Many2many(
        string="Displayed Columns",
        comodel_name="school_score_component",
        compute="_compute_display_component_ids",
        readonly=True,
        help=(
            "Score components printed as score columns on the report "
            "card, taken from the printed columns in order."
        ),
    )
    rounding_threshold = fields.Float(
        string="Rounding Threshold",
        required=True,
        default=0.56,
        digits=(3, 2),
        help=(
            "Decimal part from which the final score is rounded up. "
            "With 0.56, a score of 87.56 becomes 88 and 87.55 "
            "becomes 87. It must be between 0 and 1."
        ),
    )

    total_weight = fields.Float(
        string="Total Weight",
        compute="_compute_total_weight",
        store=True,
        readonly=True,
        help=(
            "Average weight plus the weights of all component lines. "
            "It must total 100%."
        ),
    )

    @api.depends("print_column_ids.component_id", "print_column_ids.sequence")
    def _compute_display_component_ids(self):
        """Compute the printed score components in column order.

        The result follows the sequence of the printed columns, so it is
        the single source of truth for the columns of the report card.
        """
        for record in self:
            result = record.print_column_ids.sorted("sequence").mapped("component_id")
            record.display_component_ids = result

    @api.depends("average_weight", "weight_ids.weight")
    def _compute_total_weight(self):
        """Compute the sum of the average weight and the line weights.

        Stored, so a change to any weight line recomputes it and the
        total weight check runs after all lines of a save are written.
        """
        for record in self:
            result = record.average_weight + sum(record.weight_ids.mapped("weight"))
            record.total_weight = result

    @api.constrains("total_weight")
    def _check_total_weight(self):
        """Reject a configuration whose weights do not total 100%.

        :raises ValidationError: when ``_check_total_weight_condition``
            returns False.
        """
        for record in self.sudo():
            if not record._check_total_weight_condition():
                error_message = (
                    _(
                        """
Context: Validate report card type
Database ID: %s
Problem: Total weight must be 100%%.
Solution: Adjust the average weight and the component weights to total 100%%
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    def _check_total_weight_condition(self):
        """Tell whether the average weight and line weights total 100.

        Extension point: override to change the expected total without
        touching the error message.

        :return: True when the sum is 100 to two decimals; never raises.
        """
        self.ensure_one()
        total = self.average_weight + sum(self.weight_ids.mapped("weight"))
        return float_compare(total, 100.0, precision_digits=2) == 0

    @api.constrains("average_component_ids", "weight_ids")
    def _check_component_weighted_once(self):
        """Reject a component that is weighted more than once.

        :raises ValidationError: when
            ``_check_component_weighted_once_condition`` returns False.
        """
        for record in self.sudo():
            if not record._check_component_weighted_once_condition():
                error_message = (
                    _(
                        """
Context: Validate report card type
Database ID: %s
Problem: A component may only be weighted once.
Solution: Keep each component either averaged or in one weight line
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    def _check_component_weighted_once_condition(self):
        """Tell whether no component is averaged and weighted twice.

        Extension point: override to allow repeated components without
        touching the error message.

        :return: True when the weight lines and the averaged components
            share no component and no weight line repeats a component;
            never raises.
        """
        self.ensure_one()
        line_components = self.weight_ids.mapped("component_id")
        if len(line_components) != len(self.weight_ids):
            return False
        return not (line_components & self.average_component_ids)

    @api.constrains("average_weight", "average_component_ids")
    def _check_average_components_required(self):
        """Reject an average weight without averaged components.

        :raises ValidationError: when
            ``_check_average_components_required_condition`` returns
            False.
        """
        for record in self.sudo():
            if not record._check_average_components_required_condition():
                error_message = (
                    _(
                        """
Context: Validate report card type
Database ID: %s
Problem: Averaged components are required when the average weight is set.
Solution: Select the averaged components or set the average weight to 0
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    def _check_average_components_required_condition(self):
        """Tell whether an average weight has averaged components.

        Extension point: override to relax the rule without touching
        the error message.

        :return: True when the average weight is not above 0 or at
            least one component is averaged; never raises.
        """
        self.ensure_one()
        if self.average_weight > 0.0:
            return bool(self.average_component_ids)
        return True

    @api.constrains("rounding_threshold")
    def _check_rounding_threshold(self):
        """Reject a rounding threshold outside the 0 to 1 range.

        :raises ValidationError: when
            ``_check_rounding_threshold_condition`` returns False.
        """
        for record in self.sudo():
            if not record._check_rounding_threshold_condition():
                error_message = (
                    _(
                        """
Context: Validate report card type
Database ID: %s
Problem: Rounding threshold must be between 0 and 1.
Solution: Enter a rounding threshold above 0 and below 1
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    def _check_rounding_threshold_condition(self):
        """Tell whether the rounding threshold is between 0 and 1.

        Extension point: override to change the accepted range without
        touching the error message.

        :return: True when 0 < ``rounding_threshold`` < 1; never
            raises.
        """
        self.ensure_one()
        return 0.0 < self.rounding_threshold < 1.0

    def compute_average_score(self, scores):
        """Compute the rounded mean of the averaged components.

        The mean of the scores of the averaged components is rounded
        to a whole number half-up, before it is weighted. A component
        without a score is not in the mean, and a score of 0 that is in
        the dict counts as a score.

        :param dict scores: score per component, ``{component_id:
            float}``; a component without a score is not in the dict.
        :return: the rounded mean, or None when no averaged component
            has a score.
        :rtype: float or None
        """
        self.ensure_one()
        average_scores = [
            scores[component.id]
            for component in self.average_component_ids
            if component.id in scores
        ]
        if not average_scores:
            return None
        mean = sum(average_scores) / len(average_scores)
        return float_round(mean, precision_digits=0)

    def compute_final_score(self, scores):
        """Compute the rounded final score from the component scores.

        The averaged components give one part (their mean, rounded to
        a whole number half-up before it is weighted) and every weight
        line gives one part, left unrounded. A part without a score is
        left out and the remaining weights are normalized, so a missing
        score never pulls the final score down to 0. A score of 0 that
        is in the dict counts as a score and enters the mean.

        :param dict scores: score per component, ``{component_id:
            float}``; a component without a score is not in the dict.
        :return: the final score rounded with the rounding threshold,
            or 0.0 when no part has a score.
        :rtype: float
        """
        self.ensure_one()
        parts = []
        average = self.compute_average_score(scores)
        if average is not None:
            parts.append((self.average_weight, average))
        for line in self.weight_ids:
            if line.component_id.id in scores:
                parts.append((line.weight, scores[line.component_id.id]))
        total_weight = sum(weight for weight, _score in parts)
        if not total_weight:
            return 0.0
        raw = sum(weight * score for weight, score in parts) / total_weight
        rounded = float_round(raw, precision_digits=2)
        floor_value = math.floor(rounded)
        fraction = rounded - floor_value
        if float_compare(fraction, self.rounding_threshold, precision_digits=2) >= 0:
            floor_value += 1
        return float(floor_value)
