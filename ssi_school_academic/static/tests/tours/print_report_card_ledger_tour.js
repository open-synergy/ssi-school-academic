// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.print_report_card_ledger_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/print_report_card_ledger/01-print.md
    tour.register(
        "ssi_school_academic_print_report_card_ledger_print",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 -- Open the School > Classroom > Report Card Ledger
            // menu. App root > Classroom section > leaf, the same 3-level
            // shape as the Report Cards menu.
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
                content: "Open the Report Card Ledger menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.print_report_card_ledger_menu"]',
            },
            {
                // Gate: wait for the dialog itself. It waits for the modal
                // to appear, so the search is global (in_modal: false).
                content: "The Report Card Ledger dialog is displayed",
                trigger: ".modal-title:contains(Report Card Ledger)",
                in_modal: false,
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 2 -- Fill in Grade Class, Academic Term and Report Card
            // Type.
            {
                content: "Select the Grade Class",
                trigger: ".o_field_many2one[name='grade_class_id'] input",
                run: "text TOUR LDG Class",
            },
            {
                content: "Pick the Grade Class from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR LDG Class)",
                in_modal: false,
            },
            {
                content: "Select the Academic Term",
                trigger: ".o_field_many2one[name='academic_term_id'] input",
                run: "text TOUR LDG Term",
            },
            {
                content: "Pick the Academic Term from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR LDG Term)",
                in_modal: false,
            },
            {
                content: "Select the Report Card Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text TOUR LDG Type",
            },
            {
                content: "Pick the Report Card Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR LDG Type)",
                in_modal: false,
            },

            // Flow 3 -- Click the Show button. The Print button downloads a
            // PDF file, which has no DOM signal of completion, so the tour
            // only checks that it is displayed and enabled and does not
            // click it.
            {
                content: "The Print button is displayed and enabled",
                trigger: ".modal-footer button[name='action_print']:enabled",
                run: function () {
                    // Assertion only; the download is not triggered.
                },
            },
            {
                content: "Click Show",
                trigger: ".modal-footer button[name='action_show']:enabled",
            },

            // Post-Condition -- the ledger is shown on screen.
            {
                content: "The ledger is shown on screen",
                trigger: ".o_report_iframe",
                in_modal: false,
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
