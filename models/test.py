from odoo import api, fields, models,_
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta


class TestTest(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        """ Overide the name_get() method of product model to show category"""
        res = super(TestTest, self).name_get()
        # data = []
        # if self.env.context.get('check'):
        #     for product in self:
        #         display_value = "{} {}".format(
        #             product.name or '', product.categ_id.name_get()[0][1] or '')
        #         data.append((product.id, display_value))
        #     return data
        # else:
        return res
