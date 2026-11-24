// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.ScoreGridRenderer", function (require) {
    "use strict";

    var BasicRenderer = require("web.BasicRenderer");
    var core = require("web.core");
    var field_utils = require("web.field_utils");
    var session = require("web.session");
    var _t = core._t;

    // The renderer of the score grid: one row per student and one column per
    // score component, followed by the calculated columns that the server
    // describes. Every score cell is a real ``score_entry`` field widget bound
    // to its score line, so a typed score travels to the form like in an
    // editable list. It is modelled on the 2D matrix renderer of OCA web, which
    // is rejected as a dependency: its axes are locked on the display name and
    // it has no keyboard navigation. All the formulas stay on the server.
    var ScoreGridRenderer = BasicRenderer.extend({
        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            // Layout of the calculated columns, loaded once from the server.
            this._layout = null;
            // ``{component_id: [sequence, id]}``, loaded from the server.
            this._componentOrder = {};
            // Answers of older requests are dropped, only the last one counts.
            this._refreshToken = 0;
            this._widgetAt = [];
            this._rows = [];
            this._components = [];
        },

        // --------------------------------------------------------------------
        // Public
        // --------------------------------------------------------------------

        /**
         * Update the grid after a score changed. Only the widgets of the
         * changed line are reset, so the focus and the typed text stay.
         *
         * @param {Object} state
         * @param {String} id datapoint id of the changed line
         * @param {String[]} fields names of the changed fields
         * @param {OdooEvent} ev
         * @returns {Promise}
         */
        confirmUpdate: function (state, id, fields, ev) {
            var self = this;
            return this.confirmChange(state, id, fields, ev).then(function () {
                self._paintMinimum();
                self._refreshCalculated();
            });
        },

        /**
         * Repaint what depends on the sheet, not on a line: the minimum score
         * may have changed with the subject.
         */
        refreshMinimum: function () {
            this._paintMinimum();
            this._paintCalculatedMinimum();
        },

        /**
         * The grid has no line in edition.
         *
         * @returns {null}
         */
        getEditableRecordID: function () {
            return null;
        },

        /**
         * The grid has no line in edition, so there is nothing to unselect.
         *
         * @returns {Promise}
         */
        unselectRow: function () {
            return Promise.resolve();
        },

        /**
         * Give the focus to the first score cell that can be edited.
         *
         * @returns {Boolean} true when a cell took the focus
         */
        activateFirstCell: function () {
            var widget = this._scan(0, -1, 0, 1, true);
            return Boolean(widget && widget.activate());
        },

        // --------------------------------------------------------------------
        // Private
        // --------------------------------------------------------------------

        /**
         * Render the whole grid. The score cells are field widgets, which are
         * collected in ``this.defs`` while the table is built.
         *
         * @override
         * @private
         * @returns {Promise}
         */
        _renderView: function () {
            var self = this;
            return this._loadMeta().then(function () {
                self.$el.empty();
                self._buildGrid();
                var defs = [];
                self.defs = defs;
                var $table = self._renderTable();
                delete self.defs;
                self.$el.append($table);
                return Promise.all(defs).then(function () {
                    self._paintMinimum();
                    self._refreshCalculated();
                });
            });
        },

        /**
         * Load what the server decides: the layout of the calculated columns
         * and the order of the components, which is not part of the line.
         *
         * @private
         * @returns {Promise}
         */
        _loadMeta: function () {
            var self = this;
            var defs = [];
            if (!this._layout) {
                defs.push(
                    this._rpc({
                        model: "school_score_sheet",
                        method: "get_score_grid_layout",
                        args: [],
                        context: session.user_context,
                    }).then(function (layout) {
                        self._layout = layout;
                    })
                );
            }
            var missing = [];
            _.each(this.state.data, function (record) {
                var component = record.data.component_id;
                if (
                    component &&
                    component.res_id &&
                    !self._componentOrder[component.res_id] &&
                    missing.indexOf(component.res_id) === -1
                ) {
                    missing.push(component.res_id);
                }
            });
            if (missing.length) {
                defs.push(
                    this._rpc({
                        model: "school_score_component",
                        method: "search_read",
                        args: [[["id", "in", missing]], ["sequence"]],
                        context: _.extend({}, session.user_context, {
                            active_test: false,
                        }),
                    }).then(function (components) {
                        _.each(components, function (component) {
                            self._componentOrder[component.id] = [
                                component.sequence,
                                component.id,
                            ];
                        });
                    })
                );
            }
            return Promise.all(defs);
        },

        /**
         * Group the lines into rows (one per student id) and columns (one per
         * component, ordered by sequence then id).
         *
         * @private
         */
        _buildGrid: function () {
            var self = this;
            var rowsById = {};
            var componentsById = {};
            this._rows = [];
            _.each(this.state.data, function (record) {
                var student = record.data.student_id;
                var component = record.data.component_id;
                if (!student || !student.res_id || !component || !component.res_id) {
                    return;
                }
                if (!rowsById[student.res_id]) {
                    rowsById[student.res_id] = {
                        studentId: student.res_id,
                        label: student.data.display_name,
                        records: {},
                    };
                    self._rows.push(rowsById[student.res_id]);
                }
                rowsById[student.res_id].records[component.res_id] = record;
                if (!componentsById[component.res_id]) {
                    componentsById[component.res_id] = {
                        id: component.res_id,
                        label: component.data.display_name,
                    };
                }
            });
            this._components = _.values(componentsById);
            this._components.sort(function (a, b) {
                var oa = self._componentOrder[a.id] || [0, a.id];
                var ob = self._componentOrder[b.id] || [0, b.id];
                return oa[0] - ob[0] || oa[1] - ob[1];
            });
            this._columns = this._buildColumns();
        },

        /**
         * Place the calculated columns among the component columns. A column
         * goes right after its ``after_component_id``; the ones without a
         * place, or whose component has no line, go at the far right. Columns
         * on the same component keep the order of the layout.
         *
         * @private
         * @returns {Object[]} columns ``{type, component|calc}``
         */
        _buildColumns: function () {
            var columns = [];
            var placed = {};
            var componentIds = _.pluck(this._components, "id");
            var trailing = [];
            _.each(this._layout || [], function (calc) {
                if (
                    calc.after_component_id &&
                    _.contains(componentIds, calc.after_component_id)
                ) {
                    placed[calc.after_component_id] =
                        placed[calc.after_component_id] || [];
                    placed[calc.after_component_id].push(calc);
                } else {
                    trailing.push(calc);
                }
            });
            _.each(this._components, function (component, index) {
                columns.push({type: "component", component: component, index: index});
                _.each(placed[component.id] || [], function (calc) {
                    columns.push({type: "calculated", calc: calc});
                });
            });
            _.each(trailing, function (calc) {
                columns.push({type: "calculated", calc: calc});
            });
            return columns;
        },

        /**
         * @private
         * @returns {jQuery} the table
         */
        _renderTable: function () {
            var $table = $("<table>", {
                class: "o_list_table table table-sm table-striped o_score_grid_table",
            });
            var $head = $("<tr>").append(
                $("<th>", {class: "o_score_grid_student_header"}).text(_t("Student"))
            );
            _.each(
                this._columns,
                function (column) {
                    $head.append(this._renderHeaderCell(column));
                },
                this
            );
            $table.append($("<thead>").append($head));
            var $body = $("<tbody>");
            this._widgetAt = [];
            _.each(
                this._rows,
                function (row, rowIndex) {
                    this._widgetAt[rowIndex] = [];
                    $body.append(this._renderRow(row, rowIndex));
                },
                this
            );
            $table.append($body);
            return $table;
        },

        /**
         * @private
         * @param {Object} column
         * @returns {jQuery} the header cell
         */
        _renderHeaderCell: function (column) {
            var $th = $("<th>", {class: "o_score_grid_header text-right"});
            if (column.type === "component") {
                return $th.text(column.component.label).attr({
                    "data-component-id": column.component.id,
                });
            }
            $th.addClass("o_score_grid_calculated_header").attr({
                "data-key": column.calc.key,
            });
            $th.append($("<span>").text(column.calc.label));
            if (column.calc.warning) {
                $th.append(
                    $("<i>", {
                        class: "fa fa-exclamation-triangle o_score_grid_warning",
                        title: column.calc.warning,
                    })
                );
            }
            return $th;
        },

        /**
         * @private
         * @param {Object} row
         * @param {Number} rowIndex
         * @returns {jQuery} the row
         */
        _renderRow: function (row, rowIndex) {
            var $tr = $("<tr>", {class: "o_data_row"}).attr(
                "data-student-id",
                row.studentId
            );
            $tr.append(
                $("<td>", {class: "o_data_cell o_score_grid_student"}).text(row.label)
            );
            _.each(
                this._columns,
                function (column) {
                    if (column.type === "calculated") {
                        $tr.append(
                            $("<td>", {
                                class:
                                    "o_data_cell o_list_number o_score_grid_calculated",
                            }).attr("data-key", column.calc.key)
                        );
                        return;
                    }
                    var record = row.records[column.component.id];
                    var $td = $("<td>", {
                        class: "o_data_cell o_list_number o_score_grid_cell",
                    }).attr("data-component-id", column.component.id);
                    if (record) {
                        $td.attr("data-record-id", record.id);
                        $td.append(
                            this._renderScoreCell(record, rowIndex, column.index)
                        );
                    }
                    $tr.append($td);
                },
                this
            );
            return $tr;
        },

        /**
         * Render the ``score`` field widget of one line and remember it by
         * its row and component position, for the keyboard navigation.
         *
         * @private
         * @param {Object} record the score line
         * @param {Number} rowIndex
         * @param {Number} componentIndex
         * @returns {jQuery}
         */
        _renderScoreCell: function (record, rowIndex, componentIndex) {
            var node = this._getScoreNode();
            var mode = this.getParent().mode;
            var $el = this._renderFieldWidget(node, record, {mode: mode});
            var widgets = this.allFieldWidgets[record.id];
            var widget = widgets[widgets.length - 1];
            widget.__score_position = {row: rowIndex, col: componentIndex};
            this._widgetAt[rowIndex][componentIndex] = widget;
            return $el;
        },

        /**
         * @private
         * @returns {Object} the arch node of the ``score`` field
         */
        _getScoreNode: function () {
            var node = _.find(this.arch.children, function (child) {
                return child.tag === "field" && child.attrs.name === "score";
            });
            return node || {tag: "field", attrs: {name: "score"}};
        },

        /**
         * Collect the scored cells to send to the server. Only a cell that
         * was entered, zero included, takes part in the calculation.
         *
         * @private
         * @returns {Object} ``{student_id: {component_id: score}}``
         */
        _collectScores: function () {
            var scores = {};
            _.each(this.state.data, function (record) {
                var student = record.data.student_id;
                var component = record.data.component_id;
                if (!student || !student.res_id || !component || !component.res_id) {
                    return;
                }
                if (!record.data.is_scored) {
                    return;
                }
                scores[student.res_id] = scores[student.res_id] || {};
                scores[student.res_id][component.res_id] = record.data.score;
            });
            return scores;
        },

        /**
         * Ask the server for the calculated columns and show them. There is no
         * formula here: the server uses the ones of the report card.
         *
         * @private
         * @returns {Promise}
         */
        _refreshCalculated: function () {
            var self = this;
            this._refreshToken += 1;
            var token = this._refreshToken;
            return this._rpc({
                model: "school_score_sheet",
                method: "compute_score_grid",
                args: [this._collectScores()],
                context: session.user_context,
            }).then(function (result) {
                if (token === self._refreshToken) {
                    self._paintCalculated(result);
                }
            });
        },

        /**
         * @private
         * @returns {Number} the minimum score (KKM) of the sheet
         */
        _getMinimumScore: function () {
            var data = this.getParent().recordData || {};
            return data.minimum_score || 0;
        },

        /**
         * Fill the calculated cells; an empty value leaves the cell empty.
         *
         * @private
         * @param {Object} result ``{student_id: {key: value|null}}``
         */
        _paintCalculated: function (result) {
            var minimum = this._getMinimumScore();
            var self = this;
            this.$("tr.o_data_row").each(function () {
                var $tr = $(this);
                var values = result[$tr.data("student-id")] || {};
                $tr.find("td.o_score_grid_calculated").each(function () {
                    var $td = $(this);
                    var value = values[$td.data("key")];
                    var filled = value !== null && value !== undefined;
                    $td.data("value", filled ? value : null);
                    $td.text(filled ? self._formatCalculated(value) : "");
                    $td.toggleClass(
                        "o_score_grid_below_minimum",
                        filled && value < minimum
                    );
                });
            });
        },

        /**
         * Mark again the filled calculated cells against the minimum score,
         * without asking the server.
         *
         * @private
         */
        _paintCalculatedMinimum: function () {
            var minimum = this._getMinimumScore();
            this.$("td.o_score_grid_calculated").each(function () {
                var $td = $(this);
                var value = $td.data("value");
                var below = value !== null && value !== undefined && value < minimum;
                $td.toggleClass("o_score_grid_below_minimum", below);
            });
        },

        /**
         * @private
         * @param {Number} value
         * @returns {String}
         */
        _formatCalculated: function (value) {
            return field_utils.format.float(value, {type: "float"}, {digits: [16, 0]});
        },

        /**
         * Mark the scored cells that are below the minimum score. An empty
         * cell is never marked.
         *
         * @private
         */
        _paintMinimum: function () {
            var minimum = this._getMinimumScore();
            var self = this;
            _.each(this.state.data, function (record) {
                var $td = self.$("td[data-record-id='" + record.id + "']");
                var below =
                    Boolean(record.data.is_scored) && record.data.score < minimum;
                $td.toggleClass("o_score_grid_below_minimum", below);
            });
        },

        /**
         * Find the nearest editable cell from a position.
         *
         * @private
         * @param {Number} row start row
         * @param {Number} col start component column
         * @param {Number} dRow row step, for the vertical moves
         * @param {Number} dCol column step, for the horizontal moves
         * @param {Boolean} wrap go on with the next (previous) row at the
         *   end of a row, as Tab does
         * @returns {AbstractField|null}
         */
        _scan: function (row, col, dRow, dCol, wrap) {
            var nCols = this._components.length;
            var nRows = this._rows.length;
            var widget = null;
            if (dRow) {
                for (var r = row + dRow; r >= 0 && r < nRows; r += dRow) {
                    widget = this._widgetAt[r][col];
                    if (widget) {
                        return widget;
                    }
                }
                return null;
            }
            var index = row * nCols + col + dCol;
            while (index >= 0 && index < nRows * nCols) {
                var currentRow = Math.floor(index / nCols);
                if (!wrap && currentRow !== row) {
                    break;
                }
                widget = this._widgetAt[currentRow][index % nCols];
                if (widget) {
                    return widget;
                }
                index += dCol;
            }
            return null;
        },

        /**
         * Move the focus between the score cells: Tab and Shift+Tab go to the
         * next and previous cell, Enter and the arrows move by row and column.
         * At the edge of the grid the event goes on, so Tab leaves the grid.
         *
         * @override
         * @private
         * @param {OdooEvent} ev "navigation_move" event
         */
        _onNavigationMove: function (ev) {
            var position = ev.target && ev.target.__score_position;
            if (!position) {
                return;
            }
            var target = null;
            var row = position.row;
            var col = position.col;
            switch (ev.data.direction) {
                case "next":
                    target = this._scan(row, col, 0, 1, true);
                    break;
                case "previous":
                    target = this._scan(row, col, 0, -1, true);
                    break;
                case "next_line":
                case "down":
                    target = this._scan(row, col, 1, 0, false);
                    break;
                case "up":
                    target = this._scan(row, col, -1, 0, false);
                    break;
                case "right":
                    target = this._scan(row, col, 0, 1, false);
                    break;
                case "left":
                    target = this._scan(row, col, 0, -1, false);
                    break;
                default:
                    return;
            }
            if (target) {
                // The typed score is notified now: the focus change of the
                // browser would only do it when the input loses the focus.
                ev.target.commitChanges();
                if (target.activate()) {
                    ev.stopPropagation();
                }
            }
        },
    });

    return ScoreGridRenderer;
});
