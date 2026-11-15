# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Academic",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    # pylint: disable=line-too-long
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia, Odoo Community Association (OCA)",  # noqa: B950
    # pylint: enable=line-too-long
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school",
        "ssi_master_data_mixin",
        "web_tour",
    ],
    "data": [
        "security/res_groups/school_subject.xml",
        "security/res_groups/school_score_component.xml",
        "security/ir_model_access/school_subject.xml",
        "security/ir_model_access/school_score_component.xml",
        "views/school_subject.xml",
        "views/school_score_component.xml",
        "views/assets.xml",
    ],
    "demo": [],
}
