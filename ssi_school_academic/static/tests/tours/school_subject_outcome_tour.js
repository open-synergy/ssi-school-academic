// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_subject_outcome_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- Flow 1 of every school_subject_outcome IK:
    // "Open the School > Configuration > Subject & Scoring > Subject
    // Outcomes menu." "Subject & Scoring" is a level-3 grouping menuitem
    // without action=, so 14.0 renders it as a non-clickable dropdown
    // header and there is no step for it.
    function openOutcomeList() {
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
                content: "Open the Subject Outcomes menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_subject_outcome_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted.
                content: "Subject Outcomes list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Subject Outcomes)",
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

    // IK: docs/school_subject_outcome/01-create.md
    tour.register(
        "ssi_school_academic_school_subject_outcome_create",
        {test: true, url: "/web"},
        [].concat(
            // Flow 1 -- Open the Subject Outcomes menu.
            openOutcomeList(),
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
                    run: "text TOUR Subject Outcome Create",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },
            ],
            pickMany2one("subject_id", "TOUR SSO Subject"),
            pickMany2one("grade_id", "TOUR SSO Grade"),
            pickMany2one("academic_term_id", "TOUR SSO Term"),
            [
                // Flow 4 -- Open the Learning Objectives tab.
                {
                    content: "Open the Learning Objectives tab",
                    trigger: ".o_notebook .nav-link:contains(Learning Objectives)",
                },

                // Flow 5 -- Add a line and fill it in.
                {
                    content: "Click Add a line",
                    trigger:
                        ".o_field_x2many[name='objective_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    content: "Fill in the Code of the objective",
                    trigger: ".o_selected_row .o_field_widget[name='code']",
                    run: "text TOUR TP 1",
                },
                {
                    content: "Fill in the Description of the objective",
                    trigger: ".o_selected_row .o_field_widget[name='description']",
                    run: "text TOUR objective description",
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
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Subject Outcome Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "The objective is listed",
                    trigger:
                        ".o_field_one2many[name='objective_ids'] .o_data_row:contains(TOUR TP 1)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );
});
