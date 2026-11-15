/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_school_academic_operating_unit.school_score_sheet_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/school_score_sheet/01-create.md
    // (E1 delta - Additional Fields)
    tour.register(
        "ssi_school_academic_operating_unit_school_score_sheet_field_ou",
        {
            test: true,
            url: "/web",
        },
        [
            // Base Flow 1 - Open the School > Classroom > Score Sheets
            // menu.
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
                // Gate on the TARGET action title, not on any list view.
                content: "School Score Sheets list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(School Score Sheets)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Base Flow 2 - Click the New button. (14.0: "Create")
            {
                content: "Click Create",
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

            // Additional Fields - the Operating Unit field added by
            // mixin.single_operating_unit is rendered on the create form
            // for a user in the multi operating unit group. Delta-only
            // tour: it stops here (Record Visibility is not covered by
            // a tour).
            {
                content: "Operating Unit field is displayed",
                trigger: ".o_field_widget[name='operating_unit_id']",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
