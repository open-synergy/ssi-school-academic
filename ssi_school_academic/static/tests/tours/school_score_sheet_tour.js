// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_score_sheet_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block, Flow step 1 of every IK in
    // docs/school_score_sheet/: "Open the School > Classroom > Score
    // Sheets menu." App root > Classroom section > leaf, the same 3-level
    // shape as the Deposit Forfeits menu of ssi_school_deposit.
    function openSheetsList() {
        return [
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
                // Gate: wait for the Score Sheets action itself to be
                // mounted, not just any list view left over from the
                // landing action.
                content: "Score Sheets list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(School Score Sheets)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ];
    }

    // The search text is the dedicated Subject name of the scenario. Each
    // subject owns exactly one sheet, and no scenario suffix is a prefix of
    // another, so the row is unique in the list.
    function openRecord(searchText) {
        return [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(" + searchText + ") .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ];
    }

    function confirmDialog() {
        return [
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
        ];
    }

    // IK: docs/school_score_sheet/01-create.md
    tour.register(
        "ssi_school_academic_school_score_sheet_create",
        {test: true, url: "/web"},
        [].concat(openSheetsList(), [
            {
                content: "Click New",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Select the Grade Class",
                trigger: ".o_field_many2one[name='grade_class_id'] input",
                run: "text TOUR SSS Class",
            },
            {
                content: "Pick the Grade Class from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR SSS Class)",
                in_modal: false,
            },
            {
                // The Grade is filled by the onchange of the Grade Class and
                // decides which Subjects the dropdown offers, so wait for it.
                content: "The Grade follows the Grade Class",
                trigger: ".o_field_widget[name='grade_id']:contains(TOUR SSS Grade)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Select the Academic Term",
                trigger: ".o_field_many2one[name='academic_term_id'] input",
                run: "text TOUR SSS Term",
            },
            {
                content: "Pick the Academic Term from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR SSS Term)",
                in_modal: false,
            },
            {
                content: "Select the Teacher",
                trigger: ".o_field_many2one[name='teacher_id'] input",
                run: "text TOUR SSS Teacher",
            },
            {
                content: "Pick the Teacher from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR SSS Teacher)",
                in_modal: false,
            },
            {
                content: "Select the Subject",
                trigger: ".o_field_many2one[name='subject_id'] input",
                run: "text TOUR SSS Subject CREATE",
            },
            {
                content: "Pick the Subject from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR SSS Subject CREATE)",
                in_modal: false,
            },
            {
                content: "Save the record",
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
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ])
    );

    // IK: docs/school_score_sheet/02-generate-lines.md
    tour.register(
        "ssi_school_academic_school_score_sheet_generate_lines",
        {test: true, url: "/web"},
        [].concat(
            openSheetsList(),
            openRecord("TOUR SSS Subject GENERATE"),
            [
                {
                    content: "Click the Generate Lines button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_generate_lines']",
                    extra_trigger: ".o_form_view",
                },
            ],
            confirmDialog(),
            [
                {
                    content: "Open the Scores tab",
                    trigger: ".o_notebook .nav-link:contains(Scores)",
                    extra_trigger: "body:not(:has(.modal))",
                },
                {
                    // Post-Condition: lines were generated. The fixture
                    // sheet starts without lines, so a row can only appear
                    // once the generation ran.
                    content: "A line is listed",
                    trigger: ".o_field_one2many[name='line_ids'] .o_data_row",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        )
    );

    // IK: docs/school_score_sheet/03-confirm.md
    tour.register(
        "ssi_school_academic_school_score_sheet_confirm",
        {test: true, url: "/web"},
        [].concat(
            openSheetsList(),
            openRecord("TOUR SSS Subject CONFIRM"),
            [
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },
            ],
            confirmDialog(),
            [
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        )
    );

    // IK: docs/school_score_sheet/04-approve.md
    tour.register(
        "ssi_school_academic_school_score_sheet_approve",
        {test: true, url: "/web"},
        [].concat(
            openSheetsList(),
            openRecord("TOUR SSS Subject APPROVE"),
            [
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },
            ],
            confirmDialog(),
            [
                {
                    content: "Status is Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        )
    );

    // IK: docs/school_score_sheet/05-reject.md
    tour.register(
        "ssi_school_academic_school_score_sheet_reject",
        {test: true, url: "/web"},
        [].concat(
            openSheetsList(),
            openRecord("TOUR SSS Subject REJECT"),
            [
                {
                    content: "Click the Reject button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reject_approval']",
                    extra_trigger: ".o_form_view",
                },
            ],
            confirmDialog(),
            [
                {
                    content: "Status is Rejected",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        )
    );

    // IK: docs/school_score_sheet/06-cancel.md
    tour.register(
        "ssi_school_academic_school_score_sheet_cancel",
        {test: true, url: "/web"},
        [].concat(
            openSheetsList(),
            openRecord("TOUR SSS Subject CANCEL"),
            [
                // The Cancel button is a `type="action"` button, so its
                // `name` attribute is a numeric action id in the DOM;
                // target it by label instead.
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                    extra_trigger: ".o_form_view",
                },
                {
                    // The wizard renders cancel_reason_id with
                    // widget="radio" -- select the matching radio item by
                    // its label text. 14.0: do NOT prefix the trigger with
                    // `.modal`.
                    content: "Select the Cancellation Reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(TOUR SSS Cancel Reason) input",
                    in_modal: true,
                },
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
            ],
            confirmDialog(),
            [
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        )
    );

    // IK: docs/school_score_sheet/07-restart-approval.md
    tour.register(
        "ssi_school_academic_school_score_sheet_restart_approval",
        {test: true, url: "/web"},
        [].concat(
            openSheetsList(),
            openRecord("TOUR SSS Subject RESTART"),
            [
                {
                    content: "Click the Restart Approval Process button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reload_approval_template']",
                    extra_trigger: ".o_form_view",
                },
            ],
            confirmDialog(),
            [
                {
                    content: "Status is still Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        )
    );

    // IK: docs/school_score_sheet/09-choose-objectives.md
    tour.register(
        "ssi_school_academic_school_score_sheet_choose_objectives",
        {test: true, url: "/web"},
        [].concat(
            // Flow 1 and 2 -- Open the Score Sheets menu, open the record.
            openSheetsList(),
            openRecord("TOUR SSS Subject OBJECTIVE"),
            [
                // Flow 3 -- Click the Edit button.
                {
                    content: "Click the Edit button",
                    trigger: ".o_form_button_edit",
                },
                {
                    content: "Form is now editable",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },

                // Flow 4 -- Open the Learning Objectives tab.
                {
                    content: "Open the Learning Objectives tab",
                    trigger: ".o_notebook .nav-link:contains(Learning Objectives)",
                },

                // Flow 5 -- Click the Learning Objectives cell of a row and
                // choose an objective.
                {
                    content: "Click the Learning Objectives cell of the first row",
                    trigger:
                        ".o_field_one2many[name='component_ids'] .o_data_row:contains(TOUR SSS Daily Test 1) .o_data_cell:last",
                },
                {
                    content: "Type the objective",
                    trigger:
                        ".o_selected_row .o_field_many2manytags[name='objective_ids'] input",
                    run: "text TOUR SSS TP One",
                },
                {
                    content: "Pick the objective from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR SSS TP One)",
                    in_modal: false,
                },

                // Flow 6 -- Click the Save button.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- the chosen objective is listed on the
                // row of the component.
                {
                    content: "The objective is listed on the row",
                    trigger:
                        ".o_field_one2many[name='component_ids'] .o_data_row:contains(TOUR SSS TP One)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        )
    );
});
