# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School Academic - Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    # pylint: disable=line-too-long
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia, Odoo Community Association (OCA)",  # noqa: B950
    # pylint: enable=line-too-long
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_academic",
        "ssi_operating_unit_mixin",
        "web_tour",
    ],
    "data": [
        "security/res_groups/school_score_sheet.xml",
        "security/res_groups/school_report_card.xml",
        "security/ir_rule/school_score_sheet.xml",
        "security/ir_rule/school_report_card.xml",
        "views/school_score_sheet.xml",
        "views/school_report_card.xml",
        "views/assets.xml",
    ],
    "demo": [],
}
