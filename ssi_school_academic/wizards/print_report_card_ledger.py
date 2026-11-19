# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_compare, float_round

# Digits used to compare two scores and two totals.
SCORE_DIGITS = 4


class PrintReportCardLedger(models.TransientModel):
    """Builds and prints the score ledger of one class.

    The user picks a grade class, an academic term and a report card
    type. The ledger lists one row for every enrollment of the class
    and the term that is on progress or done, and one column for every
    subject found on the non-cancelled report cards of that type. Only
    the report cards that are done give a score to a cell. The total,
    the average and the rank of every row are computed here; the rank
    breaks a tie of the total with the main subjects of the class and
    then with all the subjects.
    """

    _name = "print_report_card_ledger"
    _description = "Print Report Card Ledger"

    grade_class_id = fields.Many2one(
        string="Grade Class",
        comodel_name="school_grade_class",
        required=True,
        ondelete="cascade",
        help="Class whose students are listed on the ledger.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        ondelete="cascade",
        help="Academic term of the enrollments listed on the ledger.",
    )
    type_id = fields.Many2one(
        string="Report Card Type",
        comodel_name="school_report_card_type",
        required=True,
        ondelete="cascade",
        help="Type of the report cards whose scores fill the ledger.",
    )
    line_ids = fields.One2many(
        string="Rows",
        comodel_name="print_report_card_ledger_line",
        inverse_name="wizard_id",
        help="Student rows of the ledger.",
    )
    subject_ids = fields.One2many(
        string="Columns",
        comodel_name="print_report_card_ledger_subject",
        inverse_name="wizard_id",
        help="Subject columns of the ledger.",
    )

    def action_compute(self):
        """Rebuild the rows, the columns and the cells of the ledger.

        Nothing is returned, the ledger is read back from its rows.
        """
        for record in self.sudo():
            record._compute_ledger()

    def action_show(self):
        """Rebuild the ledger and show it on screen.

        :return: the ``ir.actions.report`` dict of the HTML ledger
        """
        for record in self.sudo():
            result = record._show_ledger()
        return result

    def action_print(self):
        """Rebuild the ledger and print it as a PDF file.

        :return: the ``ir.actions.report`` dict of the PDF ledger
        """
        for record in self.sudo():
            result = record._print_ledger()
        return result

    def _show_ledger(self):
        """Rebuild the ledger and build the action of its HTML report.

        :return: the ``ir.actions.report`` dict of the HTML ledger
        """
        self.ensure_one()
        self._compute_ledger()
        report = self.env.ref(
            "ssi_school_academic.report_print_report_card_ledger_html"
        )
        return report.report_action(self)

    def _print_ledger(self):
        """Rebuild the ledger and build the action of its PDF report.

        :return: the ``ir.actions.report`` dict of the PDF ledger
        """
        self.ensure_one()
        self._compute_ledger()
        report = self.env.ref("ssi_school_academic.report_print_report_card_ledger_pdf")
        return report.report_action(self)

    def _compute_ledger(self):
        """Rebuild the rows, the columns and the cells of the ledger.

        Side effect: deletes the current rows and columns of the
        ledger, then creates new ones. The enrollments are read with
        full rights, the report cards are read with the rights of the
        user, so the record rules of the report card still apply.
        """
        self.ensure_one()
        self.line_ids.unlink()
        self.subject_ids.unlink()
        enrollments = self._get_ledger_enrollments()
        cards = self._get_ledger_report_cards(enrollments)
        subjects = self._get_ledger_subjects(cards)
        rows = self._prepare_ledger_rows(enrollments, cards, subjects)
        ranks = self._get_ledger_ranks(rows, subjects)
        self._create_ledger_rows(rows, ranks, subjects)
        self._create_ledger_subjects(rows, subjects)

    def _get_ledger_enrollments(self):
        """Return the enrollments listed on the ledger.

        :return: enrollments of the class and the term that are on
            progress or done, sorted by the name of the student
        :rtype: recordset of ``school_enrollment``
        """
        self.ensure_one()
        enrollments = self.env["school_enrollment"].search(
            [
                ("grade_class_id", "=", self.grade_class_id.id),
                ("academic_term_id", "=", self.academic_term_id.id),
                ("state", "in", ["open", "done"]),
            ]
        )
        return enrollments.sorted(lambda r: (r.student_id.name or "", r.id))

    def _get_ledger_report_cards(self, enrollments):
        """Return the report cards the ledger reads, by enrollment.

        The report cards are read with the rights of the user, so a
        report card the user may not read is not on the ledger.

        :param enrollments: enrollments listed on the ledger
        :return: the non-cancelled report card of the selected type of
            every enrollment that has one
        :rtype: dict of enrollment id to ``school_report_card``
        """
        self.ensure_one()
        cards = self.env(su=False)["school_report_card"].search(
            [
                ("enrollment_id", "in", enrollments.ids),
                ("type_id", "=", self.type_id.id),
                ("state", "!=", "cancel"),
            ]
        )
        result = {}
        for card in cards.sorted("id"):
            result.setdefault(card.enrollment_id.id, card)
        return result

    def _get_ledger_subjects(self, cards):
        """Return the subjects that make the columns of the ledger.

        :param cards: report cards of the ledger, by enrollment id
        :return: subjects of the lines of those report cards, in the
            order of the subject model
        :rtype: recordset of ``school_subject``
        """
        self.ensure_one()
        subject_ids = set()
        for card in cards.values():
            subject_ids |= set(card.line_ids.mapped("subject_id").ids)
        return self.env["school_subject"].search([("id", "in", list(subject_ids))])

    def _prepare_ledger_rows(self, enrollments, cards, subjects):
        """Read the score of every enrollment and every subject.

        A subject is scored for an enrollment only when its report
        card is done and the line of the subject is scored.

        :param enrollments: enrollments listed on the ledger
        :param cards: report cards of the ledger, by enrollment id
        :param subjects: subjects that make the columns
        :return: one dict per enrollment with the keys ``enrollment``,
            ``scores`` (subject id to score, ``None`` when not
            scored), ``below`` (ids of the subjects below the minimum
            score), ``total`` and ``average``
        :rtype: list of dict
        """
        self.ensure_one()
        rows = []
        for enrollment in enrollments:
            card = cards.get(enrollment.id)
            lines = {}
            if card and card.state == "done":
                lines = {
                    line.subject_id.id: line for line in card.line_ids if line.is_scored
                }
            scores = {}
            below = set()
            for subject in subjects:
                line = lines.get(subject.id)
                if line is None:
                    scores[subject.id] = None
                    continue
                scores[subject.id] = line.final_score
                if line.minimum_score > 0 and (
                    float_compare(
                        line.final_score,
                        line.minimum_score,
                        precision_digits=SCORE_DIGITS,
                    )
                    < 0
                ):
                    below.add(subject.id)
            values = [score for score in scores.values() if score is not None]
            rows.append(
                {
                    "enrollment": enrollment,
                    "scores": scores,
                    "below": below,
                    "total": sum(values),
                    "average": sum(values) / len(values) if values else 0.0,
                }
            )
        return rows

    @api.model
    def _get_ledger_wins(self, key, group, subject_ids, scores):
        """Count how often a row scores higher than the rest of a group.

        For every other row of the group and every subject, one point
        is given when the row has a score higher than the other row.
        A subject without score loses against any score and ties with
        another subject without score.

        :param key: key of the row in ``scores``
        :param group: keys of the rows that are compared
        :param subject_ids: ids of the subjects that are compared
        :param scores: subject id to score, by row key
        :return: number of points of the row
        :rtype: int
        """
        wins = 0
        mine = scores[key]
        for other in group:
            if other == key:
                continue
            theirs = scores[other]
            for subject_id in subject_ids:
                left = mine.get(subject_id)
                right = theirs.get(subject_id)
                if left is None:
                    continue
                if right is None or (
                    float_compare(left, right, precision_digits=SCORE_DIGITS) > 0
                ):
                    wins += 1
        return wins

    @api.model
    def _split_ledger_tie(self, group, subject_ids, scores):
        """Split a group of tied rows by the points they win.

        :param group: keys of the tied rows
        :param subject_ids: ids of the subjects that are compared
        :param scores: subject id to score, by row key
        :return: sub groups, the ones with most points first; the rows
            of a sub group are still tied
        :rtype: list of list
        """
        buckets = {}
        for key in group:
            wins = self._get_ledger_wins(key, group, subject_ids, scores)
            buckets.setdefault(wins, []).append(key)
        return [buckets[wins] for wins in sorted(buckets, reverse=True)]

    def _get_ledger_ranks(self, rows, subjects):
        """Compute the rank of every row that has a score.

        The rows are ordered by total, the highest first. A tie of the
        total is broken by the points won on the main subjects of the
        class (skipped when the class has none), and the rows that are
        still tied by the points won on all the subjects against each
        other. Rows still tied share one rank and the next rank skips
        the shared positions.

        :param rows: rows built by ``_prepare_ledger_rows``
        :param subjects: subjects that make the columns
        :return: rank by enrollment id, for the rows with a score only
        :rtype: dict
        """
        self.ensure_one()
        main_ids = (
            self.env["school_report_card_main_subject"]
            ._get_main_subjects(self.grade_class_id)
            .ids
        )
        all_ids = subjects.ids
        scores = {}
        totals = {}
        for row in rows:
            key = row["enrollment"].id
            scored = [s for s in row["scores"].values() if s is not None]
            if not scored:
                continue
            scores[key] = row["scores"]
            totals[key] = float_round(row["total"], precision_digits=SCORE_DIGITS)
        buckets = {}
        for key, total in totals.items():
            buckets.setdefault(total, []).append(key)
        ranks = {}
        position = 1
        for total in sorted(buckets, reverse=True):
            classes = [buckets[total]]
            if len(buckets[total]) > 1 and main_ids:
                classes = self._split_ledger_tie(buckets[total], main_ids, scores)
            tied = []
            for group in classes:
                if len(group) > 1:
                    tied.extend(self._split_ledger_tie(group, all_ids, scores))
                else:
                    tied.append(group)
            for group in tied:
                for key in group:
                    ranks[key] = position
                position += len(group)
        return ranks

    def _create_ledger_rows(self, rows, ranks, subjects):
        """Create the rows and the cells of the ledger.

        Rows with a score come first, ordered by rank and then by the
        name of the student. Rows without a score come last.

        :param rows: rows built by ``_prepare_ledger_rows``
        :param ranks: rank by enrollment id
        :param subjects: subjects that make the columns
        :return: nothing
        """
        self.ensure_one()
        ordered = sorted(
            enumerate(rows),
            key=lambda item: (
                0 if item[1]["enrollment"].id in ranks else 1,
                ranks.get(item[1]["enrollment"].id, 0),
                item[0],
            ),
        )
        for number, (_index, row) in enumerate(ordered, start=1):
            enrollment = row["enrollment"]
            has_score = enrollment.id in ranks
            cells = []
            for sequence, subject_id in enumerate(subjects.ids, 1):
                score = row["scores"].get(subject_id)
                cells.append(
                    (
                        0,
                        0,
                        {
                            "sequence": sequence,
                            "subject_id": subject_id,
                            "has_score": score is not None,
                            "score": score or 0.0,
                            "is_below_minimum": subject_id in row["below"],
                        },
                    )
                )
            self.env["print_report_card_ledger_line"].create(
                {
                    "wizard_id": self.id,
                    "sequence": number,
                    "enrollment_id": enrollment.id,
                    "has_score": has_score,
                    "total": row["total"] if has_score else 0.0,
                    "average": row["average"] if has_score else 0.0,
                    "rank": ranks.get(enrollment.id, 0),
                    "cell_ids": cells,
                }
            )

    def _create_ledger_subjects(self, rows, subjects):
        """Create the subject columns with the average of each column.

        :param rows: rows built by ``_prepare_ledger_rows``
        :param subjects: subjects that make the columns
        :return: nothing
        """
        self.ensure_one()
        for sequence, subject in enumerate(subjects, start=1):
            values = [
                row["scores"][subject.id]
                for row in rows
                if row["scores"].get(subject.id) is not None
            ]
            self.env["print_report_card_ledger_subject"].create(
                {
                    "wizard_id": self.id,
                    "sequence": sequence,
                    "subject_id": subject.id,
                    "has_average": bool(values),
                    "average": sum(values) / len(values) if values else 0.0,
                }
            )
