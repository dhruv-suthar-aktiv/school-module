odoo.define('school.my_attendances', function (require) {
"use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var field_utils = require('web.field_utils');

    var HrAttendance = require('hr_attendance.my_attendances');

    HrAttendance.include({
        contentTemplate: 'Hrattendancenew',

        events: {
        "click .o_hr_attendance_sign_in_out_icon": function () {
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'hr.employee',
                res_id: 1,
                views: [[false, 'form']],
                target: 'current'
                });
            },
        },

        willStart: function () {
            console.log("Tghai che")
            var self = this;

            var def = this._rpc({
                    model: 'hr.employee',
                    method: 'search_read',
                    args: [[['user_id', '=', this.getSession().uid]], ['department_id','attendance_state', 'name', 'hours_today']],
                })
                .then(function (res) {
                    console.log(res);
                    self.employee = res.length && res[0];
                    if (res.length) {
                        self.hours_today = field_utils.format.float_time(self.employee.hours_today);
                    }
                });

            return Promise.all([def, this._super.apply(this, arguments)]);
        },



    })
});
