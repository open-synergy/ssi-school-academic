// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_report_card_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block, Flow step 1 of every IK in
    // docs/school_report_card/: "Open the School > Classroom > Report
    // Cards menu." App root > Classroom section > leaf, the same 3-level
    // shape as the Deposit Forfeits menu of ssi_school_deposit.
    function openCardsList() {
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
                content: "Open the Report Cards menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_report_card_menu"]',
            },
            {
                // Gate: wait for the Report Cards action itself to be
                // mounted, not just any list view left over from the
                // landing action.
                content: "Report Cards list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(School Report Cards)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ];
    }

    // The search text is the dedicated Report Card Type name of the
    // scenario. Each type owns exactly one card, and no scenario suffix is
    // a prefix of another, so the row is unique in the list.
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

    // IK: docs/school_report_card/01-create.md
    tour.register(
        "ssi_school_academic_school_report_card_create",
        {test: true, url: "/web"},
        [].concat(openCardsList(), [
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
                content: "Select the Enrollment",
                trigger: ".o_field_many2one[name='enrollment_id'] input",
                run: "text TOUR-SRC-ENR-001",
            },
            {
                content: "Pick the Enrollment from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-SRC-ENR-001)",
                in_modal: false,
            },
            {
                // The Student is filled by the onchange of the Enrollment,
                // so wait for it before moving on.
                content: "The Student follows the Enrollment",
                trigger:
                    ".o_field_widget[name='student_id']:contains(TOUR SRC Student)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Select the Report Card Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text TOUR SRC Type CREATE",
            },
            {
                content: "Pick the Report Card Type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR SRC Type CREATE)",
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

    // IK: docs/school_report_card/02-generate-lines.md
    tour.register(
        "ssi_school_academic_school_report_card_generate_lines",
        {test: true, url: "/web"},
        [].concat(
            openCardsList(),
            openRecord("TOUR SRC Type GENERATE"),
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
                    content: "Open the Subjects tab",
                    trigger: ".o_notebook .nav-link:contains(Subjects)",
                    extra_trigger: "body:not(:has(.modal))",
                },
                {
                    // Post-Condition: lines were generated. The fixture
                    // report card starts without lines, so a row can only
                    // appear once the generation ran.
                    content: "A line is listed",
                    trigger: ".o_field_one2many[name='line_ids'] .o_data_row",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        )
    );

    // IK: docs/school_report_card/03-compute-scores.md
    tour.register(
        "ssi_school_academic_school_report_card_compute_scores",
        {test: true, url: "/web"},
        [].concat(
            openCardsList(),
            openRecord("TOUR SRC Type COMPUTE"),
            [
                {
                    content: "Click the Compute Scores button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_compute_scores']",
                    extra_trigger: ".o_form_view",
                },
            ],
            confirmDialog(),
            [
                {
                    content: "Open the Subjects tab",
                    trigger: ".o_notebook .nav-link:contains(Subjects)",
                    extra_trigger: "body:not(:has(.modal))",
                },
                {
                    // Post-Condition: the Predicate follows the computed
                    // Final Score. The fixture lines were generated before
                    // the score sheet was done, so they start without a
                    // score and a predicate, and a row can only show the
                    // top predicate once the scores were computed.
                    content: "The line earns the top predicate",
                    trigger:
                        ".o_field_one2many[name='line_ids'] .o_data_row:contains(TOUR SRC Top)",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        )
    );

    // IK: docs/school_report_card/04-confirm.md
    tour.register(
        "ssi_school_academic_school_report_card_confirm",
        {test: true, url: "/web"},
        [].concat(
            openCardsList(),
            openRecord("TOUR SRC Type CONFIRM"),
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

    // IK: docs/school_report_card/05-approve.md
    tour.register(
        "ssi_school_academic_school_report_card_approve",
        {test: true, url: "/web"},
        [].concat(
            openCardsList(),
            openRecord("TOUR SRC Type APPROVE"),
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

    // IK: docs/school_report_card/06-reject.md
    tour.register(
        "ssi_school_academic_school_report_card_reject",
        {test: true, url: "/web"},
        [].concat(
            openCardsList(),
            openRecord("TOUR SRC Type REJECT"),
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

    // IK: docs/school_report_card/07-cancel.md
    tour.register(
        "ssi_school_academic_school_report_card_cancel",
        {test: true, url: "/web"},
        [].concat(
            openCardsList(),
            openRecord("TOUR SRC Type CANCEL"),
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
                        ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(TOUR SRC Cancel Reason) input",
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
});
