# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.11.1 -> 14.0.1.12.0
#
# Changes: ``display_component_ids`` of ``school_report_card_type`` was a
#          stored many2many and is now a computed field fed by the new
#          ``school_report_card_type_print_column`` lines. The old
#          relation rows would be ignored, so every pair becomes one
#          printed column and the printed report card stays the same.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

OLD_RELATION = "school_report_card_type_display_component_rel"


@openupgrade.migrate()
def migrate(env, version):
    """Copy the old displayed components into printed column lines.

    Components keep the order they had before (component sequence, then
    id) and only the first four are copied, as the old print did. A
    report card type that already has printed columns is skipped, so the
    script can run twice.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; inserts rows into
        ``school_report_card_type_print_column``
    """
    cr = env.cr
    if not openupgrade.table_exists(cr, OLD_RELATION):
        _logger.info("Table %s not found, nothing to migrate.", OLD_RELATION)
        return
    rows = openupgrade.logged_query(
        cr,
        """
        INSERT INTO school_report_card_type_print_column
            (type_id, component_id, sequence, create_uid, create_date,
             write_uid, write_date)
        SELECT ranked.type_id, ranked.component_id, ranked.position * 10,
               1, NOW() AT TIME ZONE 'UTC', 1, NOW() AT TIME ZONE 'UTC'
        FROM (
            SELECT rel.type_id, rel.component_id,
                   ROW_NUMBER() OVER (
                       PARTITION BY rel.type_id
                       ORDER BY comp.sequence, comp.id
                   ) AS position
            FROM school_report_card_type_display_component_rel rel
            JOIN school_score_component comp ON comp.id = rel.component_id
        ) ranked
        WHERE ranked.position <= 4
        AND NOT EXISTS (
            SELECT 1
            FROM school_report_card_type_print_column existing
            WHERE existing.type_id = ranked.type_id
        )
        """,
    )
    _logger.info("Created %s printed column line(s) from the old relation.", rows)
