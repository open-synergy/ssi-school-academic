/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_school_academic_operating_unit.school_teaching_assignment_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_teaching_assignment/01-create.md
        // (E1 delta - Additional Fields)
        tour.register(
            "ssi_school_academic_operating_unit_school_teaching_assignment_field_ou",
            {
                test: true,
                url: "/web",
            },
            [
                // Base Flow 1 - Open the School > Configuration >
                // Subject & Scoring > Teaching Assignments menu. "Subject &
                // Scoring" is a level-3 grouping menuitem without action=, so
                // 14.0 renders it as a non-clickable dropdown header and
                // there is no step for it.
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
                    content: "Open the Teaching Assignments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_academic.school_teaching_assignment_menu"]',
                },
                {
                    // Gate on the TARGET action title, not on any list view.
                    content: "Teaching Assignments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Teaching Assignments)",
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

                // Additional Fields - the Operating Units field added by
                // mixin.multiple_operating_unit is rendered on the create form
                // for a user in the multi operating unit group. Delta-only
                // tour: it stops here (Record Visibility is not covered by
                // a tour).
                {
                    content: "Operating Units field is displayed",
                    trigger: ".o_field_widget[name='operating_unit_ids']",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        );
    }
);
