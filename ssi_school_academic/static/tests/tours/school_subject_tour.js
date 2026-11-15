// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_subject_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- Flow 1 of every
    // school_subject IK: "Open the School > Configuration > Subject &
    // Scoring > Subjects menu." "Subject & Scoring"
    // (ssi_school.menu_subject_configuration) is a level-3 grouping
    // menuitem with no action= attribute, so 14.0 renders it as a
    // non-clickable dropdown header without data-menu-xmlid -- there is no
    // step for it.
    function openSubjectList() {
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
                content: "Open the Subjects menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_subject_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted, not just
                // for "some list is on screen".
                content: "Subjects list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Subjects)",
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

    // IK: docs/school_subject/01-create.md
    tour.register(
        "ssi_school_academic_school_subject_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Subjects menu.
            openSubjectList(),
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
                    run: "text TOUR Subject Create",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },

                // Flow 4 -- On the Applicability tab, keep the default
                // Subject Group and select an Applicable Grade.
                {
                    content: "Select an Applicable Grade",
                    trigger: ".o_field_many2manytags[name='grade_ids'] input",
                    run: "text TOUR Subject Grade Create",
                },
                {
                    content: "Pick the Applicable Grade from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR Subject Grade Create)",
                    in_modal: false,
                },

                // Flow 5 -- On the Minimum Score tab, add a line.
                {
                    content: "Open the Minimum Score tab",
                    trigger: ".o_notebook .nav-link:contains(Minimum Score)",
                },
                {
                    content: "Click Add a line",
                    trigger:
                        ".o_field_x2many[name='minimum_score_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    content: "Select the Grade of the line",
                    trigger: ".o_selected_row .o_field_many2one[name='grade_id'] input",
                    run: "text TOUR Subject Grade Create",
                },
                {
                    content: "Pick the Grade of the line from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR Subject Grade Create)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Minimum Score of the line",
                    trigger: ".o_selected_row .o_field_widget[name='minimum_score']",
                    run: "text 75",
                },

                // Flow 6 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- a new Subject record is created.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Subject Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_subject/02-edit.md
    tour.register(
        "ssi_school_academic_school_subject_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Subjects menu.
            openSubjectList(),
            // Flow 2 -- Find and open the record to edit.
            openRecord("TOUR Subject Edit"),
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
                    run: "text TOUR Subject Edit Changed",
                },

                // Flow 4 -- On the Minimum Score tab, change the score.
                {
                    content: "Open the Minimum Score tab",
                    trigger: ".o_notebook .nav-link:contains(Minimum Score)",
                },
                {
                    // Column 1 = minimum_score (tree: grade_id, minimum_score);
                    // a 14.0 <td> has no name attribute.
                    content: "Click the Minimum Score cell of the line",
                    trigger:
                        ".o_field_x2many[name='minimum_score_ids'] .o_data_row:first .o_data_cell:eq(1)",
                },
                {
                    content: "Change the Minimum Score of the line",
                    trigger: ".o_selected_row .o_field_widget[name='minimum_score']",
                    run: "text 80",
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
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Subject Edit Changed)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_subject/03-archive.md
    tour.register(
        "ssi_school_academic_school_subject_archive",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Subjects menu.
            openSubjectList(),
            [
                // Flow 2 -- Select the record to archive.
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:has(.o_data_cell.o_list_char[title='TOUR Subject Archive']) .o_list_record_selector input",
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
                        ".o_list_view:not(:has(.o_data_cell.o_list_char[title='TOUR Subject Archive']))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );
});
