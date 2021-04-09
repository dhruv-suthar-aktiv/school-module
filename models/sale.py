from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta, date
from collections import namedtuple, OrderedDict, defaultdict


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # Display the field in Invoice lines
    student_id = fields.Many2one('student.student', string="Students")

class StockMove(models.Model):
    _inherit = "stock.move"

    # Display the field in stock.picking lines
    student_id = fields.Many2one('student.student', string="Students")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Display the field in sale order lines
    student_id = fields.Many2one('student.student', string="Students")
    professor_ids = fields.Many2many(
                'professor.professor','saleorder_professor_rel',string="Professors")

    @api.onchange('product_id')
    def onchange_product_id(self):
      """ Updates the value of professor when the porduct is
          changed im sale.order.line"""
      for rec in self:
          rec.professor_ids = rec.product_id.professor_ids

class StockRuleInherit(models.Model):
    _inherit = "stock.rule"

    # Call this method to add the student in the stock.move
    def _get_stock_move_values(self, product_id, product_qty, product_uom,
                               location_id, name, origin, company_id, values):
        """ Updates the move_values by adding the student record and return it"""

        res = super(StockRuleInherit, self)._get_stock_move_values(product_id,
                                                                   product_qty,
                                                                   product_uom,
                                                                   location_id,
                                                                   name, origin,
                                                                   company_id,
                                                                   values)

        res['student_id'] = self.env['sale.order.line'].browse(
            values.get('sale_line_id')).student_id.id
        return res

class SaleOrder(models.Model):
    _inherit = "sale.order"
    student_id = fields.Many2one('student.student', string="Students")

