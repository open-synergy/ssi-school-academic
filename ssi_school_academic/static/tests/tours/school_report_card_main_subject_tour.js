// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_report_card_main_subject_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/school_report_card_main_subject/01-create.md
    tour.register(
        "ssi_school_academic_school_report_card_main_subject_create",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 -- Open the Main Subjects menu. "Subject & Scoring"
            // (ssi_school.menu_subject_configuration) is a grouping
            // menuitem without action, rendered as a non-clickable
            // dropdown header in 14.0, so it has no step.
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
                content: "Open the Main Subjects menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_report_card_main_subject_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted.
                content: "Main Subjects list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Main Subjects)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

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

            // Flow 3 -- Fill in Name, Code, Grade, Expertise Program and
            // Main Subjects.
            {
                content: "Fill in the Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR RCMS Main Subject Create",
            },
            {
                content: "Fill in the Code",
                trigger: ".o_field_widget[name='code']",
                run: "text /",
            },
            {
                content: "Select the Grade",
                trigger: ".o_field_many2one[name='grade_id'] input",
                run: "text TOUR RCMS Grade",
            },
            {
                content: "Pick the Grade from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR RCMS Grade)",
                in_modal: false,
            },
            {
                content: "Fill in the Expertise Program",
                trigger: ".o_field_widget[name='expertise_program']",
                run: "text TOUR RCMS Program",
            },
            {
                content: "Select a Main Subject",
                trigger: ".o_field_many2manytags[name='subject_ids'] input",
                run: "text TOUR RCMS Subject",
            },
            {
                content: "Pick the Main Subject from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR RCMS Subject)",
                in_modal: false,
            },

            // Flow 4 -- Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // Post-Condition -- a new record is created.
            {
                content: "Record is saved",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(TOUR RCMS Main Subject Create)",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
