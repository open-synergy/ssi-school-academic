// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_score_predicate_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- Flow 1 of every
    // school_score_predicate IK: "Open the School > Configuration > Subject &
    // Scoring > Score Predicates menu." "Subject & Scoring"
    // (ssi_school.menu_subject_configuration) is a level-3 grouping
    // menuitem with no action= attribute, so 14.0 renders it as a
    // non-clickable dropdown header without data-menu-xmlid -- there is no
    // step for it.
    function openPredicateList() {
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
                content: "Open the Score Predicates menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_score_predicate_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted, not just
                // for "some list is on screen".
                content: "Score Predicates list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Score Predicates)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Open the record whose exact Name cell matches.
    function openRecord(name) {
        return [
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:has(.o_data_cell.o_list_char[title='" +
                    name +
                    "']) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/school_score_predicate/01-create.md
    tour.register(
        "ssi_school_academic_school_score_predicate_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Score Predicates menu.
            openPredicateList(),
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

                // Flow 3 -- Fill in Name and Code.
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR Predicate Create",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },

                // Flow 4 -- On the Applicability tab, select an Applicable Grade.
                {
                    content: "Select an Applicable Grade",
                    trigger: ".o_field_many2manytags[name='grade_ids'] input",
                    run: "text TOUR Predicate Grade Create",
                },
                {
                    content: "Pick the Applicable Grade from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR Predicate Grade Create)",
                    in_modal: false,
                },

                // Flow 5 -- On the Predicate Lines tab, add a line.
                {
                    content: "Open the Predicate Lines tab",
                    trigger: ".o_notebook .nav-link:contains(Predicate Lines)",
                },
                {
                    content: "Click Add a line",
                    trigger:
                        ".o_field_x2many[name='line_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    content: "Fill in the Predicate of the line",
                    trigger: ".o_selected_row .o_field_widget[name='name']",
                    run: "text A",
                },
                {
                    content: "Fill in the Description of the line",
                    trigger: ".o_selected_row .o_field_widget[name='description']",
                    run: "text Very Good",
                },
                {
                    content: "Fill in the Minimum Score of the line",
                    trigger: ".o_selected_row .o_field_widget[name='min_score']",
                    run: "text 90",
                },

                // Flow 6 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- a new Score Predicate record is created.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Predicate Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_score_predicate/02-edit.md
    tour.register(
        "ssi_school_academic_school_score_predicate_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Score Predicates menu.
            openPredicateList(),
            // Flow 2 -- Find and open the record to edit.
            openRecord("TOUR Predicate Edit"),
            [
                {
                    content: "Click the Edit button",
                    trigger: ".o_form_button_edit",
                },
                {
                    content: "Form is now editable",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 -- Change the Name.
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR Predicate Edit Changed",
                },

                // Flow 4 -- On the Predicate Lines tab, change the score.
                {
                    content: "Open the Predicate Lines tab",
                    trigger: ".o_notebook .nav-link:contains(Predicate Lines)",
                },
                {
                    // Column 2 = min_score (tree: name, description, min_score);
                    // a 14.0 <td> has no name attribute.
                    content: "Click the Minimum Score cell of the line",
                    trigger:
                        ".o_field_x2many[name='line_ids'] .o_data_row:first .o_data_cell:eq(2)",
                },
                {
                    content: "Change the Minimum Score of the line",
                    trigger: ".o_selected_row .o_field_widget[name='min_score']",
                    run: "text 85",
                },

                // Flow 5 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- the record is updated.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Predicate Edit Changed)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_score_predicate/03-archive.md
    tour.register(
        "ssi_school_academic_school_score_predicate_archive",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Score Predicates menu.
            openPredicateList(),
            [
                // Flow 2 -- Select the record to archive.
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:has(.o_data_cell.o_list_char[title='TOUR Predicate Archive']) .o_list_record_selector input",
                    run: "click",
                },

                // Flow 3 -- Click Action > Archive.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Archive",
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $archive = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Archive";
                            }
                        );
                        $archive[0].click();
                    },
                },

                // Flow 4 -- Click OK to confirm.
                {
                    content: "Confirm archive",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- the record no longer appears in the
                // default list view.
                {
                    content: "Record no longer in the default list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_cell.o_list_char[title='TOUR Predicate Archive']))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );
});
