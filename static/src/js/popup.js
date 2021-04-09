odoo.define("school.popupjs", function(require) {
    "use strict";

    var ajax = require("web.ajax");
    var core=require("web.core");
    var Widget = require("web.Widget");
    var rpc = require("web.rpc");
    var Dialog = require('web.Dialog');
    var _t = core._t;


    $(document).ready(function() {
        console.log("aagaaya");
        // $('.carousel').carousel({
        //  interval: 2000
        // });

        // Job application js for editing the data through js
        $(".edit").click(function(event) {
            $("#modaleditapp").modal("show");
             var request_id = parseInt(
                $(event.target)
                    .parents("tr")
                    .find("td:nth-child(1) span")
                    .html(),
                10
            );
            console.log("Hello this is id of current block",request_id);
            rpc.query({
                model: "job.application",
                method: "search_read",
                args: [
                    [["id", "=", request_id]],
                    [
                        "id",
                        "name",
                        "dob",
                        "email",
                        "gender",
                    ],
                ],
            }).then(function(data) {
                console.log("THis is the data",data)
                $(".name").val(data[0]['name']);
                $(".dob").val(data[0]['dob']);
                $(".email").val(data[0]['email']);
                $("#gender").val(data[0]['gender']);
                $("#application_id").val(data[0]['id']);

            });
        });


        // Student js for creating the student record
        $(".submit-student").click(function(event) {
            var self = $(this);
            var name = $('.name').val();
            var dob = $('.dob').val();
            var age = $('.age').val();
            var gender = $('#gender').val();
            // console.log("name len",name.length)
            // console.log("name",name)
            // console.log("dob len",dob.length)
            // console.log("dob",dob)


            if (dob.length > 0 && name.length > 0 && gender.length >0 ){
                 console.log("--------In the if statement-------")
                $.ajax({
                    url:"/create-student/",
                    method:"POST",
                    dataType: 'json',
                    contentType: "application/json; charset=utf-8",

                    cache: true,
                    async:false,
                    data: JSON.stringify(
                                    {
                                        'jsonrpc': "2.0",
                                        'method': "call",
                                        "params":{
                                            'name': name,
                                            'student_dob': dob,
                                            'gender':gender,
                                            'email':'hello@xyz.com',
                                        }
                                    }),
                    success: function () {
                        console.error("SUCCESS");
                    },
                    error: function (data) {
                        console.error("ERROR ", data);
                    },
                }).then(function (data){
                        window.location.href = '/my/students'
                });

                return true
            }
            else if (name.length <= 0 ) {
                Dialog.alert(self, _t("Please Enter the name."), {
                    title: _t('Name Alert'),
                });
                return false
            }
            else if (dob.length <= 0 ) {
                Dialog.alert(self, _t("Please Enter Date of Birth."), {
                    title: _t('Date Alert'),
                });
                return false
            }
            else if (gender.length <= 0 ) {
                Dialog.alert(self, _t("Please select the gender."), {
                    title: _t('Gender Alert'),
                });
                return false
            }
        });



    });
});
