// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.school_score_sheet_enter_scores_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Score cell of the Nth component of the Nth student of the Scores grid.
    // The grid has one row per student and one cell per score component, so
    // a cell is addressed by its row and column position.
    function scoreCell(row, column) {
        return (
            ".o_score_grid_table .o_data_row:eq(" +
            row +
            ") .o_score_grid_cell:eq(" +
            column +
            ")"
        );
    }

    // Input of a score cell.
    function scoreInput(row, column) {
        return scoreCell(row, column) + " input";
    }

    // The table of the grid as it was before the first score was typed.
    var gridTable = null;

    // Remember the table of the grid. A grid that is drawn again replaces
    // its table, so the table is the proof that the grid was left alone.
    function rememberGrid() {
        gridTable = $(".o_score_grid_table")[0];
    }

    // Fail when the grid is another table than the remembered one. This is
    // the regression of the score entry: the whole grid was drawn again
    // after a score was committed, and the focus and the text typed in the
    // next cell were lost with the old table.
    function assertSameGrid() {
        var table = $(".o_score_grid_table")[0];
        if (!table || table !== gridTable) {
            throw new Error("The grid was drawn again after a score was entered.");
        }
    }

    // Fail when the focus is not in the given score cell.
    function assertFocus(row, column) {
        var input = $(scoreInput(row, column))[0];
        if (!input || document.activeElement !== input) {
            throw new Error(
                "The focus is not in the score cell " + row + "/" + column + "."
            );
        }
    }

    // Type like a user does: the cell gets the focus, so the cell that had it
    // loses it, and the browser tells the change of the typed text.
    function typeInCell(input, text) {
        input.focus();
        input.select();
        document.execCommand("insertText", false, text);
    }

    // Step that waits for the end of the commit of a score, the cell of the
    // score turning red (the scores of the tour are below the minimum score
    // of 75), then checks that the grid was left alone and where the focus
    // is. The focus is checked after the wait, not right after the key: a
    // check that is done at once is also true for the grid that is drawn
    // again later.
    function committedStep(content, row, column, focusRow, focusColumn) {
        return {
            content: content,
            trigger: scoreCell(row, column) + ".o_score_grid_below_minimum",
            run: function () {
                assertSameGrid();
                assertFocus(focusRow, focusColumn);
            },
        };
    }

    // Step that types a score in a cell, then presses a key.
    function typeAndPress(content, row, column, text, keyCode) {
        return [
            {
                content: "Type " + text + " in " + content,
                trigger: scoreInput(row, column),
                run: "text " + text,
            },
            {
                content: "Press the key " + keyCode + " in " + content,
                trigger: scoreInput(row, column),
                run: "keydown " + keyCode,
            },
        ];
    }

    // Score of the whole grid, row by row, filled with the Tab key only: a
    // number is typed in the cell, null leaves the cell as it is. The cells
    // that got a score before, in the steps above, keep it.
    var TAB_FILL = [
        [null, null, 80, null, 0, 90, null],
        [85, null, null, 0, null, null, 95],
        [null, null, 72, null, 88, null, null],
        [0, 77, null, null, 66, null, null],
    ];

    // Steps that go over the 28 cells with the Tab key, from the first one.
    function tabFillSteps() {
        var steps = [
            {
                content: "Put the focus in the first score cell",
                trigger: scoreInput(0, 0),
                run: function () {
                    this.$anchor[0].focus();
                },
            },
        ];
        _.each(TAB_FILL, function (scores, row) {
            _.each(scores, function (score, column) {
                var nextIndex = row * scores.length + column + 1;
                var last = nextIndex === TAB_FILL.length * scores.length;
                var next = last
                    ? null
                    : [
                          Math.floor(nextIndex / scores.length),
                          nextIndex % scores.length,
                      ];
                if (score !== null) {
                    steps.push({
                        content: "Type " + score + " in the cell " + row + "/" + column,
                        trigger: scoreInput(row, column),
                        run: "text " + score,
                    });
                }
                steps.push({
                    content: "Press Tab in the cell " + row + "/" + column,
                    trigger: scoreInput(row, column),
                    run: function (actions) {
                        actions.keydown("9");
                        if (last) {
                            // The focus leaves the grid and does not come back
                            // to the first cell.
                            if (
                                $(".o_score_grid_table").has(document.activeElement)
                                    .length
                            ) {
                                throw new Error("The focus stayed in the grid.");
                            }
                        } else {
                            assertFocus(next[0], next[1]);
                        }
                    },
                });
            });
        });
        return steps;
    }

    // IK: docs/school_score_sheet/08-enter-scores.md
    tour.register(
        "ssi_school_academic_school_score_sheet_enter_scores",
        {test: true, url: "/web"},
        [
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
                content: "Score Sheets list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(School Score Sheets)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR SSS Subject ENTER) .o_data_cell:first",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Open the Scores tab",
                trigger: ".o_notebook .nav-link:contains(Scores)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                // The Scores tab is a grid, not a list: one row per student and
                // the calculated columns after the components.
                content: "The Scores tab is a grid with the calculated columns",
                trigger: ".o_score_grid_table .o_score_grid_calculated_header",
                extra_trigger: ".o_score_grid_table .o_data_row:eq(3)",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Remember the table of the grid",
                trigger: ".o_score_grid_table .o_data_row:eq(3)",
                run: function () {
                    rememberGrid();
                },
            },
            // Flow 5: type, then Tab.
        ]
            .concat(typeAndPress("the first score cell", 0, 0, 50, 9))
            .concat([
                committedStep(
                    "The first score is entered and the focus is in the next cell",
                    0,
                    0,
                    0,
                    1
                ),
            ])
            // Flow 6: type, then Enter.
            .concat(typeAndPress("the second score cell", 0, 1, 60, 13))
            .concat([
                committedStep(
                    "The focus is in the cell of the next student",
                    0,
                    1,
                    1,
                    1
                ),
            ])
            // Flow 7: type, then the Down arrow.
            .concat(typeAndPress("the cell of the second student", 1, 1, 65, 40))
            .concat([
                committedStep(
                    "The focus is in the cell of the third student",
                    1,
                    1,
                    2,
                    1
                ),
            ])
            // Flow 8: type, then the Up arrow.
            .concat(typeAndPress("the cell of the third student", 2, 1, 70, 38))
            .concat([
                committedStep(
                    "The focus is back in the cell of the second student",
                    2,
                    1,
                    1,
                    1
                ),
                // Flow 9: type in a cell, click another one, type at once.
                {
                    content: "Type 40 in a cell",
                    trigger: scoreInput(1, 2),
                    run: function () {
                        typeInCell(this.$anchor[0], "40");
                    },
                },
                {
                    // The click moves the focus, which commits the 40, and the
                    // next score is typed before that commit is over.
                    content: "Click another cell and type 30 at once",
                    trigger: scoreInput(2, 3),
                    run: function () {
                        var previous = document.activeElement;
                        if (previous && previous !== this.$anchor[0]) {
                            previous.dispatchEvent(
                                new Event("change", {bubbles: true})
                            );
                        }
                        typeInCell(this.$anchor[0], "30");
                    },
                },
                {
                    content: "The 40 is entered, and the 30 is still in its cell",
                    trigger: scoreCell(1, 2) + ".o_score_grid_below_minimum",
                    run: function () {
                        assertSameGrid();
                        assertFocus(2, 3);
                        if ($(scoreInput(2, 3)).val() !== "30") {
                            throw new Error("The text typed in the cell was lost.");
                        }
                    },
                },
                {
                    content: "Press Tab in the cell of the 30",
                    trigger: scoreInput(2, 3),
                    run: "keydown 9",
                },
                committedStep(
                    "The 30 is entered and the focus is in the next cell",
                    2,
                    3,
                    2,
                    4
                ),
            ])
            // Flow 10: fill the whole grid with the Tab key only.
            .concat(tabFillSteps())
            .concat([
                {
                    // The last typed score is the last commit of the chain.
                    content: "The last typed score is entered and the grid is the same",
                    trigger: scoreCell(3, 4) + ".o_score_grid_below_minimum",
                    run: function () {
                        assertSameGrid();
                    },
                },
                // Flow 11: save.
                {
                    content: "Click the Save button",
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
                    // Post-Condition: a typed number is shown and is red when
                    // it is below the minimum score of 75, and 85 is not.
                    content: "The first score is shown and is red",
                    trigger:
                        scoreCell(0, 0) + ":contains(50).o_score_grid_below_minimum",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    content: "The score of 85 is shown and is not red",
                    trigger:
                        scoreCell(1, 0) +
                        ":contains(85):not(.o_score_grid_below_minimum)",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
                {
                    // Post-Condition: a zero is shown, and is red.
                    content: "The typed zero is shown and is red",
                    trigger: scoreCell(0, 4) + ".o_score_grid_below_minimum",
                    run: function () {
                        var text = this.$anchor.text().trim();
                        if (text === "" || parseFloat(text) !== 0) {
                            throw new Error("The zero is not shown: " + text);
                        }
                    },
                },
                {
                    // Post-Condition: a cell that was only gone over with Tab
                    // stays empty and is never red.
                    content: "The cell that Tab went over stays empty",
                    trigger: scoreCell(0, 3) + ":not(.o_score_grid_below_minimum)",
                    run: function () {
                        if (this.$anchor.text().trim() !== "") {
                            throw new Error("The cell is not empty.");
                        }
                    },
                },
            ])
    );
});
