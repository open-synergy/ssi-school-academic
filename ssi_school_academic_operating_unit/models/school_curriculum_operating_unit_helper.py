# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Shared helper deriving ``operating_unit_id`` from ``school_id``.

Plain functions (not an Odoo model) shared by the ``create``, ``write``
and onchange of the school curriculum, so the derivation rule is written
once.
"""


def get_operating_unit_id_from_school(env, school_id):
    """Return the id of the operating unit of a school, if unambiguous.

    A school belongs to exactly one operating unit by design, so the
    operating unit of the school is used whether or not the current
    user holds it. When the school has no operating unit or more than
    one, the rule does not apply and the caller keeps its own value.

    :param env: the current Odoo environment
    :param school_id: id of the ``school`` record, or a falsy value
    :return: id of the ``operating.unit`` record when the school has
        exactly one operating unit; ``None`` otherwise
    """
    if not school_id:
        return None
    # Read with sudo: the school record rule only shows the schools of
    # the operating units of the user, but the operating unit of the
    # school is used whether or not the user holds it. The curriculum
    # record rule decides whether the user may save it.
    school = env["school"].sudo().browse(school_id)
    operating_units = school.operating_unit_ids
    if len(operating_units) == 1:
        return operating_units.id
    return None


def derive_operating_unit_from_school_vals(env, vals):
    """Mutate ``vals`` in place, deriving ``operating_unit_id``.

    Applies only when ``school_id`` is present in ``vals`` and the
    caller has not supplied ``operating_unit_id`` in the same ``vals``;
    an explicit value always wins.

    :param env: the current Odoo environment
    :param vals: the ``create``/``write`` values dict, mutated in place
    :return: None
    """
    if "school_id" not in vals or "operating_unit_id" in vals:
        return
    operating_unit_id = get_operating_unit_id_from_school(env, vals.get("school_id"))
    if operating_unit_id:
        vals["operating_unit_id"] = operating_unit_id
