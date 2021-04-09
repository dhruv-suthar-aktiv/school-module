odoo.define('school.sales_report', function (require) {
"use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;

    var SalesReport = AbstractAction.extend({
        contentTemplate: 'SalesReportDashboard',

         events: {
            "click .button_clickable": function () {
                self=this;
                var confirmed_orders = this._rpc({
                model: 'testing.testing',
                method: 'get_dashboard_data',
                args: [
                        [],
                    ],
                })
                .then(function (res) {
                    // var result = res;
                    console.log("--------",res)
                    var result = res
                    self.$el.html(QWeb.render('SalesReportDashboard2',{'result':result}));

                });
            },
        }
    });

    core.action_registry.add('sale_report', SalesReport);

    return SalesReport;

});
