// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_report_card_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- Flow 1 of every
    // school_report_card_type IK: "Open the School > Configuration > Subject &
    // Scoring > Report Card Types menu." "Subject & Scoring"
    // (ssi_school.menu_subject_configuration) is a level-3 grouping
    // menuitem with no action= attribute, so 14.0 renders it as a
    // non-clickable dropdown header without data-menu-xmlid -- there is no
    // step for it.
    function openReportCardTypeList() {
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
                content: "Open the Report Card Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_report_card_type_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be mounted, not just
                // for "some list is on screen".
                content: "Report Card Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Report Card Types)",
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

    // IK: docs/school_report_card_type/01-create.md
    tour.register(
        "ssi_school_academic_school_report_card_type_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Report Card Types menu.
            openReportCardTypeList(),
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

                // Flow 3 -- Fill in Name, Code and Term Type.
                {
                    content: "Fill in the Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR Report Card Type Create",
                },
                {
                    content: "Fill in the Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },
                {
                    // 14.0: a selection <select> carries o_field_widget itself.
                    content: "Select the Term Type",
                    trigger: "select.o_field_widget[name='term_type']",
                    run: "text Mid-Term",
                },

                // Flow 4 -- On the Calculation tab, set the average. The
                // Calculation page is the first page of the notebook, so it is
                // already displayed.
                {
                    content: "Select the first Averaged Component",
                    trigger:
                        ".o_field_many2manytags[name='average_component_ids'] input",
                    run: "text TOUR RCT UH 1",
                },
                {
                    content: "Pick the first Averaged Component from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR RCT UH 1)",
                    in_modal: false,
                },
                {
                    // Gate: adding a tag re-renders the many2many_tags input;
                    // wait until the first tag badge is rendered before typing.
                    content: "First Averaged Component tag is rendered",
                    trigger:
                        ".o_field_many2manytags[name='average_component_ids'] .o_badge_text:contains(TOUR RCT UH 1)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Select the second Averaged Component",
                    trigger:
                        ".o_field_many2manytags[name='average_component_ids'] input",
                    extra_trigger:
                        ".o_field_many2manytags[name='average_component_ids'] .o_badge_text:contains(TOUR RCT UH 1)",
                    run: "text TOUR RCT Task 1",
                },
                {
                    content: "Pick the second Averaged Component from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR RCT Task 1)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Average Weight",
                    trigger: ".o_field_widget[name='average_weight']",
                    run: "text 70",
                },

                // Flow 5 -- Add a weight line.
                {
                    content: "Click Add a line",
                    trigger:
                        ".o_field_x2many[name='weight_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    content: "Select the Component of the line",
                    trigger:
                        ".o_selected_row .o_field_many2one[name='component_id'] input",
                    run: "text TOUR RCT PTS",
                },
                {
                    content: "Pick the Component of the line from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR RCT PTS)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Weight of the line",
                    trigger: ".o_selected_row .o_field_widget[name='weight']",
                    run: "text 30",
                },

                // Flow 6 -- Optional Display tab: not exercised.

                // Flow 7 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- a new Report Card Type record is created.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Report Card Type Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_report_card_type/02-edit.md
    tour.register(
        "ssi_school_academic_school_report_card_type_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Report Card Types menu.
            openReportCardTypeList(),
            // Flow 2 -- Find and open the record to edit.
            openRecord("TOUR Report Card Type Edit"),
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
                    run: "text TOUR Report Card Type Edit Changed",
                },

                // Flow 4 -- On the Calculation tab, change the threshold.
                {
                    content: "Change the Rounding Threshold",
                    trigger: ".o_field_widget[name='rounding_threshold']",
                    run: "text 0.6",
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
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR Report Card Type Edit Changed)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );

    // IK: docs/school_report_card_type/03-archive.md
    tour.register(
        "ssi_school_academic_school_report_card_type_archive",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Report Card Types menu.
            openReportCardTypeList(),
            [
                // Flow 2 -- Select the record to archive.
                {
                    content: "Select the record's checkbox",
                    trigger:
                        ".o_data_row:has(.o_data_cell.o_list_char[title='TOUR Report Card Type Archive']) .o_list_record_selector input",
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
                        ".o_list_view:not(:has(.o_data_cell.o_list_char[title='TOUR Report Card Type Archive']))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );
});
