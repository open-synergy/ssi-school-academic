// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_score_sheet_enter_scores_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Score cell of the Nth line of the Scores tab. In 14.0 the list cell has
    // no name attribute, so it is addressed by its position: Enrollment,
    // Student, Score Component, then Score.
    function scoreCell(index) {
        return (
            ".o_field_one2many[name='line_ids'] .o_data_row:eq(" +
            index +
            ") .o_data_cell:eq(3)"
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
                // Pre-Condition: the generated lines are not scored yet, so
                // the cell is empty and not "0,00".
                content: "The first score cell is empty",
                trigger: scoreCell(0) + ":not(:contains(0))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the first score cell",
                trigger: scoreCell(0),
            },
            {
                content: "Type 0 in the first score cell",
                trigger: ".o_data_row.o_selected_row .o_data_cell input[name='score']",
                run: "text 0",
            },
            {
                content: "Click the second score cell",
                trigger: scoreCell(1),
            },
            {
                content: "Type 90 in the second score cell",
                trigger: ".o_data_row.o_selected_row .o_data_cell input[name='score']",
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
                trigger: scoreCell(0) + ":contains(0)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "The second score cell shows 90",
                trigger: scoreCell(1) + ":contains(90)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                // Post-Condition: a cell that was not touched stays empty.
                content: "The third score cell stays empty",
                trigger: scoreCell(2) + ":not(:contains(0))",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
