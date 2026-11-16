// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_academic.FieldScoreEntry", function (require) {
    "use strict";

    var basic_fields = require("web.basic_fields");
    var core = require("web.core");
    var field_registry = require("web.field_registry");
    var _lt = core._lt;

    // A Float field reads 0.0 for both an empty score and a zero score. The
    // read-only Boolean field ``is_scored`` of the same line tells them apart,
    // so this widget shows an empty cell while ``is_scored`` is false, and it
    // lets a typed zero count as a change. The shown text of an unscored cell
    // is empty unless the node option ``empty_text`` sets another one.
    var FieldScoreEntry = basic_fields.FieldFloat.extend({
        description: _lt("Score Entry"),
        className: "o_field_float o_field_number o_field_score_entry",
        supportedFieldTypes: ["float"],

        // --------------------------------------------------------------------
        // Public
        // --------------------------------------------------------------------

        /**
         * A scored cell is set, zero included. An unscored cell is not.
         *
         * @override
         * @returns {Boolean}
         */
        isSet: function () {
            return this._isScored();
        },

        // --------------------------------------------------------------------
        // Private
        // --------------------------------------------------------------------

        /**
         * Tell whether the line holds an entered score.
         *
         * @private
         * @returns {Boolean}
         */
        _isScored: function () {
            return Boolean(this.recordData.is_scored);
        },

        /**
         * Show an empty cell, or the ``empty_text`` node option, while the
         * score is not entered.
         *
         * @override
         * @private
         * @returns {String}
         */
        _formatValue: function () {
            if (!this._isScored()) {
                return this.nodeOptions.empty_text || "";
            }
            return this._super.apply(this, arguments);
        },

        /**
         * An empty input means the score is emptied, which is ``false``
         * and not zero, so the server clears ``is_scored``.
         *
         * @override
         * @private
         * @param {String} value
         * @returns {Number|Boolean}
         */
        _parseValue: function (value) {
            if (typeof value === "string" && value.trim() === "") {
                return false;
            }
            return this._super.apply(this, arguments);
        },

        /**
         * While the line is unscored, any entered number is a change, zero
         * included, and an emptied cell is not a change.
         *
         * @override
         * @private
         * @param {Number|Boolean} value
         * @returns {Boolean}
         */
        _isSameValue: function (value) {
            if (!this._isScored()) {
                return value === false;
            }
            return this._super.apply(this, arguments);
        },

        /**
         * Send the score together with the scored flag, so the cell is
         * rendered right before the record is saved. The server computes
         * the flag again on save, this value only serves the client.
         *
         * @override
         * @private
         * @param {String} value
         * @param {Object} [options]
         * @returns {Promise}
         */
        _setValue: function (value, options) {
            if (this._isLastSetValue(value)) {
                return Promise.resolve();
            }
            this.lastSetValue = value;
            var parsed = null;
            try {
                parsed = this._parseValue(value);
                this._isValid = true;
            } catch (e) {
                this._isValid = false;
                this.trigger_up("set_dirty", {dataPointID: this.dataPointID});
                return Promise.reject({message: "Value set is not valid"});
            }
            if (!(options && options.forceChange) && this._isSameValue(parsed)) {
                return Promise.resolve();
            }
            var self = this;
            return new Promise(function (resolve, reject) {
                var changes = {};
                changes[self.name] = parsed;
                changes.is_scored = parsed !== false;
                self.trigger_up("field_changed", {
                    dataPointID: self.dataPointID,
                    changes: changes,
                    viewType: self.viewType,
                    doNotSetDirty: options && options.doNotSetDirty,
                    notifyChange: !options || options.notifyChange !== false,
                    allowWarning: options && options.allowWarning,
                    onSuccess: resolve,
                    onFailure: reject,
                });
            });
        },
    });

    field_registry.add("score_entry", FieldScoreEntry);

    return FieldScoreEntry;
});
