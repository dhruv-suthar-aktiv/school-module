odoo.define('school.practice', function (require) {
"use strict";


var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var QWeb = core.qweb;


var HelloWorld = AbstractAction.extend({
    contentTemplate: 'HelloWorldTemplate',
    events: {
        "click .button_clickable": function () {
            var self = this;
            console.log("Event is calling");
            var def = this._rpc({
                model: 'student.student',
                method: 'search_read',
                args: [
                        [],
                        ["roll_no","name","age","gender","email"],
                    ],
            })
            .then(function (res) {
                console.log("This is student ",res);
                var result = res;
                self.$el.html(QWeb.render('ClickTemplate',{'student':result}));
            });
        },

        "click .back": function(){
            this.$el.html(QWeb.render('HelloWorldTemplate'));
        }
    },

    start: function () {
        console.log("Jagte raho");
    },

});

core.action_registry.add('welcome_action', HelloWorld);

return HelloWorld;

});
