// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_curriculum_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- Flow 1 of every school_curriculum work
    // instruction: "Open the School > Configuration > Subject & Scoring >
    // Curriculums menu." "Subject & Scoring"
    // (ssi_school.menu_subject_configuration) is a level-3 grouping
    // menuitem with no action= attribute, so 14.0 renders it as a
    // non-clickable dropdown header without data-menu-xmlid -- there is no
    // step for it.
    function openCurriculumList() {
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
                content: "Open the Curriculums menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_curriculum_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted, not just
                // for "some list view" -- the landing action of the app is
                // also a .o_list_view.
                content: "Curriculums list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Curriculums)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Opens the row identified by the unique title set by setUpClass.
    // Draft curriculums share the placeholder number "/", so the title is
    // the only stable row key.
    function openCurriculumByTitle(title) {
        return [
            {
                content: "Open the curriculum",
                trigger: ".o_data_row:contains(" + title + ") .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    // Clicks a statusbar button, then OK on the confirmation dialog, then
    // waits for the status to settle.
    function clickWorkflowButton(buttonName, status) {
        return [
            {
                content: "Click the " + buttonName + " button",
                trigger: ".o_statusbar_buttons button[name='" + buttonName + "']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Status is " + status,
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='" +
                    status +
                    "'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    function pickMany2one(field, text) {
        return [
            {
                content: "Fill in " + field,
                trigger: ".o_field_many2one[name='" + field + "'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text " + text,
            },
            {
                content: "Pick " + field + " from the dropdown",
                trigger:
                    ".ui-autocomplete:visible .ui-menu-item a:contains(" + text + ")",
                in_modal: false,
            },
        ];
    }

    // IK: docs/school_curriculum/01-create.md
    tour.register(
        "ssi_school_academic_school_curriculum_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the School > Configuration > Subject & Scoring >
            // Curriculums menu.
            openCurriculumList(),
            [
                // Flow 2 -- Click the New button (14.0: "Create").
                {
                    content: "Click Create",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },
                // Flow 3 -- Fill in the header fields.
                {
                    content: "Fill in the Title",
                    trigger: ".o_field_widget[name='title']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Tour CU Create Curriculum",
                },
            ],
            pickMany2one("school_id", "TOUR Create School"),
            pickMany2one("academic_year_id", "TOUR Create Year"),
            [
                {
                    content: "Fill in Effective Start",
                    trigger: ".o_field_widget[name='effective_start'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 07/01/2026",
                },
                {
                    content: "Fill in Effective End",
                    trigger: ".o_field_widget[name='effective_end'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 06/30/2027",
                },
                // Flow 4 -- On the Lines tab, click Add a line and fill in
                // Subject, Grade, Weekly Hours and Total Class.
                {
                    content: "Add a line",
                    trigger:
                        ".o_field_x2many[name='line_ids'] .o_field_x2many_list_row_add a",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    content: "Fill in the Subject",
                    trigger:
                        ".o_selected_row .o_field_many2one[name='subject_id'] input",
                    run: "text TOUR Create Subject",
                },
                {
                    content: "Pick the Subject from the dropdown",
                    trigger:
                        ".ui-autocomplete:visible .ui-menu-item a:contains(TOUR Create Subject)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Grade",
                    trigger: ".o_selected_row .o_field_many2one[name='grade_id'] input",
                    run: "text TOUR Create Grade",
                },
                {
                    content: "Pick the Grade from the dropdown",
                    trigger:
                        ".ui-autocomplete:visible .ui-menu-item a:contains(TOUR Create Grade)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Weekly Hours",
                    trigger: ".o_selected_row .o_field_widget[name='weekly_hours']",
                    run: "text 4",
                },
                {
                    content: "Fill in the Total Class",
                    trigger: ".o_selected_row .o_field_widget[name='total_class']",
                    run: "text 3",
                },
                // Flow 5 -- Click Save. Clicking Save also leaves the line
                // row, which commits it into the record.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
                // Post-Condition -- a new curriculum is created in Draft
                // status. Category and Total Time are values and belong to
                // the unit test.
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_curriculum/04-confirm.md
    tour.register(
        "ssi_school_academic_school_curriculum_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Curriculums menu.
            openCurriculumList(),
            // Flow 2 -- Open the curriculum to confirm.
            openCurriculumByTitle("Tour CU Confirm Curriculum"),
            // Flow 3-4 -- Click the button, then OK on the dialog; the
            // Post-Condition is the new status on the statusbar.
            clickWorkflowButton("action_confirm", "confirm")
        )
    );

    // IK: docs/school_curriculum/05-approve.md
    tour.register(
        "ssi_school_academic_school_curriculum_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Curriculums menu.
            openCurriculumList(),
            // Flow 2 -- Open the curriculum to approve.
            openCurriculumByTitle("Tour CU Approve Curriculum"),
            // Flow 3-4 -- Click the button, then OK on the dialog; the
            // Post-Condition is the new status on the statusbar.
            clickWorkflowButton("action_approve_approval", "open")
        )
    );

    // IK: docs/school_curriculum/06-reject.md
    tour.register(
        "ssi_school_academic_school_curriculum_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Curriculums menu.
            openCurriculumList(),
            // Flow 2 -- Open the curriculum to reject.
            openCurriculumByTitle("Tour CU Reject Curriculum"),
            // Flow 3-4 -- Click the button, then OK on the dialog; the
            // Post-Condition is the new status on the statusbar.
            clickWorkflowButton("action_reject_approval", "reject")
        )
    );

    // IK: docs/school_curriculum/09-finish.md
    tour.register(
        "ssi_school_academic_school_curriculum_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Curriculums menu.
            openCurriculumList(),
            // Flow 2 -- Open the curriculum to finish.
            openCurriculumByTitle("Tour CU Finish Curriculum"),
            // Flow 3-4 -- Click the button, then OK on the dialog; the
            // Post-Condition is the new status on the statusbar.
            clickWorkflowButton("action_done", "done")
        )
    );

    // IK: docs/school_curriculum/12-restart.md
    tour.register(
        "ssi_school_academic_school_curriculum_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Curriculums menu.
            openCurriculumList(),
            // Flow 2 -- Open the curriculum to restart.
            openCurriculumByTitle("Tour CU Restart Curriculum"),
            // Flow 3-4 -- Click the button, then OK on the dialog; the
            // Post-Condition is the new status on the statusbar.
            clickWorkflowButton("action_restart", "draft")
        )
    );

    // IK: docs/school_curriculum/10-cancel.md
    tour.register(
        "ssi_school_academic_school_curriculum_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Curriculums menu.
            openCurriculumList(),
            // Flow 2 -- Open the curriculum to cancel.
            openCurriculumByTitle("Tour CU Cancel Curriculum"),
            [
                // Flow 3 -- Click the Cancel button.
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:contains(Cancel)",
                    extra_trigger: ".o_form_view",
                },
                // Flow 4 -- Select the Cancellation Reason in the wizard.
                {
                    content: "Wizard is open",
                    trigger: ".o_field_widget[name='cancel_reason_id']",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] label:contains(Tour CU Cancel Reason)",
                },
                // Flow 5 -- Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                // Flow 6 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the stacked dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                // Post-Condition -- status changes to Cancelled.
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );
});
