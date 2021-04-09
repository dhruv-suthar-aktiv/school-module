from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta, date
from collections import namedtuple, OrderedDict, defaultdict

class StockMove(models.Model):
    _inherit="stock.move"

    # Display the field in stock.move
    professor_ids = fields.Many2many(
                    'professor.professor','stockmove_professor_rel', string="Professors")

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # Display the field in Invoice lines
    professor_ids = fields.Many2many(
                    'professor.professor','account_move_professor_rel', string="Professors")

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    student_id = fields.Many2one('student.student',string = "Students")
    professor_ids = fields.Many2many(
                    'professor.professor','purchaseorder_professor_rel', string="Professors")

    @api.onchange('product_id')
    def onchange_product_id_purchase(self):
        """ On change of product the professor value will be updated in purchase
            order line"""
        for rec in self:
            rec.professor_ids = rec.product_id.professor_ids

    def _prepare_stock_moves(self, picking):
        """ Adds both field in reciept(stock.move)"""
        res = super(PurchaseOrderLine,self)._prepare_stock_moves(picking)
        res[0]['professor_ids'] = self.product_id.professor_ids.ids
        res[0]['student_id'] = self.student_id.id
        return res

    def _prepare_account_move_line(self, move):
        """ Add the professors field in draft bill's account move lines"""
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        res['student_id'] = self.student_id.id
        res['professor_ids'] = self.professor_ids.ids
        print('\n\n----res-----\n\n', res)
        return res


