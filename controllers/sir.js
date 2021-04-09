odoo.define('digi_website_quote.simplified_quote_request', function (require) {
"use strict";

var ajax = require("web.ajax");
var core=require("web.core");
var Widget = require("web.Widget");
var Dialog = require('web.Dialog');
var _t = core._t;

$(document).ready(function () {

    if (window.location.pathname == '/quotation/question') {
        get_apparatus() ;
    }

    function get_apparatus(){
        $(".table").find("tr:eq(3)").each(function () {
            var self = $(this);
            var appliances = $(this).find('.appliances').attr('appliances-id');
            if (appliances) {
                ajax.jsonRpc("/get_appliances_recs/", 'call', {'appliances_recs': appliances}).then(
                function(data) {
                    if (data) {
                        for (var i = 0; i < data.length; i++) {
                            self.find('.apparatus').append('<label class="text-center mr16"><input type="radio" name="apparatus" class="form-check"/>' + data[i] +
                                '</label>')
                        }
                    }
                });
            }
        });
    }

    $(".table").each(function () {
        var self = $(this);
        var number_of_parts = $(this).find('#number_of_parts')
        $(number_of_parts).change(function() {
            var current = $(this).val();
            var prev = self.find(".part_types").length
            var diff = current - prev;
            if (diff < 0 ){
                while (diff < 0) {
                    if(self.find(".part_types").length != 0 ) {
                        self.find("tr:nth-last-child(1)").remove()
                        diff++;
                    }
                }
            }
            else if (diff > 0) {
                for (var i = 0; i < diff; i++) {
                    self.find("tr:nth-last-child(1)").after('<tr class="part_types"><td class="col-md-4" style="background-color: #eeeeee;">Choix de la pièce :</td><td><select class="form-select select-selected custom_select_class" data-toggle="tooltip" id="type_of_parts" required="True"/></td></tr>')
                    var appliances = self.find('.appliances').attr('appliances-id');
                    if (appliances) {
                        ajax.jsonRpc("/get_product_recs/", 'call', {'appliances_recs': appliances}).then(
                        function(data) {
                            if (data) {
                                _.each(data, function (x) {
                                    $("table #type_of_parts").each(function () {
                                        if ($(this).children("option").length == 0) {
                                            $(this).append('<option value="' + '">' + '</option>');
                                            for (var i = 0; i < x.length; i++) {
                                                $(this).append('<option value="' + x[i] + '">' + x[i] + '</option>');
                                            }
                                        }
                                    })
                                })
                            }
                        });
                    }
                }
            }
        });
    });

    $('button.simplified_quote_submit').click(function () {
        var number_of_parts = $(".table").find('#number_of_parts').val()
        var number_of_level = $(".table").find('#number_of_level').val()
        var attic_suitable = $(".table").find("tr:eq(2) td:eq(1) input[type=radio]:checked").length
        var apparatus = $(".table").find("tr:eq(3) td:eq(1) input[type=radio]:checked").length
        var type_of_parts
        $(".table #type_of_parts").each(function () {
            if (!$(this).find("option:selected").val()) {
                type_of_parts = 0;
            }
        });
        if (number_of_parts > 0 && number_of_level > 0  && attic_suitable != 0 && apparatus != 0 && type_of_parts !=0 ) {
            $(".table").each(function () {
                var cols =[]
                var row = $(this).find("tr");
                for (var i = 0; i < row.length; i++) {
                    if (i == 0) {
                        cols.push({[i]:$(this).find("tr:eq(0) td:eq(1) input[type='number']").val()})
                    }
                    else if (i == 1) {
                        cols.push({[i]:$(this).find("tr:eq(1) td:eq(1) input[type='number']").val()})
                    }
                    else if (i == 2) {
                        cols.push({[i]:$(this).find("tr:eq(2) td:eq(1) input[type=radio]:checked").parent('label').text()})
                    }
                    else if (i == 3) {
                        cols.push({[i]:$(this).find("tr:eq(3) td:eq(1) input[type=radio]:checked").parent('label').text()})
                    }
                    else if (i > 3) {
                        cols.push({[i]:$(this).find("tr #type_of_parts option:selected")[(row.length - 1) - i].textContent})
                    }
                }
                $.ajax({
                        url:"/simplified/quote/products/calculation",
                        method:"POST",
                        cache: true,
                        async:false,
                        data:{
                            'cols': JSON.stringify(cols)
                        },
                    }).then(function (data){
                        window.location.href = '/shop/address'
                });
            });
        }
        else if (! number_of_parts || number_of_parts < 0 ) {
            Dialog.alert(self, _t("Please enter the quantity of number of parts."), {
                title: _t('Enter the Parts'),
            });
        }
        else if (! number_of_level || number_of_level < 0) {
            Dialog.alert(self, _t("Please enter the quantity of number of level."), {
                title: _t('Enter the Level'),
            });
        }
        else if (attic_suitable == 0) {
            Dialog.alert(self, _t("Please select Yes or No for Attic Suitable."), {
                title: _t('Select Attic Suitable'),
            });
        }
        else if (apparatus == 0) {
            Dialog.alert(self, _t("Please select the apparatus."), {
                title: _t('Select Apparatus'),
            });
        }
        else if (type_of_parts == 0) {
            Dialog.alert(self, _t("Please select the type of parts or reduce the number of parts"), {
                title: _t('Select Type of Parts'),
            });
        }
    });

});


});
