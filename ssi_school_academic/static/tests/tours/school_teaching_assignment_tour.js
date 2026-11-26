// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_teaching_assignment_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- Flow 1 of the school_teaching_assignment
    // IK: "Open the School > Configuration > Subject & Scoring > Teaching
    // Assignments menu." "Subject & Scoring" is a level-3 grouping menuitem
    // without action=, so 14.0 renders it as a non-clickable dropdown
    // header and there is no step for it.
    function openAssignmentList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
            },
            {
                content: "Open the Teaching Assignments menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_teaching_assignment_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted.
                content: "Teaching Assignments list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Teaching Assignments)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    function pickMany2one(fieldName, text) {
        return [
            {
                content: "Select the " + fieldName,
                trigger: ".o_field_many2one[name='" + fieldName + "'] input",
                run: "text " + text,
            },
            {
                content: "Pick the " + fieldName + " from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(" + text + ")",
                in_modal: false,
            },
        ];
    }

    function pickLineMany2one(fieldName, text) {
        return [
            {
                content: "Select the " + fieldName + " of the line",
                trigger:
                    ".o_selected_row .o_field_many2one[name='" + fieldName + "'] input",
                run: "text " + text,
            },
            {
                content: "Pick the " + fieldName + " of the line from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(" + text + ")",
                in_modal: false,
            },
        ];
    }

    // IK: docs/school_teaching_assignment/01-create.md
    tour.register(
        "ssi_school_academic_school_teaching_assignment_create",
        {test: true, url: "/web"},
        [].concat(
            // Flow 1 -- Open the Teaching Assignments menu.
            openAssignmentList(),
            [
                // Flow 2 -- Click the New button. (14.0: "Create")
                {
                    content: "Click New",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 -- Fill in the required fields.
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR TA Assignment Create",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },
            ],
            pickMany2one("teacher_id", "TOUR TA Teacher"),
            pickMany2one("academic_term_id", "TOUR TA Term"),
            [
                // Flow 4 -- Open the Lines tab.
                {
                    content: "Open the Lines tab",
                    trigger: ".o_notebook .nav-link:contains(Lines)",
                },

                // Flow 5 -- Add a line and fill it in.
                {
                    content: "Click Add a line",
                    trigger:
                        ".o_field_x2many[name='line_ids'] .o_field_x2many_list_row_add a",
                },
            ],
            pickLineMany2one("homeroom_id", "TOUR TA Class"),
            [
                {
                    // The Grade Class is filled from the Homeroom and
                    // decides which Subjects the dropdown offers.
                    content: "The Grade Class follows the Homeroom",
                    trigger:
                        ".o_selected_row .o_field_widget[name='grade_class_id']:contains(TOUR TA Class)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ],
            pickLineMany2one("subject_id", "TOUR TA Subject"),
            [
                {
                    content: "Fill in the Weekly Hours of the line",
                    trigger: ".o_selected_row .o_field_widget[name='weekly_hours']",
                    run: "text 4",
                },

                // Flow 6 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- the record is created with its line.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR TA Assignment Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The line is listed",
                    trigger:
                        ".o_field_one2many[name='line_ids'] .o_data_row:contains(TOUR TA Subject)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_teaching_assignment/03-generate-score-sheets.md
    tour.register(
        "ssi_school_academic_school_teaching_assignment_generate_score_sheets",
        {test: true, url: "/web"},
        [].concat(
            // Flow 1 -- Open the Teaching Assignments menu.
            openAssignmentList(),
            [
                // Flow 2 -- Open the Teaching Assignment.
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR TG Assignment) .o_data_cell:first",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 -- Click Action and choose Generate Score Sheets.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                    run: function () {
                        this.$anchor[0].click();
                    },
                },
                {
                    content: "Click Generate Score Sheets",
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $item = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return (
                                    $(this).text().trim() === "Generate Score Sheets"
                                );
                            }
                        );
                        $item[0].click();
                    },
                },
                {
                    content: "The Generate Score Sheets dialog is displayed",
                    trigger: ".modal-title:contains(Generate Score Sheets)",
                    in_modal: false,
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 4 -- Click the Generate button.
                {
                    content: "Click Generate",
                    trigger: ".modal-footer button.btn-primary:contains(Generate)",
                    in_modal: true,
                },

                // Flow 5 -- Read the Result.
                {
                    content: "The Result gives the number of score sheets created",
                    trigger:
                        ".o_field_widget[name='result_note']:contains(Score sheets created: 1)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 6 -- Click Close.
                {
                    content: "Close the dialog",
                    trigger: ".modal-footer button:contains(Close)",
                    in_modal: true,
                },
                {
                    // Post-Condition -- the dialog is closed and the
                    // record stays displayed.
                    content: "The dialog is closed",
                    trigger: ".o_form_view.o_form_readonly",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_teaching_assignment/04-copy-from-previous-term.md
    tour.register(
        "ssi_school_academic_school_teaching_assignment_copy_from_previous_term",
        {test: true, url: "/web"},
        [
            // Flow 1 -- Open the Copy Teaching Assignments menu. The menu is
            // a leaf of the "Subject & Scoring" grouping header, like the
            // Teaching Assignments menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
            },
            {
                content: "Open the Copy Teaching Assignments menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.copy_teaching_assignment_from_previous_term_menu"]',
            },
            {
                // Gate: the menu opens a dialog, so wait for its title.
                content: "The Copy Teaching Assignments dialog is displayed",
                trigger: ".modal-title:contains(Copy Teaching Assignments)",
                in_modal: false,
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 2 -- Fill in the Source Term and the Target Term.
            {
                content: "Select the Source Term",
                trigger: ".o_field_many2one[name='source_term_id'] input",
                run: "text TOUR TC Term A",
            },
            {
                content: "Pick the Source Term from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR TC Term A)",
                in_modal: false,
            },
            {
                content: "Select the Target Term",
                trigger: ".o_field_many2one[name='target_term_id'] input",
                run: "text TOUR TC Term B",
            },
            {
                content: "Pick the Target Term from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR TC Term B)",
                in_modal: false,
            },
            {
                // The Source Term offers every assignment of that term.
                content: "The assignments of the source term are offered",
                trigger:
                    ".o_field_many2manytags[name='assignment_ids'] .o_badge_text:contains(TOUR TC Assignment)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 3 -- Click the Copy button.
            {
                content: "Click Copy",
                trigger: ".modal-footer button.btn-primary:contains(Copy)",
                in_modal: true,
            },

            // Flow 4 -- Read the Result.
            {
                content: "The Result gives the number of assignments copied",
                trigger:
                    ".o_field_widget[name='result_note']:contains(Assignments copied: 1, lines copied: 1)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // Flow 5 -- Click Close.
            {
                content: "Close the dialog",
                trigger: ".modal-footer button:contains(Close)",
                in_modal: true,
            },
            {
                // Post-Condition -- the dialog is closed.
                content: "The dialog is closed",
                trigger: ".o_web_client",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
