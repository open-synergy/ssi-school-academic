// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_score_sheet_enter_scores_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Score cell of the Nth component of the Nth student of the Scores grid.
    // The grid has one row per student and one cell per score component, so
    // a cell is addressed by its row and column position.
    function scoreCell(row, column) {
        return (
            ".o_score_grid_table .o_data_row:eq(" +
            row +
            ") .o_score_grid_cell:eq(" +
            column +
            ")"
        );
    }

    // IK: docs/school_score_sheet/08-enter-scores.md
    tour.register(
        "ssi_school_academic_school_score_sheet_enter_scores",
        {test: true, url: "/web"},
        [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Classroom menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_classroom"]',
            },
            {
                content: "Open the Score Sheets menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_score_sheet_menu"]',
            },
            {
                content: "Score Sheets list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(School Score Sheets)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR SSS Subject ENTER) .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Open the Scores tab",
                trigger: ".o_notebook .nav-link:contains(Scores)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                // The Scores tab is a grid, not a list: one row per student and
                // the calculated columns after the components.
                content: "The Scores tab is a grid with the calculated columns",
                trigger: ".o_score_grid_table .o_score_grid_calculated_header",
                extra_trigger: ".o_score_grid_table .o_data_row:eq(1)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the first score cell",
                trigger: scoreCell(0, 0) + " input",
                run: "click",
            },
            {
                content: "Type 0 in the first score cell",
                trigger: scoreCell(0, 0) + " input",
                run: "text 0",
            },
            {
                content: "Press Tab in the first score cell",
                trigger: scoreCell(0, 0) + " input",
                run: "keydown 9",
            },
            {
                // The focus moved to the next cell of the same student.
                content: "The second score cell has the focus",
                trigger: scoreCell(0, 1) + " input",
                run: function () {
                    if (document.activeElement !== this.$anchor[0]) {
                        throw new Error("The focus did not move to the next cell.");
                    }
                },
            },
            {
                content: "Type 90 in the second score cell",
                trigger: scoreCell(0, 1) + " input",
                run: "text 90",
            },
            {
                content: "Click the Save button",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                // Post-Condition: the typed zero is shown and counted.
                content: "The first score cell shows the zero",
                trigger: scoreCell(0, 0) + ":contains(0)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "The second score cell shows 90",
                trigger: scoreCell(0, 1) + ":contains(90)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                // Post-Condition: a cell that was not touched stays empty.
                content: "The first score cell of the second student stays empty",
                trigger: scoreCell(1, 0) + ":not(:contains(0))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                // Post-Condition: the subject has a minimum score of 75, so the
                // zero is red, 90 is not, and an empty cell never is.
                content: "The zero is below the minimum score and is red",
                trigger: scoreCell(0, 0) + ".o_score_grid_below_minimum",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "The score of 90 is not red",
                trigger: scoreCell(0, 1) + ":not(.o_score_grid_below_minimum)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "The empty cell is not red",
                trigger: scoreCell(1, 0) + ":not(.o_score_grid_below_minimum)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
