# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.17.2 -> 14.0.1.18.0
#
# Changes: a score sheet gets a lock per score column, and the report
#          card reads the locked columns instead of the sheets that are
#          done, and prints a copy of the scores. Existing data must
#          keep working: every column that has lines gets a record, the
#          columns of the sheets that were finished or waiting for
#          approval are locked, and every report card gets its copy.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Create the column records, lock them and copy the scores.

    Every step can run twice: the column records and the copies are only
    inserted when they are missing, and the locks are only set.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; writes ``school_score_sheet_component``,
        ``school_score_sheet_line`` and
        ``school_report_card_line_score``
    """
    cr = env.cr
    # 1. A column record for every component that has lines.
    openupgrade.logged_query(
        cr,
        """
        INSERT INTO school_score_sheet_component
            (sheet_id, component_id, is_locked, create_uid, create_date,
             write_uid, write_date)
        SELECT DISTINCT line.sheet_id, line.component_id, FALSE,
               1, NOW() AT TIME ZONE 'UTC', 1, NOW() AT TIME ZONE 'UTC'
        FROM school_score_sheet_line line
        WHERE NOT EXISTS (
            SELECT 1
            FROM school_score_sheet_component existing
            WHERE existing.sheet_id = line.sheet_id
            AND existing.component_id = line.component_id
        )
        """,
    )
    # 2. Sheets that passed the old confirm rule are locked: without
    # this, approving them would give a done sheet with open columns.
    openupgrade.logged_query(
        cr,
        """
        UPDATE school_score_sheet_component col
        SET is_locked = TRUE
        FROM school_score_sheet sheet
        WHERE sheet.id = col.sheet_id
        AND sheet.state IN ('confirm', 'done')
        AND col.is_locked IS NOT TRUE
        """,
    )
    # 3. The lock of a line follows its column (stored computed field).
    openupgrade.logged_query(
        cr,
        """
        UPDATE school_score_sheet_line line
        SET is_locked = TRUE
        FROM school_score_sheet_component col
        WHERE col.sheet_id = line.sheet_id
        AND col.component_id = line.component_id
        AND col.is_locked
        AND line.is_locked IS NOT TRUE
        """,
    )
    # 4. The copy of the scores of every report card that is not
    # cancelled, the finished ones included, so they still print.
    openupgrade.logged_query(
        cr,
        """
        INSERT INTO school_report_card_line_score
            (line_id, component_id, score, create_uid, create_date,
             write_uid, write_date)
        SELECT DISTINCT ON (card_line.id, sheet_line.component_id)
               card_line.id, sheet_line.component_id, sheet_line.score,
               1, NOW() AT TIME ZONE 'UTC', 1, NOW() AT TIME ZONE 'UTC'
        FROM school_report_card_line card_line
        JOIN school_report_card card
            ON card.id = card_line.report_card_id
        JOIN school_score_sheet sheet
            ON sheet.subject_id = card_line.subject_id
            AND sheet.academic_term_id = card.academic_term_id
        JOIN school_score_sheet_line sheet_line
            ON sheet_line.sheet_id = sheet.id
            AND sheet_line.enrollment_id = card.enrollment_id
        WHERE card.state != 'cancel'
        AND sheet.state != 'cancel'
        AND sheet_line.is_scored
        AND sheet_line.is_locked
        AND NOT EXISTS (
            SELECT 1
            FROM school_report_card_line_score existing
            WHERE existing.line_id = card_line.id
        )
        ORDER BY card_line.id, sheet_line.component_id, sheet.id
        """,
    )
    _logger.info("Score columns and report card copies migrated.")
