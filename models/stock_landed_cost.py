from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta, date


class StockLandedCost(models.Model):
    _inherit="stock.landed.cost"
    vendor_id = fields.Many2one('res.partner',
                                string="vendor",
                                domain="[('supplier_rank','>',0)]")
    vendor_bill_id = fields.Many2one(
        'account.move', 'Vendor Bill', copy=False,
        domain="[('type', '=', 'in_invoice'),('partner_id','=', vendor_id)]")
