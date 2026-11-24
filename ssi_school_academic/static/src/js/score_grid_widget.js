// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.FieldScoreGrid", function (require) {
    "use strict";

    var core = require("web.core");
    var field_registry = require("web.field_registry");
    var relational_fields = require("web.relational_fields");
    var ScoreGridRenderer = require("ssi_school_academic.ScoreGridRenderer");
    var _lt = core._lt;

    // Shows the score lines of a score sheet as a grid: one row per student,
    // one column per score component, and the calculated columns of the
    // report card. The lines are the One2many of the sheet, so the scores are
    // saved with the form, like in an editable list.
    var FieldScoreGrid = relational_fields.FieldOne2Many.extend({
        description: _lt("Score Grid"),

        // The core cuts a sub view at 40 records unless the widget sets its own
        // limit. A grid of a whole class must not lose a student.
        limit: 100000,

        // --------------------------------------------------------------------
        // Public
        // --------------------------------------------------------------------

        /**
         * Notify the pending value of every score cell, so a score typed in a
         * cell that still has the focus is saved with the form.
         *
         * @override
         * @returns {Promise}
         */
        commitChanges: function () {
            var defs = [];
            if (this.renderer) {
                _.each(this.renderer.allFieldWidgets, function (widgets) {
                    _.each(widgets, function (widget) {
                        defs.push(widget.commitChanges());
                    });
                });
            }
            return Promise.all(defs);
        },

        /**
         * Keep the grid in step with the sheet: the minimum score depends on
         * the subject and the class, not on a line.
         *
         * @override
         * @returns {Promise}
         */
        reset: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                if (self.renderer && self.renderer.refreshMinimum) {
                    self.renderer.refreshMinimum();
                }
            });
        },

        /**
         * Give the focus to the first score cell when the user tabs into the
         * field. There is no line to add, so nothing else is activated.
         *
         * @override
         * @returns {Boolean}
         */
        activate: function () {
            if (this.isReadonly || !this.renderer || !this.$el.is(":visible")) {
                return false;
            }
            return this.renderer.activateFirstCell();
        },

        // --------------------------------------------------------------------
        // Private
        // --------------------------------------------------------------------

        /**
         * Build the grid renderer on the first call and update it afterwards.
         *
         * @override
         * @private
         * @returns {Promise}
         */
        _render: function () {
            if (!this.view || this.view.arch.tag !== "tree") {
                return this._super.apply(this, arguments);
            }
            this.currentColInvisibleFields = this._evalColumnInvisibleFields();
            if (this.renderer) {
                return this.renderer.updateState(this.value, {});
            }
            this.renderer = new ScoreGridRenderer(this, this.value, {
                arch: this.view.arch,
                viewType: "list",
            });
            this.$el.addClass("o_field_x2many o_field_x2many_list o_field_score_grid");
            return this.renderer.appendTo(this.$el);
        },
    });

    field_registry.add("score_grid", FieldScoreGrid);

    return FieldScoreGrid;
});
