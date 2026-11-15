// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_score_component_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- Flow 1 of every
    // school_score_component IK: "Open the School > Configuration > Subject &
    // Scoring > Score Components menu." "Subject & Scoring"
    // (ssi_school.menu_subject_configuration) is a level-3 grouping
    // menuitem with no action= attribute, so 14.0 renders it as a
    // non-clickable dropdown header without data-menu-xmlid -- there is no
    // step for it.
    function openComponentList() {
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
                content: "Open the Score Components menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_score_component_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted, not just
                // for "some list is on screen".
                content: "Score Components list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Score Components)",
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

    // IK: docs/school_score_component/01-create.md
    tour.register(
        "ssi_school_academic_school_score_component_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Score Components menu.
            openComponentList(),
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

                // Flow 3 -- Fill in Name, Code, Category and Sequence.
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR Score Component Create",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },
                {
                    // 14.0: a selection <select> carries o_field_widget itself.
                    content: "Select the Category",
                    trigger: "select.o_field_widget[name='category']",
                    run: "text Final Exam",
                },
                {
                    content: "Fill in the Sequence",
                    trigger: ".o_field_widget[name='sequence']",
                    run: "text 40",
                },

                // Flow 4 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- a new Score Component record is created.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Score Component Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_score_component/02-edit.md
    tour.register(
        "ssi_school_academic_school_score_component_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Score Components menu.
            openComponentList(),
            // Flow 2 -- Find and open the record to edit.
            openRecord("TOUR Score Component Edit"),
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

                // Flow 3 -- Change the Name and the Sequence.
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR Score Component Edit Changed",
                },
                {
                    content: "Change the Sequence",
                    trigger: ".o_field_widget[name='sequence']",
                    run: "text 5",
                },

                // Flow 4 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- the record is updated.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Score Component Edit Changed)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_score_component/03-archive.md
    tour.register(
        "ssi_school_academic_school_score_component_archive",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Score Components menu.
            openComponentList(),
            [
                // Flow 2 -- Select the record to archive.
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:has(.o_data_cell.o_list_char[title='TOUR Score Component Archive']) .o_list_record_selector input",
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
                        ".o_list_view:not(:has(.o_data_cell.o_list_char[title='TOUR Score Component Archive']))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );
});
